import time
from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trial import ClinicalTrial, TrialCriterion
from app.models.patient import Patient, PatientLab, PatientBiomarker
from app.models.match import PatientTrialMatch
from app.ml.eligibility_engine import eligibility_engine
from app.ai.router import llm_router
from app.core.logging import logger

async def run_patient_screening_workflow(
    db: AsyncSession,
    patient_id: str,
    trial_id: str,
) -> Dict[str, Any]:
    """
    Executes deterministic clinical criteria matching and synthesizes an explainable
    eligibility battlecard using Sarvam AI 105B.
    """
    start_time = time.perf_counter()

    # 1. Fetch Patient EHR
    p_stmt = select(Patient).where(Patient.id == patient_id).options(
        selectinload(Patient.labs),
        selectinload(Patient.biomarkers),
    )
    p_res = await db.execute(p_stmt)
    patient = p_res.scalar_one_or_none()
    if not patient:
        raise ValueError(f"Patient '{patient_id}' not found.")

    # 2. Fetch Trial Protocol & Criteria
    t_stmt = select(ClinicalTrial).where(ClinicalTrial.id == trial_id).options(
        selectinload(ClinicalTrial.criteria),
    )
    t_res = await db.execute(t_stmt)
    trial = t_res.scalar_one_or_none()
    if not trial:
        raise ValueError(f"Trial '{trial_id}' not found.")

    # Structure patient data
    patient_data = {
        "age": patient.age,
        "ecog_performance": patient.ecog_performance,
        "prior_therapies": patient.prior_therapies or "",
        "biomarkers": [{"gene": b.gene, "mutation_variant": b.mutation_variant, "status": b.status} for b in patient.biomarkers],
        "labs": {l.test_name.lower(): {"value": l.result_value, "unit": l.unit} for l in patient.labs},
    }

    # Structure trial criteria
    criteria_list = [
        {
            "id": c.id,
            "criterion_type": c.criterion_type,
            "category": c.category,
            "description": c.description,
            "required_biomarker": c.required_biomarker,
            "min_numeric_value": c.min_numeric_value,
            "max_numeric_value": c.max_numeric_value,
        }
        for c in trial.criteria
    ]

    # 3. Deterministic Evaluation
    overall_status, confidence, breakdown = eligibility_engine.evaluate_patient_for_trial(
        trial_criteria=criteria_list,
        patient_data=patient_data,
    )

    # 4. Synthesize AI Explanation via Sarvam AI
    failed_items = [b for b in breakdown if b["status"] == "FAIL"]
    unknown_items = [b for b in breakdown if b["status"] == "UNKNOWN"]
    passed_items = [b for b in breakdown if b["status"] == "PASS"]

    system_prompt = (
        "You are an executive Principal Investigator & Clinical Trial Protocol Eligibility Copilot.\n"
        "RULES:\n"
        "1. STRICT CITATION & GROUNDING: Ground your assessment ONLY in the deterministic criteria evaluations provided.\n"
        "2. State the Overall Recommendation clearly: ELIGIBLE, INELIGIBLE, or UNCERTAIN.\n"
        "3. Provide clinical reasoning explaining why the patient passed or failed specific criteria.\n"
        "4. If there are missing labs/tests (UNKNOWN), provide a clear screening checklist for the study coordinator.\n"
        "5. Keep the tone concise, clinical, objective, and executive."
    )

    criteria_summary = "\n".join([
        f"- [{b['status']}] ({b['criterion_type']} - {b['category']}) {b['description']}: {b['evaluation_reason']}"
        for b in breakdown
    ])

    user_prompt = (
        f"PATIENT EHR SUMMARY:\n"
        f"- Patient MRN: {patient.synthetic_mrn} (Age: {patient.age}, Gender: {patient.gender})\n"
        f"- Diagnosis: {patient.primary_diagnosis} ({patient.stage}, ECOG PS: {patient.ecog_performance})\n"
        f"- Prior Therapies: {patient.prior_therapies or 'None'}\n"
        f"- Biomarkers: {', '.join([f'{b.gene} {b.mutation_variant}' for b in patient.biomarkers]) or 'None'}\n\n"
        f"TRIAL PROTOCOL:\n"
        f"- NCT ID: {trial.nct_id} - {trial.title} ({trial.phase})\n"
        f"- Target Condition: {trial.condition}\n\n"
        f"DETERMINISTIC CRITERIA BREAKDOWN:\n{criteria_summary}\n\n"
        f"OVERALL STATUS: {overall_status} (Confidence: {int(confidence*100)}%)\n"
        f"Synthesize an executive clinical eligibility assessment and study coordinator next steps."
    )

    llm_resp, fallback = await llm_router.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.15,
        max_tokens=700,
        grounded_context={
            "patient_id": patient.synthetic_mrn,
            "trial_id": trial.nct_id,
            "eligibility_status": overall_status,
        },
    )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return {
        "patient_id": patient.id,
        "patient_mrn": patient.synthetic_mrn,
        "trial_id": trial.id,
        "trial_nct": trial.nct_id,
        "trial_title": trial.title,
        "eligibility_status": overall_status,
        "confidence_score": confidence,
        "criteria_breakdown": breakdown,
        "failed_count": len(failed_items),
        "unknown_count": len(unknown_items),
        "passed_count": len(passed_items),
        "ai_explanation": llm_resp.content,
        "provider_used": llm_resp.provider_name,
        "latency_ms": latency_ms,
        "fallback_triggered": fallback,
    }

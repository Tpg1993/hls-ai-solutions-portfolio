import uuid
import random
from datetime import date, timedelta
from app.core.security import get_password_hash
from app.core.rbac import UserRole
from app.models.user import User
from app.models.trial import ClinicalTrial, TrialCriterion
from app.models.patient import Patient, PatientLab, PatientBiomarker
from app.models.site import TrialSite, SiteMetric
from app.models.match import PatientTrialMatch
from app.ml.site_risk_model import site_risk_engine
from app.ml.eligibility_engine import eligibility_engine

# Real clinical trials from clinical trials registries
TRIALS_DATA = [
    {
        "id": "TRIAL-NSCLC-01",
        "nct_id": "NCT04488081",
        "title": "Study of Amivantamab and Lazertinib in Patients With Advanced Non-Small Cell Lung Cancer (CHRYSALIS-2)",
        "phase": "Phase 2",
        "condition": "Non-Small Cell Lung Cancer (NSCLC)",
        "therapeutic_area": "Oncology",
        "target_enrollment": 180,
        "current_enrollment": 114,
        "status": "Recruiting",
        "summary": "Evaluates the efficacy and safety of the bispecific antibody Amivantamab in combination with Lazertinib in patients with advanced or metastatic NSCLC harboring EGFR Exon 20 insertion mutations whose disease has progressed on or after platinum-based chemotherapy.",
        "criteria": [
            {"type": "INCLUSION", "category": "AGE", "desc": "Age >= 18 years at the time of signing informed consent", "min": 18.0, "max": None, "bio": None},
            {"type": "INCLUSION", "category": "ECOG", "desc": "Eastern Cooperative Oncology Group (ECOG) performance status of 0 or 1", "min": 0.0, "max": 1.0, "bio": None},
            {"type": "INCLUSION", "category": "BIOMARKER", "desc": "Documented EGFR Exon 20 insertion mutation verified by CLIA-certified NGS or PCR assay", "min": None, "max": None, "bio": "EGFR_EXON_20"},
            {"type": "INCLUSION", "category": "LAB", "desc": "Adequate bone marrow function: Absolute Neutrophil Count (ANC) >= 1,500/uL", "min": 1.5, "max": None, "bio": "anc"},
            {"type": "INCLUSION", "category": "LAB", "desc": "Platelet count >= 100,000/uL without transfusion within 14 days", "min": 100.0, "max": None, "bio": "platelets"},
            {"type": "EXCLUSION", "category": "PRIOR_THERAPY", "desc": "Prior treatment with Amivantamab or EGFR/MET bispecific antibodies", "min": None, "max": None, "bio": "Amivantamab"},
            {"type": "EXCLUSION", "category": "LAB", "desc": "Serum creatinine > 1.5x Upper Limit of Normal (ULN)", "min": None, "max": 1.5, "bio": "creatinine"}
        ]
    },
    {
        "id": "TRIAL-BREAST-02",
        "nct_id": "NCT03329092",
        "title": "Trastuzumab Deruxtecan (T-DXd) vs Trastuzumab Emtansine (T-DM1) in HER2-Positive Metastatic Breast Cancer (DESTINY-Breast03)",
        "phase": "Phase 3",
        "condition": "HER2+ Breast Cancer",
        "therapeutic_area": "Oncology",
        "target_enrollment": 524,
        "current_enrollment": 490,
        "status": "Active, not recruiting",
        "summary": "Phase 3 confirmatory study comparing the antibody-drug conjugate Trastuzumab Deruxtecan with T-DM1 in patients with unresectable or metastatic HER2-positive breast cancer previously treated with Trastuzumab and a taxane.",
        "criteria": [
            {"type": "INCLUSION", "category": "AGE", "desc": "Age >= 18 years", "min": 18.0, "max": None, "bio": None},
            {"type": "INCLUSION", "category": "ECOG", "desc": "ECOG Performance Status 0 or 1", "min": 0.0, "max": 1.0, "bio": None},
            {"type": "INCLUSION", "category": "BIOMARKER", "desc": "Documented HER2-positive status by IHC 3+ or ISH positive on archived tumor tissue", "min": None, "max": None, "bio": "HER2_POSITIVE"},
            {"type": "INCLUSION", "category": "LAB", "desc": "Platelet count >= 100,000/uL", "min": 100.0, "max": None, "bio": "platelets"},
            {"type": "EXCLUSION", "category": "PRIOR_THERAPY", "desc": "Prior treatment with anti-HER2 antibody-drug conjugate containing exatecan derivative", "min": None, "max": None, "bio": "T-DXd"}
        ]
    },
    {
        "id": "TRIAL-LUNG-03",
        "nct_id": "NCT04077099",
        "title": "Osimertinib With or Without Chemotherapy in EGFR-Mutated Advanced NSCLC (FLAURA2)",
        "phase": "Phase 3",
        "condition": "EGFR-Mutant Non-Small Cell Lung Cancer",
        "therapeutic_area": "Oncology",
        "target_enrollment": 557,
        "current_enrollment": 412,
        "status": "Recruiting",
        "summary": "Evaluates whether adding platinum-pemetrexed doublet chemotherapy to first-line Osimertinib extends progression-free survival in patients with locally advanced or metastatic EGFR-mutated (Exon 19 del or L858R) NSCLC.",
        "criteria": [
            {"type": "INCLUSION", "category": "AGE", "desc": "Age >= 18 years", "min": 18.0, "max": None, "bio": None},
            {"type": "INCLUSION", "category": "ECOG", "desc": "ECOG Performance Status 0 or 1", "min": 0.0, "max": 1.0, "bio": None},
            {"type": "INCLUSION", "category": "BIOMARKER", "desc": "Local or central test confirming activating EGFR mutation (Exon 19 del or L858R)", "min": None, "max": None, "bio": "EGFR_ACTIVATING"},
            {"type": "INCLUSION", "category": "LAB", "desc": "Hemoglobin >= 9.0 g/dL", "min": 9.0, "max": None, "bio": "hemoglobin"},
            {"type": "EXCLUSION", "category": "PRIOR_THERAPY", "desc": "Prior systemic therapy for locally advanced or metastatic NSCLC", "min": None, "max": None, "bio": "Chemotherapy"}
        ]
    }
]

SITES_DATA = [
    {
        "id": "SITE-01",
        "site_number": "SITE-101",
        "site_name": "Dana-Farber Cancer Institute - Thoracic Oncology Center",
        "institution": "Dana-Farber Cancer Institute / Harvard Medical School",
        "city": "Boston",
        "state": "MA",
        "pi_name": "Dr. Pasi A. Jänne, MD, PhD",
        "target": 35,
        "enrolled": 31,
        "velocity": 3.8,
        "failure_rate": 0.18,
        "delay_days": 18,
        "dropout": 0.03,
    },
    {
        "id": "SITE-02",
        "site_number": "SITE-102",
        "site_name": "Memorial Sloan Kettering Cancer Center - Main Pavilion",
        "institution": "Memorial Sloan Kettering Cancer Center",
        "city": "New York",
        "state": "NY",
        "pi_name": "Dr. Mark G. Kris, MD",
        "target": 40,
        "enrolled": 36,
        "velocity": 4.1,
        "failure_rate": 0.15,
        "delay_days": 14,
        "dropout": 0.04,
    },
    {
        "id": "SITE-03",
        "site_number": "SITE-103",
        "site_name": "MD Anderson Cancer Center - Investigational Cancer Therapeutics",
        "institution": "University of Texas MD Anderson Cancer Center",
        "city": "Houston",
        "state": "TX",
        "pi_name": "Dr. John V. Heymach, MD, PhD",
        "target": 45,
        "enrolled": 39,
        "velocity": 4.5,
        "failure_rate": 0.14,
        "delay_days": 21,
        "dropout": 0.02,
    },
    {
        "id": "SITE-04",
        "site_number": "SITE-104",
        "site_name": "UCLA Health Jonsson Comprehensive Cancer Center",
        "institution": "University of California, Los Angeles",
        "city": "Los Angeles",
        "state": "CA",
        "pi_name": "Dr. Edward B. Garon, MD",
        "target": 30,
        "enrolled": 14,
        "velocity": 1.6,
        "failure_rate": 0.38,
        "delay_days": 54,
        "dropout": 0.08,
    },
    {
        "id": "SITE-05",
        "site_number": "SITE-105",
        "site_name": "Midwest Regional Medical Center - Oncology Annex",
        "institution": "Midwest Community Health Network",
        "city": "Des Moines",
        "state": "IA",
        "pi_name": "Dr. Arthur Pendelton, MD",
        "target": 25,
        "enrolled": 4,
        "velocity": 0.4,
        "failure_rate": 0.64,
        "delay_days": 115,
        "dropout": 0.22,
    },
    {
        "id": "SITE-06",
        "site_number": "SITE-106",
        "site_name": "Fred Hutchinson Cancer Center - Clinical Research Division",
        "institution": "Fred Hutchinson Cancer Center",
        "city": "Seattle",
        "state": "WA",
        "pi_name": "Dr. Keith D. Eaton, MD, PhD",
        "target": 28,
        "enrolled": 24,
        "velocity": 3.2,
        "failure_rate": 0.20,
        "delay_days": 24,
        "dropout": 0.05,
    }
]

PATIENTS_DATA = [
    {
        "id": "PT-001",
        "mrn": "MRN-ONC-88102",
        "age": 58,
        "gender": "Female",
        "diagnosis": "Non-Small Cell Lung Cancer (NSCLC)",
        "stage": "Stage IVB",
        "ecog": 1,
        "prior": "Carboplatin + Pemetrexed (4 cycles, completed 2024-01-15)",
        "notes": "58-year-old female non-smoker with metastatic adenocarcinoma of lung. Comprehensive next-gen sequencing confirms presence of EGFR Exon 20 insertion (p.Ala767_Val769dup). Experienced disease progression following front-line platinum doublet. Liver function preserved. Seeking second-line clinical protocol.",
        "biomarkers": [("EGFR", "Exon 20 Insertion (p.A767_V769dup)", "POSITIVE"), ("TP53", "R273H", "POSITIVE")],
        "labs": [("anc", 2.8, "10^3/uL"), ("platelets", 185.0, "10^3/uL"), ("creatinine", 0.9, "mg/dL"), ("hemoglobin", 11.4, "g/dL")]
    },
    {
        "id": "PT-002",
        "mrn": "MRN-ONC-94211",
        "age": 64,
        "gender": "Male",
        "diagnosis": "Non-Small Cell Lung Cancer (NSCLC)",
        "stage": "Stage IV",
        "ecog": 2, # Note ECOG 2 will fail ECOG <= 1 criterion
        "prior": "Cisplatin + Gemcitabine, Nivolumab",
        "notes": "64-year-old male with recurrent adenocarcinoma. Debilitating bone metastases resulting in ECOG performance status 2. Molecular profiling identified EGFR Exon 20 insertion mutation. Platelet counts border on thrombocytopenia due to recent myelosuppressive treatment.",
        "biomarkers": [("EGFR", "Exon 20 Insertion", "POSITIVE")],
        "labs": [("anc", 1.2, "10^3/uL"), ("platelets", 88.0, "10^3/uL"), ("creatinine", 1.8, "mg/dL"), ("hemoglobin", 8.8, "g/dL")]
    },
    {
        "id": "PT-003",
        "mrn": "MRN-ONC-63109",
        "age": 52,
        "gender": "Female",
        "diagnosis": "Invasive Ductal Carcinoma of Breast",
        "stage": "Stage IV Metastatic",
        "ecog": 0,
        "prior": "Trastuzumab + Pertuzumab + Docetaxel (completed 2023-09-10)",
        "notes": "52-year-old premenopausal female presenting with HER2-positive metastatic breast cancer to lung and bone. IHC 3+ strongly positive for HER2 amplification. Prior anti-HER2 therapy demonstrated partial response followed by progression. Patient maintains excellent functional status (ECOG 0).",
        "biomarkers": [("HER2", "HER2 Amplification (IHC 3+)", "POSITIVE"), ("PIK3CA", "H1047R", "POSITIVE")],
        "labs": [("anc", 3.4, "10^3/uL"), ("platelets", 240.0, "10^3/uL"), ("creatinine", 0.8, "mg/dL"), ("hemoglobin", 12.2, "g/dL")]
    },
    {
        "id": "PT-004",
        "mrn": "MRN-ONC-77291",
        "age": 71,
        "gender": "Male",
        "diagnosis": "Non-Small Cell Lung Cancer (NSCLC)",
        "stage": "Stage IIIB Locally Advanced",
        "ecog": 1,
        "prior": "None (Treatment Naive)",
        "notes": "71-year-old male presenting with locally advanced unresectable adenocarcinoma. Tissue biopsy sent for NGS panel revealed classical activating EGFR Exon 19 deletion. No prior systemic antineoplastic therapy administered. Eager to participate in first-line targeted combination trial.",
        "biomarkers": [("EGFR", "Exon 19 Deletion (E746_A750del)", "POSITIVE")],
        "labs": [("anc", 3.1, "10^3/uL"), ("platelets", 210.0, "10^3/uL"), ("creatinine", 1.1, "mg/dL"), ("hemoglobin", 13.5, "g/dL")]
    },
    {
        "id": "PT-005",
        "mrn": "MRN-ONC-51922",
        "age": 47,
        "gender": "Female",
        "diagnosis": "Non-Small Cell Lung Cancer (NSCLC)",
        "stage": "Stage IV",
        "ecog": 1,
        "prior": "Amivantamab + Chemotherapy (Discontinued for severe infusion reaction)", # Excluded prior therapy
        "notes": "47-year-old female with EGFR Exon 20 insertion lung cancer previously treated on compassionate use Amivantamab. Discontinued therapy after Cycle 2. Active search for alternative exon 20 targeted therapies or novel antibody-drug conjugates.",
        "biomarkers": [("EGFR", "Exon 20 Insertion", "POSITIVE")],
        "labs": [("anc", 2.2, "10^3/uL"), ("platelets", 160.0, "10^3/uL"), ("creatinine", 0.7, "mg/dL"), ("hemoglobin", 10.9, "g/dL")]
    }
]

def generate_clinical_trials_dataset():
    # 1. Users
    users = [
        User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@demo.clinical.hls",
            hashed_password=get_password_hash("Admin@123"),
            full_name="Global Clinical Operations Administrator",
            role=UserRole.ADMIN,
        ),
        User(
            id=str(uuid.uuid4()),
            username="clin_reviewer",
            email="reviewer@demo.clinical.hls",
            hashed_password=get_password_hash("Reviewer@123"),
            full_name="Lead Clinical Trial Protocol Reviewer",
            role=UserRole.CLINICAL_REVIEWER,
        ),
        User(
            id=str(uuid.uuid4()),
            username="auditor",
            email="auditor@demo.clinical.hls",
            hashed_password=get_password_hash("Auditor@123"),
            full_name="GCP Compliance & GCP Auditor",
            role=UserRole.AUDITOR,
        ),
        User(
            id=str(uuid.uuid4()),
            username="standard_user",
            email="nurse@demo.clinical.hls",
            hashed_password=get_password_hash("User@123"),
            full_name="Clinical Research Nurse / Coordinator",
            role=UserRole.STANDARD_USER,
        ),
    ]

    # 2. Trials & Criteria
    trials = []
    criteria = []
    for t_def in TRIALS_DATA:
        t = ClinicalTrial(
            id=t_def["id"],
            nct_id=t_def["nct_id"],
            title=t_def["title"],
            phase=t_def["phase"],
            condition=t_def["condition"],
            therapeutic_area=t_def["therapeutic_area"],
            target_enrollment=t_def["target_enrollment"],
            current_enrollment=t_def["current_enrollment"],
            status=t_def["status"],
            protocol_summary=t_def["summary"],
        )
        trials.append(t)

        for c_idx, c_def in enumerate(t_def["criteria"], 1):
            crit = TrialCriterion(
                id=f"CRIT-{t.id}-{c_idx:02d}",
                trial_id=t.id,
                criterion_type=c_def["type"],
                category=c_def["category"],
                description=c_def["desc"],
                min_numeric_value=c_def["min"],
                max_numeric_value=c_def["max"],
                required_biomarker=c_def["bio"],
            )
            criteria.append(crit)

    # 3. Sites & Site Metrics (with ML prediction)
    sites = []
    site_metrics = []
    for s_def in SITES_DATA:
        site = TrialSite(
            id=s_def["id"],
            site_number=s_def["site_number"],
            site_name=s_def["site_name"],
            institution=s_def["institution"],
            city=s_def["city"],
            state=s_def["state"],
            pi_name=s_def["pi_name"],
        )
        sites.append(site)

        # Predict ML Risk
        tier, score, _ = site_risk_engine.predict_site_risk(
            screening_velocity=s_def["velocity"],
            screen_failure_rate=s_def["failure_rate"],
            activation_delay_days=s_def["delay_days"],
            dropout_rate=s_def["dropout"],
            target_patients=s_def["target"],
            actual_enrolled=s_def["enrolled"],
        )

        metric = SiteMetric(
            id=f"METRIC-{site.id}",
            site_id=site.id,
            target_patients=s_def["target"],
            actual_enrolled=s_def["enrolled"],
            screening_velocity_per_month=s_def["velocity"],
            screen_failure_rate=s_def["failure_rate"],
            activation_delay_days=s_def["delay_days"],
            dropout_rate=s_def["dropout"],
            predicted_risk=tier,
            risk_score=score,
        )
        site_metrics.append(metric)

    # 4. Patients, Labs, Biomarkers
    patients = []
    labs = []
    biomarkers = []
    for p_def in PATIENTS_DATA:
        p = Patient(
            id=p_def["id"],
            synthetic_mrn=p_def["mrn"],
            age=p_def["age"],
            gender=p_def["gender"],
            primary_diagnosis=p_def["diagnosis"],
            stage=p_def["stage"],
            ecog_performance=p_def["ecog"],
            prior_therapies=p_def["prior"],
            clinical_notes=p_def["notes"],
        )
        patients.append(p)

        for gene, var, stat in p_def["biomarkers"]:
            bio = PatientBiomarker(
                id=f"BIO-{p.id}-{gene}",
                patient_id=p.id,
                gene=gene,
                mutation_variant=var,
                status=stat,
            )
            biomarkers.append(bio)

        for test, val, unit in p_def["labs"]:
            lab = PatientLab(
                id=f"LAB-{p.id}-{test}",
                patient_id=p.id,
                test_name=test,
                result_value=val,
                unit=unit,
                test_date=date(2024, 3, 10),
            )
            labs.append(lab)

    # 5. Precomputed Patient-Trial Matches
    matches = []
    for p in patients:
        for t in trials:
            t_crits = [
                {
                    "id": c.id,
                    "criterion_type": c.criterion_type,
                    "category": c.category,
                    "description": c.description,
                    "min_numeric_value": c.min_numeric_value,
                    "max_numeric_value": c.max_numeric_value,
                    "required_biomarker": c.required_biomarker,
                }
                for c in criteria if c.trial_id == t.id
            ]
            p_dict = {
                "age": p.age,
                "ecog_performance": p.ecog_performance,
                "prior_therapies": p.prior_therapies or "",
                "biomarkers": [{"gene": b.gene, "mutation_variant": b.mutation_variant, "status": b.status} for b in biomarkers if b.patient_id == p.id],
                "labs": {l.test_name.lower(): {"value": l.result_value, "unit": l.unit} for l in labs if l.patient_id == p.id},
            }
            status, conf, breakdown = eligibility_engine.evaluate_patient_for_trial(t_crits, p_dict)

            match = PatientTrialMatch(
                id=f"MATCH-{p.id}-{t.id}",
                patient_id=p.id,
                trial_id=t.id,
                eligibility_status=status,
                confidence_score=conf,
                criteria_breakdown=breakdown,
                review_status="PENDING" if status == "ELIGIBLE" else "REJECTED",
                reviewer_notes="Automated deterministic criteria screening." if status != "ELIGIBLE" else "Queued for Lead Clinical Reviewer sign-off.",
                ai_explanation=f"Patient {p.synthetic_mrn} evaluated against {t.nct_id}. Deterministic eligibility outcome: {status} (Confidence: {int(conf*100)}%).",
            )
            matches.append(match)

    return {
        "users": users,
        "trials": trials,
        "criteria": criteria,
        "sites": sites,
        "site_metrics": site_metrics,
        "patients": patients,
        "labs": labs,
        "biomarkers": biomarkers,
        "matches": matches,
    }

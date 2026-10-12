import asyncio
import random
from datetime import date, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.recommendation import Recommendation
from app.ai.providers.sarvam_provider import SarvamProvider
from app.core.logging import logger

CLINICAL_SCENARIOS = [
    {
        "topic": "Clinical Efficacy & Progression-Free Survival (PFS)",
        "context": "Phase 3 clinical trial readout demonstrating superior 24-month PFS versus current standard of care."
    },
    {
        "topic": "Biomarker Stratification & Next-Gen Sequencing (NGS)",
        "context": "Discussion around patient selection criteria, liquid biopsy turnaround time, and targetable oncogenic mutations."
    },
    {
        "topic": "Formulary Access, Prior Authorization & Patient Assistance",
        "context": "Physician concern over patient co-pay burdens, Tier 2 formulary inclusion, and rapid turnaround for prior-auth appeals."
    },
    {
        "topic": "Adverse Event Mitigation & Dose Modification Protocols",
        "context": "Managing Grade 1/2 skin rash and immune-mediated adverse reactions; guidance on proactive supportive care regimens."
    },
    {
        "topic": "Head-to-Head Comparative Safety Profile vs Competitor",
        "context": "Detailing lower discontinuation rates and favorable cardiotoxicity profile compared to first-generation tyrosine kinase inhibitors."
    }
]

async def generate_sarvam_field_note(provider: SarvamProvider, hcp_name: str, specialty: str, hospital: str, scenario: dict) -> str:
    """Calls live Sarvam AI to create a realistic, detailed field call note."""
    prompt = (
        f"You are a Senior Pharmaceutical Field Representative & Medical Science Liaison. "
        f"Generate a realistic, professional, concise 3-4 sentence field interaction note for your meeting with "
        f"{hcp_name}, a {specialty} specialist at {hospital}.\n"
        f"Discussion Topic: {scenario['topic']}\n"
        f"Clinical Context: {scenario['context']}\n"
        f"Include: Physician's key question/feedback, reaction to clinical data, and agreed follow-up action.\n"
        f"Tone: Clinical, objective, and executive. Do not use generic filler."
    )
    
    try:
        resp = await provider.generate_text(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=350,
        )
        return resp.content.strip()
    except Exception as e:
        logger.error(f"Sarvam generation failed for {hcp_name}: {e}")
        return (
            f"Met with {hcp_name} at {hospital} to review {scenario['topic']}. "
            f"Discussed {scenario['context']}. Agreed to provide follow-up safety monographs next week."
        )

async def run_enrichment(limit: int = 20):
    print(f"\n=======================================================")
    print(f"  Live AI Commercial Data Generator (Sarvam AI 105B)  ")
    print(f"=======================================================\n")
    
    provider = SarvamProvider()
    if not await provider.is_available():
        print("ERROR: Sarvam API key not configured in .env!")
        return

    print("Sarvam AI provider initialized and verified successfully.")
    print(f"Enriching top {limit} high-priority HCPs with live LLM clinical interaction logs...\n")

    async with AsyncSessionLocal() as db:
        # Select high decile HCPs
        stmt = select(HCP).order_by(HCP.decile.desc()).limit(limit)
        res = await db.execute(stmt)
        hcps = res.scalars().all()

        count = 0
        for hcp in hcps:
            scenario = random.choice(CLINICAL_SCENARIOS)
            full_name = f"Dr. {hcp.first_name} {hcp.last_name}"
            print(f"[{count+1}/{len(hcps)}] Generating Sarvam AI clinical note for {full_name} ({hcp.specialty}, Decile {hcp.decile})...")
            
            note_text = await generate_sarvam_field_note(
                provider=provider,
                hcp_name=full_name,
                specialty=hcp.specialty,
                hospital=hcp.hospital_affiliation,
                scenario=scenario,
            )

            # Insert a new detailed interaction
            import uuid
            inter_id = f"INT-AI-{hcp.id}-{uuid.uuid4().hex[:6]}"
            inter_date = date.today() - timedelta(days=random.randint(2, 45))
            channel = random.choice(["In-Person Detail", "Medical Science Liaison (MSL) Briefing", "Virtual Advisory"])
            sentiment = random.choice(["Positive", "Positive", "Hesitant", "Advocate"])

            new_inter = Interaction(
                id=inter_id,
                hcp_id=hcp.id,
                interaction_date=inter_date,
                channel=channel,
                rep_name="Live AI Commercial Copilot",
                topics_discussed=scenario["topic"],
                sentiment=sentiment,
                notes=f"[Sarvam AI Generated Call Note]\n{note_text}",
            )
            db.add(new_inter)
            count += 1
            print(f"    --> Generated note ({len(note_text)} chars): {note_text[:120]}...\n")

        await db.commit()
        print(f"Successfully generated and committed {count} live Sarvam AI interaction records to the database!")

if __name__ == "__main__":
    asyncio.run(run_enrichment(limit=10))

import random
from datetime import datetime, timezone, timedelta
from app.core.database import Base, sync_engine, SyncSessionLocal
from app.core.security import get_password_hash
from app.models.safety import User, SafetyCase, SafetySignal, EvidenceDocument, SafetyReview, AuditEvent
from app.statistics.disproportionality import calculate_disproportionality_metrics

def seed_database():
    """
    Initializes database tables and seeds synthetic pharmacovigilance data.
    """
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()

    # If users already seeded, return
    if session.query(User).first():
        session.close()
        return

    # 1. Seed RBAC Users
    users = [
        User(
            username="admin",
            hashed_password=get_password_hash("AdminPassword123!"),
            role="ADMIN",
            full_name="PV System Administrator"
        ),
        User(
            username="safety_reviewer",
            hashed_password=get_password_hash("ReviewerPassword123!"),
            role="SAFETY_REVIEWER",
            full_name="Dr. Eleanor Vance (Lead Safety Physician)"
        ),
        User(
            username="analyst",
            hashed_password=get_password_hash("AnalystPassword123!"),
            role="ANALYST",
            full_name="Marcus Brody (Drug Safety Case Specialist)"
        ),
        User(
            username="auditor",
            hashed_password=get_password_hash("AuditorPassword123!"),
            role="AUDITOR",
            full_name="Sarah Jenkins (Regulatory Compliance Auditor)"
        )
    ]
    session.add_all(users)
    session.commit()

    # 2. Seed Synthetic Safety Cases (ICSRs)
    drugs = ["CardioShield", "NeuroCalm", "OncoVax", "ImmunoBlast"]
    events = [
        ("Acute Hepatitis", "Hepatobiliary disorders"),
        ("Ventricular Tachycardia", "Cardiac disorders"),
        ("Stevens-Johnson Syndrome", "Skin and subcutaneous tissue disorders"),
        ("Severe Thrombocytopenia", "Blood and lymphatic system disorders"),
        ("Acute Kidney Injury", "Renal and urinary disorders"),
        ("Mild Headache", "Nervous system disorders"),
        ("Nausea", "Gastrointestinal disorders")
    ]
    severities = ["SERIOUS_HOSPITALIZATION", "LIFE_THREATENING", "NON_SERIOUS"]
    outcomes = ["RECOVERED", "NOT_RECOVERED", "FATAL", "UNKNOWN"]
    countries = ["US", "DE", "FR", "JP", "GB", "IN"]

    sample_cases = []
    # Seed 80 background cases + clustered signal cases
    random.seed(42)
    for i in range(1, 101):
        case_id = f"ICSR-2026-{1000 + i}"
        # Ensure CardioShield + Acute Hepatitis is enriched to form a real signal
        if i <= 24:
            drug = "CardioShield"
            event, soc = ("Acute Hepatitis", "Hepatobiliary disorders")
            sev = "SERIOUS_HOSPITALIZATION"
            out = "NOT_RECOVERED" if i % 2 == 0 else "RECOVERED"
        elif i <= 36:
            drug = "OncoVax"
            event, soc = ("Severe Thrombocytopenia", "Blood and lymphatic system disorders")
            sev = "LIFE_THREATENING" if i % 3 == 0 else "SERIOUS_HOSPITALIZATION"
            out = "RECOVERED"
        else:
            drug = random.choice(drugs)
            event, soc = random.choice(events)
            sev = random.choice(severities)
            out = random.choice(outcomes)

        age = random.randint(22, 79)
        sex = random.choice(["M", "F"])
        cntry = random.choice(countries)
        narrative = (
            f"Patient {age}yo {sex} received {drug} 50mg daily. On day 14, developed {event.lower()}. "
            f"Patient required intervention and was classified as {sev.lower()}."
        )

        sample_cases.append(SafetyCase(
            case_id=case_id,
            age=age,
            sex=sex,
            suspect_drug=drug,
            dosage="50mg daily",
            adverse_event=event,
            meddra_soc=soc,
            severity=sev,
            outcome=out,
            country=cntry,
            date_received=(datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            narrative_raw=narrative,
            narrative_scrubbed=narrative
        ))
    session.add_all(sample_cases)
    session.commit()

    # 3. Seed Deterministic Safety Signals
    # Signal 1: CardioShield <-> Acute Hepatitis
    # Contingency Table: a=24, b=16, c=4, d=56 -> N=100
    m1 = calculate_disproportionality_metrics(a=24, b=16, c=4, d=56)
    sig1 = SafetySignal(
        drug_name="CardioShield",
        adverse_event="Acute Hepatitis",
        meddra_soc="Hepatobiliary disorders",
        observed_cases=24,
        expected_cases=m1["expected_cases"],
        total_drug_cases=40,
        total_event_cases=28,
        prr=m1["prr"],
        prr_ci_lower=m1["prr_ci_lower"],
        prr_ci_upper=m1["prr_ci_upper"],
        ror=m1["ror"],
        ror_ci_lower=m1["ror_ci_lower"],
        ror_ci_upper=m1["ror_ci_upper"],
        chi_square=m1["chi_square"],
        risk_level=m1["risk_level"],
        signal_status="OPEN"
    )

    # Signal 2: OncoVax <-> Severe Thrombocytopenia
    # Contingency Table: a=12, b=18, c=6, d=64
    m2 = calculate_disproportionality_metrics(a=12, b=18, c=6, d=64)
    sig2 = SafetySignal(
        drug_name="OncoVax",
        adverse_event="Severe Thrombocytopenia",
        meddra_soc="Blood and lymphatic system disorders",
        observed_cases=12,
        expected_cases=m2["expected_cases"],
        total_drug_cases=30,
        total_event_cases=18,
        prr=m2["prr"],
        prr_ci_lower=m2["prr_ci_lower"],
        prr_ci_upper=m2["prr_ci_upper"],
        ror=m2["ror"],
        ror_ci_lower=m2["ror_ci_lower"],
        ror_ci_upper=m2["ror_ci_upper"],
        chi_square=m2["chi_square"],
        risk_level=m2["risk_level"],
        signal_status="INVESTIGATING"
    )

    # Signal 3: NeuroCalm <-> Mild Headache (Routine, not a signal)
    m3 = calculate_disproportionality_metrics(a=3, b=25, c=10, d=62)
    sig3 = SafetySignal(
        drug_name="NeuroCalm",
        adverse_event="Mild Headache",
        meddra_soc="Nervous system disorders",
        observed_cases=3,
        expected_cases=m3["expected_cases"],
        total_drug_cases=28,
        total_event_cases=13,
        prr=m3["prr"],
        prr_ci_lower=m3["prr_ci_lower"],
        prr_ci_upper=m3["prr_ci_upper"],
        ror=m3["ror"],
        ror_ci_lower=m3["ror_ci_lower"],
        ror_ci_upper=m3["ror_ci_upper"],
        chi_square=m3["chi_square"],
        risk_level=m3["risk_level"],
        signal_status="CLOSED"
    )
    session.add_all([sig1, sig2, sig3])
    session.commit()

    # 4. Seed Evidence Documents (Drug Labels and PubMed abstracts)
    docs = [
        EvidenceDocument(
            doc_type="DRUG_LABEL",
            drug_name="CardioShield",
            adverse_event="Acute Hepatitis",
            title="CardioShield USPI Package Insert (FDA Approved)",
            section="Section 5.2 - Warnings and Precautions: Hepatic Injury",
            citation="FDA Label Ref #2024-CS-09",
            text_chunk=(
                "Elevations in ALT and AST greater than 3x ULN were observed in 0.8% of clinical trial patients. "
                "Post-marketing spontaneous reports have identified acute hepatic failure and severe cholestasis, "
                "primarily occurring within the first 6 weeks of initiation. Discontinue CardioShield immediately if symptoms occur."
            ),
            relevance_score=0.96
        ),
        EvidenceDocument(
            doc_type="LITERATURE_PUBMED",
            drug_name="CardioShield",
            adverse_event="Acute Hepatitis",
            title="Drug-Induced Liver Injury Associated with Novel Anti-Arrhythmic CardioShield: A Multicenter Series",
            section="Results & Case Discussion",
            citation="J. Hepatol. 2025; 82(4): 512-519. PMID: 39120481",
            text_chunk=(
                "We report 14 patients presenting with severe hepatocellular jaundice after commencing CardioShield. "
                "Mean latency to jaundice was 19 days (range 7-42 days). Roussel Uclaf Causality Assessment Method (RUCAM) "
                "indicated 'Probable' causality in 11/14 cases. Histopathology revealed marked centrilobular necrosis."
            ),
            relevance_score=0.92
        ),
        EvidenceDocument(
            doc_type="DRUG_LABEL",
            drug_name="OncoVax",
            adverse_event="Severe Thrombocytopenia",
            title="OncoVax Prescribing Information",
            section="Section 5.4 - Hematologic Toxicities",
            citation="EMA Summary of Product Characteristics, Ref: EMEA/H/C/004910",
            text_chunk=(
                "Grade 3/4 thrombocytopenia occurred in 4.1% of patients receiving combination regimens. "
                "Platelet nadirs generally occurred on Cycle 1 Day 14. Routine weekly CBC monitoring is recommended."
            ),
            relevance_score=0.88
        )
    ]
    session.add_all(docs)
    session.commit()
    session.close()

if __name__ == "__main__":
    seed_database()

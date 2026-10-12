import uuid
from datetime import date, timedelta
from typing import Dict, Any, List
from app.core.security import get_password_hash
from app.core.rbac import UserRole
from app.models.user import User
from app.models.guidance import GuidanceDocument, GuidanceSection
from app.models.diff import GuidanceVersionDiff
from app.models.submission_impact import SubmissionImpact

GUIDANCES_DEF = [
    {
        "id": "DOC-FDA-RWE-2024",
        "authority": "FDA",
        "title": "Real-World Evidence: Considerations Regarding Registry Data in Oncology and Rare Disease Submissions",
        "document_number": "FDA-2021-D-1149",
        "therapeutic_area": "Oncology",
        "doc_type": "Final Guidance",
        "status": "Final",
        "publication_date": date(2024, 4, 18),
        "version": "2.0",
        "summary": "Provides comprehensive recommendations for sponsors considering submitting real-world data (RWD) from disease registries to support regulatory approval decisions for oncology and rare diseases.",
        "sections": [
            {
                "section_number": "Section 2.1",
                "section_title": "Registry Selection and Relevance Assessment",
                "page_number": 6,
                "keywords": "registry selection, fitness-for-use, data completeness, patient accrual",
                "text": "Sponsors should evaluate whether the candidate registry captures key data elements with sufficient granularity, including baseline disease histology, prior treatment regimens, molecular biomarkers, and longitudinal survival outcomes. Missingness patterns in clinical variables must be pre-specified in the statistical analysis plan."
            },
            {
                "section_number": "Section 3.2",
                "section_title": "Data Quality, Validation Protocols, and Audit Trails",
                "page_number": 14,
                "keywords": "audit trail, source data verification, electronic validation, 21 CFR Part 11",
                "text": "Electronic registry systems must maintain immutable, computer-generated, time-stamped audit trails complying with 21 CFR Part 11. Sponsors must perform independent source data verification on a risk-stratified sample of at least 15% of registry patients to validate real-world progression-free survival (rwPFS) against primary health records."
            },
            {
                "section_number": "Section 4.4",
                "section_title": "Confounding Control and Propensity Score Matching",
                "page_number": 23,
                "keywords": "propensity score, unmeasured confounding, sensitivity analysis, external control",
                "text": "When constructing an external synthetic control arm from registry cohorts, sponsors must utilize robust propensity score matching or weighting. Quantitative sensitivity analyses (e.g., tipping point and E-value analyses) are mandatory to assess the potential impact of unmeasured confounding on hazard ratio estimates."
            }
        ]
    },
    {
        "id": "DOC-FDA-RWE-2021",
        "authority": "FDA",
        "title": "Real-World Evidence: Considerations Regarding Registry Data in Oncology (Draft)",
        "document_number": "FDA-2021-D-1149-DRAFT",
        "therapeutic_area": "Oncology",
        "doc_type": "Draft Guidance",
        "status": "Superseded",
        "publication_date": date(2021, 11, 10),
        "version": "1.0",
        "summary": "Initial draft guidance setting forth preliminary thoughts on registry data relevance and quality for regulatory submissions.",
        "sections": [
            {
                "section_number": "Section 3.2",
                "section_title": "Data Quality and Electronic Records",
                "page_number": 12,
                "keywords": "electronic records, validation, registry inspection",
                "text": "Sponsors should discuss their data quality assurance plans with FDA during pre-IND meetings. Electronic systems should have reasonable safeguards to prevent unauthorized modifications."
            }
        ]
    },
    {
        "id": "DOC-EMA-ICHE6R3-2024",
        "authority": "EMA / ICH",
        "title": "ICH Guideline E6(R3) on Good Clinical Practice (GCP) — Integrated Addendum",
        "document_number": "EMA/CHMP/ICH/135/1995-Rev3",
        "therapeutic_area": "Clinical Methodology",
        "doc_type": "Final Guideline",
        "status": "Final",
        "publication_date": date(2024, 7, 22),
        "version": "3.0",
        "summary": "Overhauls clinical trial governance to support decentralized clinical trials, digital health technologies, electronic source records, and risk-proportionate monitoring.",
        "sections": [
            {
                "section_number": "Section 2.6",
                "section_title": "Data Governance and Digital Health Technologies (DHT)",
                "page_number": 19,
                "keywords": "digital health technologies, wearable sensors, continuous monitoring, data validation",
                "text": "Data capture through digital health technologies, wearable sensors, and remote patient portals must be governed by documented validation protocols. Sponsors must ensure data integrity from continuous physiological streams and preserve full metadata context during transmission."
            },
            {
                "section_number": "Section 3.4",
                "section_title": "Risk-Based and Centralized Quality Monitoring",
                "page_number": 31,
                "keywords": "risk-based monitoring, centralized statistical monitoring, site anomaly detection",
                "text": "Clinical monitoring must be proportionate to the inherent risks to participant safety and data reliability. Centralized statistical monitoring using automated threshold triggers and anomaly detection should be employed to identify site-level variance before routine on-site audits."
            }
        ]
    },
    {
        "id": "DOC-FDA-AI-2024",
        "authority": "FDA",
        "title": "Artificial Intelligence and Machine Learning (AI/ML) in Drug Development and Clinical Pharmacology",
        "document_number": "FDA-2024-D-0820",
        "therapeutic_area": "Digital Health",
        "doc_type": "Final Guidance",
        "status": "Final",
        "publication_date": date(2024, 5, 30),
        "version": "1.0",
        "summary": "Sets clarity on transparency, explainability, lifecycle validation, and risk management for predictive AI/ML algorithms used in clinical trials and dose optimization.",
        "sections": [
            {
                "section_number": "Section 3.1",
                "section_title": "Model Explainability and Traceability Standards",
                "page_number": 11,
                "keywords": "explainability, black-box algorithms, feature importance, SHAP, clinical validation",
                "text": "When AI/ML models are used to enrich patient enrollment or predict therapeutic response, sponsors must demonstrate biological plausibility and feature interpretability. Black-box algorithmic outputs without feature attribution or deterministic verification will not be accepted for primary efficacy claims."
            },
            {
                "section_number": "Section 5.2",
                "section_title": "Algorithmic Drift and Continuous Lifecycle Monitoring",
                "page_number": 28,
                "keywords": "data drift, concept drift, model retraining, predetermined change control plan (PCCP)",
                "text": "Sponsors must submit a Predetermined Change Control Plan (PCCP) outlining procedures for monitoring input distribution drift and performance degradation. Retraining triggers, regression testing suites, and human oversight gates must be established prior to study initiation."
            }
        ]
    },
    {
        "id": "DOC-PMDA-REG-2024",
        "authority": "PMDA",
        "title": "Basic Principles on Utilization of Registry Data for Applications of Pharmaceuticals and Medical Devices",
        "document_number": "PMDA-NOTIF-0329-1",
        "therapeutic_area": "Regulatory Submissions",
        "doc_type": "Guideline",
        "status": "Final",
        "publication_date": date(2024, 3, 29),
        "version": "1.2",
        "summary": "Establishes regulatory expectations in Japan for utilizing domestic and international patient registries in new drug applications.",
        "sections": [
            {
                "section_number": "Section 1.3",
                "section_title": "Reliability Assessment of External Registry Data",
                "page_number": 8,
                "keywords": "Japan PMDA, GPSP conformance, registry reliability, consultation",
                "text": "When utilizing registry data as external controls, sponsors must conduct prior PMDA consultations. Reliability assurance under Good Post-marketing Study Practice (GPSP) requires transparent standard operating procedures and accessible source documentation."
            }
        ]
    }
]

DIFFS_DEF = [
    {
        "id": "DIFF-RWE-01",
        "baseline_doc_id": "DOC-FDA-RWE-2021",
        "comparison_doc_id": "DOC-FDA-RWE-2024",
        "section_number": "Section 3.2",
        "section_title": "Data Quality, Validation Protocols, and Audit Trails",
        "change_type": "MODIFICATION",
        "old_text": "Sponsors should discuss their data quality assurance plans with FDA during pre-IND meetings. Electronic systems should have reasonable safeguards to prevent unauthorized modifications.",
        "new_text": "Electronic registry systems must maintain immutable, computer-generated, time-stamped audit trails complying with 21 CFR Part 11. Sponsors must perform independent source data verification on a risk-stratified sample of at least 15% of registry patients to validate real-world progression-free survival (rwPFS) against primary health records.",
        "semantic_impact": "Elevates recommendation to a strict quantitative requirement: mandates 21 CFR Part 11 compliance and 15% minimum independent source data verification (SDV) for progression endpoints.",
        "impact_severity": "CRITICAL"
    },
    {
        "id": "DIFF-RWE-02",
        "baseline_doc_id": "DOC-FDA-RWE-2021",
        "comparison_doc_id": "DOC-FDA-RWE-2024",
        "section_number": "Section 4.4",
        "section_title": "Confounding Control and Propensity Score Matching",
        "change_type": "ADDITION",
        "old_text": "None (Section was not present in 2021 Draft).",
        "new_text": "When constructing an external synthetic control arm from registry cohorts, sponsors must utilize robust propensity score matching or weighting. Quantitative sensitivity analyses (e.g., tipping point and E-value analyses) are mandatory to assess the potential impact of unmeasured confounding on hazard ratio estimates.",
        "semantic_impact": "Introduces formal requirement for sensitivity analysis (tipping point and E-value) when using external synthetic control arms in regulatory submissions.",
        "impact_severity": "HIGH"
    }
]

SUBMISSIONS_DEF = [
    {
        "id": "SUB-001",
        "guidance_id": "DOC-FDA-RWE-2024",
        "product_name": "OncoVax-7 (mRNA Neoantigen Vaccine)",
        "ind_nda_number": "IND-149204",
        "development_phase": "Phase 2b",
        "therapeutic_area": "Oncology",
        "impact_level": "Critical",
        "impact_summary": "Phase 2b expansion study utilizes an external synthetic registry control arm for overall survival. 2024 Final Guidance mandates 15% independent SDV and formal E-value sensitivity testing.",
        "action_required": "Commission third-party audit to perform 15% SDV on 310 registry patient records; revise statistical analysis plan with tipping-point analysis before Type B FDA meeting.",
        "compliance_deadline": date(2026, 12, 15)
    },
    {
        "id": "SUB-002",
        "guidance_id": "DOC-FDA-AI-2024",
        "product_name": "CardioStat-Alpha (Targeted SGLT2 Inhibitor)",
        "ind_nda_number": "NDA-218491",
        "development_phase": "Phase 3 Confirmatory",
        "therapeutic_area": "Cardiovascular",
        "impact_level": "High",
        "impact_summary": "Trial incorporates an AI algorithmic dose optimization tool. Requires formal submission of a Predetermined Change Control Plan (PCCP) and feature attribution documentation.",
        "action_required": "Prepare PCCP regulatory dossier and compile SHAP feature interpretability validation package for FDA review.",
        "compliance_deadline": date(2027, 2, 28)
    },
    {
        "id": "SUB-003",
        "guidance_id": "DOC-EMA-ICHE6R3-2024",
        "product_name": "NeuroRegen-09 (ASO Therapy)",
        "ind_nda_number": "CTA-2023-00918",
        "development_phase": "Phase 2",
        "therapeutic_area": "Neurology",
        "impact_level": "Moderate",
        "impact_summary": "Protocol uses continuous wearable accelerometry. Under ICH E6(R3) Section 2.6, data capture requires validated digital health technology SOPs and metadata preservation.",
        "action_required": "Update clinical protocol with wearable data governance SOP and establish automated anomaly alerts for decentralized site monitoring.",
        "compliance_deadline": date(2026, 11, 30)
    }
]

def generate_regulatory_dataset():
    # 1. Users
    users = [
        User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@demo.regulatory.hls",
            hashed_password=get_password_hash("Admin@123"),
            full_name="Global Regulatory Affairs Administrator",
            role=UserRole.ADMIN,
        ),
        User(
            id=str(uuid.uuid4()),
            username="reg_reviewer",
            email="reviewer@demo.regulatory.hls",
            hashed_password=get_password_hash("Reviewer@123"),
            full_name="Senior Regulatory Affairs Specialist",
            role=UserRole.REGULATORY_REVIEWER,
        ),
        User(
            id=str(uuid.uuid4()),
            username="auditor",
            email="auditor@demo.regulatory.hls",
            hashed_password=get_password_hash("Auditor@123"),
            full_name="Compliance & Regulatory Auditor",
            role=UserRole.AUDITOR,
        ),
        User(
            id=str(uuid.uuid4()),
            username="standard_user",
            email="user@demo.regulatory.hls",
            hashed_password=get_password_hash("User@123"),
            full_name="Clinical Submissions Coordinator",
            role=UserRole.STANDARD_USER,
        ),
    ]

    # 2. Guidance Documents and Sections
    guidances = []
    sections = []
    for g_def in GUIDANCES_DEF:
        doc = GuidanceDocument(
            id=g_def["id"],
            authority=g_def["authority"],
            title=g_def["title"],
            document_number=g_def["document_number"],
            therapeutic_area=g_def["therapeutic_area"],
            doc_type=g_def["doc_type"],
            status=g_def["status"],
            publication_date=g_def["publication_date"],
            version=g_def["version"],
            summary=g_def["summary"],
        )
        guidances.append(doc)

        for s_def in g_def["sections"]:
            sec = GuidanceSection(
                id=f"SEC-{doc.id}-{s_def['section_number'].replace(' ', '_')}",
                document_id=doc.id,
                section_number=s_def["section_number"],
                section_title=s_def["section_title"],
                page_number=s_def["page_number"],
                chunk_text=s_def["text"],
                keywords=s_def["keywords"],
            )
            sections.append(sec)

    # 3. Diffs
    diffs = [
        GuidanceVersionDiff(
            id=d["id"],
            baseline_doc_id=d["baseline_doc_id"],
            comparison_doc_id=d["comparison_doc_id"],
            section_number=d["section_number"],
            section_title=d["section_title"],
            change_type=d["change_type"],
            old_text=d["old_text"],
            new_text=d["new_text"],
            semantic_impact=d["semantic_impact"],
            impact_severity=d["impact_severity"],
        )
        for d in DIFFS_DEF
    ]

    # 4. Submission Impacts
    submissions = [
        SubmissionImpact(
            id=s["id"],
            guidance_id=s["guidance_id"],
            product_name=s["product_name"],
            ind_nda_number=s["ind_nda_number"],
            development_phase=s["development_phase"],
            therapeutic_area=s["therapeutic_area"],
            impact_level=s["impact_level"],
            impact_summary=s["impact_summary"],
            action_required=s["action_required"],
            compliance_deadline=s["compliance_deadline"],
        )
        for s in SUBMISSIONS_DEF
    ]

    return {
        "users": users,
        "guidances": guidances,
        "sections": sections,
        "diffs": diffs,
        "submissions": submissions,
    }

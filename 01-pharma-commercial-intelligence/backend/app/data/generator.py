import random
import uuid
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Any
from app.core.security import get_password_hash
from app.core.rbac import UserRole
from app.models.user import User
from app.models.territory import Territory
from app.models.product import Product
from app.models.hcp import HCP
from app.models.prescription import Prescription
from app.models.interaction import Interaction
from app.models.recommendation import Recommendation
from app.ml.features import compute_hcp_features
from app.ml.model import propensity_engine
from app.ml.nba_rules import evaluate_nba_decision

FIRST_NAMES = [
    "Sarah", "David", "Priya", "Michael", "Elena", "James", "Ananya", "Robert", "Fatima", "Carlos",
    "Emily", "Brian", "Mei", "Marcus", "Jessica", "Alexander", "Aisha", "Jonathan", "Grace", "Daniel",
    "Siddharth", "Laura", "Raj", "Hannah", "Kevin", "Deepa", "Andrew", "Maya", "Christopher", "Rachel"
]

LAST_NAMES = [
    "Chen", "Patel", "Miller", "Gupta", "Rodriguez", "Kim", "Smith", "Johnson", "Williams", "Brown",
    "Jones", "Garcia", "Davis", "Martinez", "Hernandez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore",
    "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez"
]

SPECIALTIES = ["Oncology", "Cardiology", "Endocrinology", "Internal Medicine", "Hematology"]

HOSPITALS = [
    "Memorial Cancer Center", "Johns Hopkins Hospital", "Mount Sinai Medical Center",
    "Massachusetts General Hospital", "Cleveland Clinic", "Mayo Clinic Comprehensive",
    "Stanford Health Care", "UCLA Ronald Reagan Center", "Northwestern Memorial Hospital",
    "MD Anderson Cancer Center", "Brigham and Women's Hospital", "Cedars-Sinai Medical Center"
]

CITIES_STATES = [
    ("Boston", "MA", "02115"),
    ("New York", "NY", "10029"),
    ("Philadelphia", "PA", "19104"),
    ("Houston", "TX", "77030"),
    ("Chicago", "IL", "60611"),
    ("Los Angeles", "CA", "90095"),
    ("San Francisco", "CA", "94143"),
    ("Seattle", "WA", "98195"),
    ("Atlanta", "GA", "30322"),
    ("Cleveland", "OH", "44195"),
]

TERRITORIES_DEF = [
    ("TERR-NE-01", "North-East Oncology Alpha", "North", 1500000.0, "Rachel Green", "rachel.green@demo.hls", "Oncology"),
    ("TERR-MA-02", "Mid-Atlantic Cardiology Prime", "East", 1200000.0, "Mark Sloan", "mark.sloan@demo.hls", "Cardiology"),
    ("TERR-SE-03", "South-East Specialty Care", "South", 1100000.0, "Lisa Cuddy", "lisa.cuddy@demo.hls", "Oncology"),
    ("TERR-MW-04", "Mid-West Commercial Health", "North", 1350000.0, "John Dorian", "john.dorian@demo.hls", "Internal Medicine"),
    ("TERR-SW-05", "South-West Oncology District", "South", 1400000.0, "Gregory House", "gregory.house@demo.hls", "Oncology"),
    ("TERR-NW-06", "Pacific North-West Bio", "West", 1250000.0, "Allison Cameron", "allison.cameron@demo.hls", "Cardiology"),
    ("TERR-PC-07", "Pacific Coast Premier", "West", 1600000.0, "Eric Foreman", "eric.foreman@demo.hls", "Oncology"),
    ("TERR-GL-08", "Great Lakes Therapeutics", "North", 1150000.0, "James Wilson", "james.wilson@demo.hls", "Hematology"),
]

PRODUCTS_DEF = [
    ("PROD-ONCO-01", "OncoVex", "Oncology", "Primary", 2200.0, "CompeteX-Onc"),
    ("PROD-CARD-02", "CardioShield", "Cardiology", "Primary", 1400.0, "VascuGuard"),
    ("PROD-ENDO-03", "GlycoStab", "Endocrinology", "Secondary", 850.0, "InsuliPrime"),
]

def generate_synthetic_data(num_hcps: int = 10000, seed: int = 42):
    random.seed(seed)
    print(f"Generating synthetic commercial dataset with {num_hcps} HCPs...")

    # 1. Users across roles
    users = [
        User(
            id=str(uuid.uuid4()),
            username="superadmin",
            email="superadmin@demo.hls",
            hashed_password=get_password_hash("SuperAdmin@123"),
            full_name="Global Portfolio Architect",
            role=UserRole.SUPER_ADMIN,
        ),
        User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@demo.hls",
            hashed_password=get_password_hash("Admin@123"),
            full_name="Commercial System Admin",
            role=UserRole.ADMIN,
        ),
        User(
            id=str(uuid.uuid4()),
            username="business_owner",
            email="business.owner@demo.hls",
            hashed_password=get_password_hash("Business@123"),
            full_name="VP Commercial Operations",
            role=UserRole.BUSINESS_OWNER,
        ),
        User(
            id=str(uuid.uuid4()),
            username="analyst",
            email="analyst@demo.hls",
            hashed_password=get_password_hash("Analyst@123"),
            full_name="Senior Commercial Analyst",
            role=UserRole.ANALYST,
        ),
        User(
            id=str(uuid.uuid4()),
            username="auditor",
            email="auditor@demo.hls",
            hashed_password=get_password_hash("Auditor@123"),
            full_name="Compliance & Model Auditor",
            role=UserRole.AUDITOR,
        ),
        User(
            id=str(uuid.uuid4()),
            username="standard_user",
            email="rep.user@demo.hls",
            hashed_password=get_password_hash("User@123"),
            full_name="Field Representative",
            role=UserRole.STANDARD_USER,
        ),
    ]

    # 2. Territories
    territories = [
        Territory(
            id=t[0],
            name=t[1],
            region=t[2],
            quota=t[3],
            assigned_rep_name=t[4],
            assigned_rep_email=t[5],
            target_specialty=t[6],
        )
        for t in TERRITORIES_DEF
    ]

    # 3. Products
    products = [
        Product(
            id=p[0],
            name=p[1],
            therapeutic_area=p[2],
            brand_tier=p[3],
            price_per_unit=p[4],
            competitor_product_name=p[5],
        )
        for p in PRODUCTS_DEF
    ]

    # 4. HCPs & longitudinal Rx
    hcps = []
    prescriptions = []
    interactions = []
    recommendations = []

    months = [
        "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06",
        "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"
    ]

    for i in range(1, num_hcps + 1):
        hcp_id = f"HCP-{i:05d}"
        npi = f"9{random.randint(100000000, 999999999)}"
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        spec = random.choice(SPECIALTIES)
        hosp = random.choice(HOSPITALS)
        city, state, zip_code = random.choice(CITIES_STATES)
        terr = random.choice(territories).id
        decile = random.choices(range(1, 11), weights=[5, 6, 8, 10, 15, 18, 14, 11, 8, 5])[0]
        affinity = random.choice(["High", "Medium", "Low"])
        stage = random.choice(["Advocate", "Trialist", "Skeptic"])

        hcp = HCP(
            id=hcp_id,
            npi_synthetic=npi,
            first_name=fn,
            last_name=ln,
            specialty=spec,
            hospital_affiliation=hosp,
            address=f"{random.randint(100, 999)} Health Ave, Suite {random.randint(10, 500)}",
            city=city,
            state=state,
            zip_code=zip_code,
            territory_id=terr,
            decile=decile,
            digital_affinity=affinity,
            adoption_stage=stage,
        )
        hcps.append(hcp)

        # Matched primary product
        prod_id = "PROD-ONCO-01" if spec == "Oncology" or spec == "Hematology" else (
            "PROD-CARD-02" if spec == "Cardiology" else "PROD-ENDO-03"
        )

        base_vol = decile * random.randint(3, 7)
        hcp_rx_list = []

        for m_idx, m in enumerate(months):
            # Dynamic growth or dip
            growth_factor = 1.0 + (m_idx * random.uniform(-0.03, 0.05))
            trx = max(1, int(base_vol * growth_factor + random.randint(-2, 3)))
            nrx = max(0, int(trx * random.uniform(0.15, 0.40)))
            comp_trx = max(2, int(trx * random.uniform(0.6, 1.4)))

            rx_record = Prescription(
                id=f"RX-{hcp_id}-{m}",
                hcp_id=hcp_id,
                product_id=prod_id,
                month_year=m,
                trx_count=trx,
                nrx_count=nrx,
                competitor_trx_count=comp_trx,
            )
            prescriptions.append(rx_record)
            hcp_rx_list.append({
                "month_year": m,
                "trx_count": trx,
                "nrx_count": nrx,
                "competitor_trx_count": comp_trx,
            })

        # Interactions
        num_interactions = random.randint(1, 4)
        hcp_inter_list = []
        for j in range(num_interactions):
            inter_id = f"INT-{hcp_id}-{j+1}"
            days_ago = random.randint(5, 120)
            inter_date = date(2024, 12, 31) - timedelta(days=days_ago)
            channel = random.choice(["In-Person Detail", "Virtual Call", "Approved Email", "Medical Webinar"])
            sentiment = random.choice(["Positive", "Neutral", "Hesitant"])
            topics = random.choice([
                "Head-to-head clinical efficacy data and OS endpoints",
                "Biomarker selection and genomic testing protocols",
                "Formulary tier placement and co-pay assistance cards",
                "Adverse event management and patient compliance tips",
            ])
            inter = Interaction(
                id=inter_id,
                hcp_id=hcp_id,
                interaction_date=inter_date,
                channel=channel,
                rep_name="Assigned Commercial Rep",
                topics_discussed=topics,
                sentiment=sentiment,
                notes=f"Discussed {topics} with {hcp.first_name}. Sentiment was {sentiment}.",
            )
            interactions.append(inter)
            hcp_inter_list.append({
                "channel": channel,
                "sentiment": sentiment,
                "days_ago": days_ago,
            })

        # Precompute initial recommendation for Top 2,500 HCPs
        if i <= 2500:
            feat = compute_hcp_features(decile, affinity, hcp_rx_list, hcp_inter_list)
            prop_score, drivers = propensity_engine.predict_propensity(feat)
            tier, action, rec_channel = evaluate_nba_decision(prop_score, feat)

            rec = Recommendation(
                id=f"REC-{hcp_id}",
                hcp_id=hcp_id,
                product_id=prod_id,
                propensity_score=prop_score,
                priority_tier=tier,
                recommended_action=action,
                recommended_channel=rec_channel,
                top_drivers=drivers,
                model_version="xgb-v1.0",
                status="PENDING",
            )
            recommendations.append(rec)

    print(f"Generated: {len(users)} users, {len(territories)} territories, {len(products)} products, "
          f"{len(hcps)} HCPs, {len(prescriptions)} prescriptions, {len(interactions)} interactions, "
          f"{len(recommendations)} recommendations.")

    return {
        "users": users,
        "territories": territories,
        "products": products,
        "hcps": hcps,
        "prescriptions": prescriptions,
        "interactions": interactions,
        "recommendations": recommendations,
    }

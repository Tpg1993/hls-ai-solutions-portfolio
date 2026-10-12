import pytest
from app.ml.features import compute_hcp_features
from app.ml.model import propensity_engine

def test_feature_computation():
    prescriptions = [
        {"month_year": "2024-01", "trx_count": 10, "nrx_count": 3, "competitor_trx_count": 8},
        {"month_year": "2024-02", "trx_count": 12, "nrx_count": 4, "competitor_trx_count": 9},
        {"month_year": "2024-03", "trx_count": 15, "nrx_count": 5, "competitor_trx_count": 10},
    ]
    interactions = [
        {"channel": "In-Person Detail", "sentiment": "Positive"},
        {"channel": "Email", "sentiment": "Positive"},
    ]

    features = compute_hcp_features(
        hcp_decile=8,
        digital_affinity="High",
        prescriptions=prescriptions,
        interactions=interactions,
    )

    assert features["hcp_decile"] == 8.0
    assert 0.0 <= features["competitor_share"] <= 1.0
    assert 0.0 <= features["digital_affinity_score"] <= 1.0
    assert features["interaction_frequency_6m"] == 2.0

def test_propensity_prediction_bounds():
    features = {
        "hcp_decile": 9.0,
        "trx_growth_3m": 0.25,
        "nrx_to_trx_ratio": 0.35,
        "competitor_share": 0.40,
        "days_since_last_interaction": 12.0,
        "interaction_frequency_6m": 4.0,
        "digital_affinity_score": 0.85,
        "historical_response_rate": 0.75,
    }

    score, drivers = propensity_engine.predict_propensity(features)
    assert 0.0 <= score <= 1.0
    assert isinstance(drivers, dict)
    assert "trx_growth_3m" in drivers
    assert "competitor_share" in drivers

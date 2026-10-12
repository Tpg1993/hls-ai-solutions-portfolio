import pytest
from app.ml.nba_rules import evaluate_nba_decision

def test_high_propensity_high_competitor_action():
    features = {
        "competitor_share": 0.65,
        "days_since_last_interaction": 20.0,
        "digital_affinity_score": 0.40,
        "hcp_decile": 9.0,
    }
    tier, action, channel = evaluate_nba_decision(0.85, features)
    assert tier == "High"
    assert "Head-to-Head Efficacy Data" in action
    assert channel == "In-Person Detail"

def test_medium_propensity_digital_action():
    features = {
        "competitor_share": 0.30,
        "days_since_last_interaction": 30.0,
        "digital_affinity_score": 0.85,
        "hcp_decile": 6.0,
    }
    tier, action, channel = evaluate_nba_decision(0.55, features)
    assert tier == "Medium"
    assert "Digital Detail" in action
    assert channel == "Approved Email"

def test_low_propensity_low_decile_action():
    features = {
        "competitor_share": 0.20,
        "days_since_last_interaction": 90.0,
        "digital_affinity_score": 0.20,
        "hcp_decile": 2.0,
    }
    tier, action, channel = evaluate_nba_decision(0.20, features)
    assert tier == "Low"
    assert "Newsletter" in action

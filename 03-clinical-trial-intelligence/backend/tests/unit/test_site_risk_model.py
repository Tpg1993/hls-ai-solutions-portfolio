import pytest
from app.ml.site_risk_model import site_risk_engine

def test_site_risk_prediction_high():
    # Low velocity, high failure rate, large delay
    tier, score, drivers = site_risk_engine.predict_site_risk(
        screening_velocity=0.4,
        screen_failure_rate=0.65,
        activation_delay_days=110,
        dropout_rate=0.20,
        target_patients=25,
        actual_enrolled=3,
    )
    assert tier == "High"
    assert score >= 0.5
    assert len(drivers) >= 1

def test_site_risk_prediction_low():
    # High velocity, low failure rate, minimal delay, good enrollment
    tier, score, drivers = site_risk_engine.predict_site_risk(
        screening_velocity=4.5,
        screen_failure_rate=0.15,
        activation_delay_days=14,
        dropout_rate=0.03,
        target_patients=35,
        actual_enrolled=32,
    )
    assert tier == "Low"
    assert score < 0.4

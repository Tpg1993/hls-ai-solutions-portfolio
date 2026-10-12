import pytest
from app.statistics.disproportionality import calculate_disproportionality_metrics

def test_prr_ror_calculation_signal():
    """
    Test contingency table where a drug has disproportionate reports of an event.
    a=24 (Drug+Event), b=16 (Drug+Other), c=4 (Other+Event), d=56 (Other+Other)
    """
    metrics = calculate_disproportionality_metrics(a=24, b=16, c=4, d=56)
    
    # Numerator PRR: 24/40 = 0.60
    # Denominator PRR: 4/60 = 0.0667
    # Expected PRR: 0.60 / 0.0667 = 9.0
    assert metrics["prr"] > 5.0
    assert metrics["ror"] > 5.0
    assert metrics["chi_square"] > 4.0
    assert metrics["is_signal"] is True
    assert metrics["risk_level"] == "HIGH"
    assert metrics["prr_ci_lower"] > 1.0

def test_prr_non_signal_baseline():
    """
    Test background noise where event distribution is proportional.
    a=2, b=40, c=10, d=150
    """
    metrics = calculate_disproportionality_metrics(a=2, b=40, c=10, d=150)
    # Less than 3 observed cases -> Evans criteria requires a >= 3
    assert metrics["is_signal"] is False
    assert metrics["risk_level"] == "LOW"

def test_zero_contingency_defense():
    """
    Test robustness when counts are zero
    """
    metrics = calculate_disproportionality_metrics(a=0, b=0, c=0, d=0)
    assert metrics["prr"] == 1.0
    assert metrics["chi_square"] == 0.0
    assert metrics["is_signal"] is False

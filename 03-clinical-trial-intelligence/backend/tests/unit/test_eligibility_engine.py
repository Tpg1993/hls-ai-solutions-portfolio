import pytest
from app.ml.eligibility_engine import eligibility_engine

def test_inclusion_age_pass():
    crit = {"criterion_type": "INCLUSION", "category": "AGE", "min_numeric_value": 18.0}
    res = eligibility_engine.evaluate_criterion(crit, {"age": 55})
    assert res["status"] == "PASS"

def test_inclusion_age_fail():
    crit = {"criterion_type": "INCLUSION", "category": "AGE", "min_numeric_value": 18.0}
    res = eligibility_engine.evaluate_criterion(crit, {"age": 16})
    assert res["status"] == "FAIL"

def test_ecog_failure():
    crit = {"criterion_type": "INCLUSION", "category": "ECOG", "max_numeric_value": 1.0}
    res = eligibility_engine.evaluate_criterion(crit, {"ecog_performance": 2})
    assert res["status"] == "FAIL"

def test_biomarker_matching():
    crit = {"criterion_type": "INCLUSION", "category": "BIOMARKER", "required_biomarker": "EGFR_EXON_20"}
    patient_pos = {"biomarkers": [{"gene": "EGFR", "mutation_variant": "Exon 20 Insertion", "status": "POSITIVE"}]}
    res_pos = eligibility_engine.evaluate_criterion(crit, patient_pos)
    assert res_pos["status"] == "PASS"

    patient_neg = {"biomarkers": [{"gene": "KRAS", "mutation_variant": "G12C", "status": "POSITIVE"}]}
    res_neg = eligibility_engine.evaluate_criterion(crit, patient_neg)
    assert res_neg["status"] == "FAIL"

def test_lab_threshold_evaluation():
    crit = {"criterion_type": "INCLUSION", "category": "LAB", "required_biomarker": "platelets", "min_numeric_value": 100.0}
    # Pass
    res1 = eligibility_engine.evaluate_criterion(crit, {"labs": {"platelets": {"value": 150.0, "unit": "k/uL"}}})
    assert res1["status"] == "PASS"
    # Fail
    res2 = eligibility_engine.evaluate_criterion(crit, {"labs": {"platelets": {"value": 75.0, "unit": "k/uL"}}})
    assert res2["status"] == "FAIL"
    # Unknown (missing lab)
    res3 = eligibility_engine.evaluate_criterion(crit, {"labs": {}})
    assert res3["status"] == "UNKNOWN"

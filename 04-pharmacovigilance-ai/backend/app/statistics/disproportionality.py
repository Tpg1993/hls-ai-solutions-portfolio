import math
from typing import Dict, Any, Tuple

def calculate_disproportionality_metrics(
    a: int,  # Suspect Drug + Target Event
    b: int,  # Suspect Drug + Other Events
    c: int,  # Other Drugs + Target Event
    d: int   # Other Drugs + Other Events
) -> Dict[str, Any]:
    """
    Computes deterministic Pharmacovigilance disproportionality metrics (PRR, ROR, Chi-square, Expected cases).
    Strictly deterministic - zero LLM calculation.
    """
    total_n = a + b + c + d
    if total_n == 0:
        return {
            "prr": 1.0, "prr_ci_lower": 1.0, "prr_ci_upper": 1.0,
            "ror": 1.0, "ror_ci_lower": 1.0, "ror_ci_upper": 1.0,
            "chi_square": 0.0, "expected_cases": 0.0, "is_signal": False, "risk_level": "LOW"
        }

    # Expected count under independence
    expected = ((a + b) * (a + c)) / total_n

    # PRR calculation: (a / (a + b)) / (c / (c + d))
    denom_prr = (c / (c + d)) if (c + d) > 0 else 0
    numer_prr = (a / (a + b)) if (a + b) > 0 else 0
    
    if denom_prr > 0 and numer_prr > 0:
        prr = numer_prr / denom_prr
        # Variance of ln(PRR) = 1/a - 1/(a+b) + 1/c - 1/(c+d)
        se_prr_sq = (1.0 / max(a, 1)) - (1.0 / max(a + b, 1)) + (1.0 / max(c, 1)) - (1.0 / max(c + d, 1))
        se_prr = math.sqrt(max(se_prr_sq, 0.0001))
        prr_ci_lower = math.exp(math.log(prr) - 1.96 * se_prr)
        prr_ci_upper = math.exp(math.log(prr) + 1.96 * se_prr)
    else:
        prr = 1.0
        prr_ci_lower = 1.0
        prr_ci_upper = 1.0

    # ROR calculation: (a * d) / (b * c)
    if b * c > 0 and a * d > 0:
        ror = (a * d) / (b * c)
        se_ror = math.sqrt((1.0 / a) + (1.0 / b) + (1.0 / c) + (1.0 / d))
        ror_ci_lower = math.exp(math.log(ror) - 1.96 * se_ror)
        ror_ci_upper = math.exp(math.log(ror) + 1.96 * se_ror)
    else:
        ror = 1.0
        ror_ci_lower = 1.0
        ror_ci_upper = 1.0

    # Chi-square with Yates continuity correction
    denom_chi = float((a + b) * (c + d) * (a + c) * (b + d))
    if denom_chi > 0:
        yates_term = abs(a * d - b * c) - (total_n / 2.0)
        chi_square = (total_n * (max(0.0, yates_term) ** 2)) / denom_chi
    else:
        chi_square = 0.0

    # Evans Criteria for Safety Signal:
    # 1. Observed cases >= 3
    # 2. PRR >= 2.0
    # 3. Chi-square >= 4.0 (approx p < 0.05)
    is_signal = bool(a >= 3 and prr >= 2.0 and chi_square >= 4.0)

    # Risk Level classification
    if is_signal and prr >= 3.0 and chi_square >= 15.0:
        risk_level = "HIGH"
    elif is_signal:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "prr": round(prr, 2),
        "prr_ci_lower": round(prr_ci_lower, 2),
        "prr_ci_upper": round(prr_ci_upper, 2),
        "ror": round(ror, 2),
        "ror_ci_lower": round(ror_ci_lower, 2),
        "ror_ci_upper": round(ror_ci_upper, 2),
        "chi_square": round(chi_square, 2),
        "expected_cases": round(expected, 2),
        "is_signal": is_signal,
        "risk_level": risk_level
    }

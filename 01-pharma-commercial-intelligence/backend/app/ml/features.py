import numpy as np
import pandas as pd
from typing import Dict, Any, List

def compute_hcp_features(
    hcp_decile: int,
    digital_affinity: str,
    prescriptions: List[Dict[str, Any]],
    interactions: List[Dict[str, Any]],
    reference_date_str: str = "2024-12-31"
) -> Dict[str, float]:
    """
    Computes normalized, reproducible feature vectors for an HCP.
    Deterministic numerics only - no LLM hallucinations.
    """
    # 1. Prescription features
    if prescriptions and len(prescriptions) >= 3:
        # Sort by month_year
        sorted_rx = sorted(prescriptions, key=lambda x: x["month_year"])
        last_3 = sorted_rx[-3:]
        prev_3 = sorted_rx[-6:-3] if len(sorted_rx) >= 6 else sorted_rx[:3]
        
        recent_trx = sum(r.get("trx_count", 0) for r in last_3)
        past_trx = max(1, sum(r.get("trx_count", 0) for r in prev_3))
        trx_growth_3m = float((recent_trx - past_trx) / past_trx)
        
        recent_nrx = sum(r.get("nrx_count", 0) for r in last_3)
        nrx_to_trx_ratio = float(recent_nrx / max(1, recent_trx))
        
        recent_comp_trx = sum(r.get("competitor_trx_count", 0) for r in last_3)
        total_market = recent_trx + recent_comp_trx
        competitor_share = float(recent_comp_trx / max(1, total_market))
    else:
        trx_growth_3m = 0.05
        nrx_to_trx_ratio = 0.20
        competitor_share = 0.45

    # 2. CRM interaction features
    if interactions:
        interaction_frequency_6m = float(len(interactions))
        days_since_last_interaction = 25.0  # Normalized default
        
        # Digital touch ratio
        digital_channels = {"Email", "Webinar", "Virtual Call"}
        digital_count = sum(1 for i in interactions if i.get("channel") in digital_channels)
        digital_ratio = float(digital_count / max(1, len(interactions)))
        
        positive_sentiment_count = sum(1 for i in interactions if i.get("sentiment") == "Positive")
        historical_response_rate = float(positive_sentiment_count / max(1, len(interactions)))
    else:
        interaction_frequency_6m = 1.0
        days_since_last_interaction = 60.0
        digital_ratio = 0.33
        historical_response_rate = 0.40

    digital_affinity_map = {"High": 0.85, "Medium": 0.50, "Low": 0.15}
    digital_affinity_score = digital_affinity_map.get(digital_affinity, 0.50)

    return {
        "hcp_decile": float(hcp_decile),
        "trx_growth_3m": round(float(np.clip(trx_growth_3m, -1.0, 2.0)), 4),
        "nrx_to_trx_ratio": round(float(np.clip(nrx_to_trx_ratio, 0.0, 1.0)), 4),
        "competitor_share": round(float(np.clip(competitor_share, 0.0, 1.0)), 4),
        "days_since_last_interaction": round(float(np.clip(days_since_last_interaction, 1.0, 180.0)), 1),
        "interaction_frequency_6m": round(float(interaction_frequency_6m), 1),
        "digital_affinity_score": round(float(digital_affinity_score), 4),
        "historical_response_rate": round(float(historical_response_rate), 4),
    }

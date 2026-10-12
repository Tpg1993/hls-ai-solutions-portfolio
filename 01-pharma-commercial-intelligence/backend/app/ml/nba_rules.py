from typing import Dict, Any, Tuple

def evaluate_nba_decision(
    propensity_score: float,
    features: Dict[str, float]
) -> Tuple[str, str, str]:
    """
    Evaluates deterministic Next-Best-Action (NBA) matrix based on:
    - Calibrated ML propensity score
    - Competitor share & interaction recency
    - Digital affinity & decile
    Returns: (priority_tier, recommended_action, recommended_channel)
    """
    competitor_share = features.get("competitor_share", 0.45)
    days_since_interaction = features.get("days_since_last_interaction", 30.0)
    digital_affinity = features.get("digital_affinity_score", 0.50)
    hcp_decile = features.get("hcp_decile", 5.0)

    # Priority Tier assignment
    if propensity_score >= 0.70:
        priority_tier = "High"
    elif propensity_score >= 0.40:
        priority_tier = "Medium"
    else:
        priority_tier = "Low"

    # Action & Channel assignment
    if priority_tier == "High":
        if competitor_share >= 0.50:
            recommended_action = "Clinical Detail - Head-to-Head Efficacy Data"
            recommended_channel = "In-Person Detail"
        elif days_since_interaction >= 45:
            recommended_action = "Urgent Re-Engagement - Patient Initiation Support"
            recommended_channel = "In-Person Detail"
        else:
            recommended_action = "Key Account Follow-Up - Dosing & Safety Briefing"
            recommended_channel = "Virtual Call"
    elif priority_tier == "Medium":
        if digital_affinity >= 0.65:
            recommended_action = "Digital Detail - Interactive Clinical Case Study"
            recommended_channel = "Approved Email"
        elif competitor_share >= 0.40:
            recommended_action = "Peer Advisory - Regional Oncology Expert Webinar"
            recommended_channel = "Medical Webinar"
        else:
            recommended_action = "Sample Delivery & Patient Starter Kit Refill"
            recommended_channel = "In-Person Detail"
    else:  # Low
        if hcp_decile >= 7:
            recommended_action = "Awareness Re-engagement - Clinical Trial Update"
            recommended_channel = "Approved Email"
        else:
            recommended_action = "Automated Monthly Therapeutic Newsletter"
            recommended_channel = "Approved Email"

    return priority_tier, recommended_action, recommended_channel

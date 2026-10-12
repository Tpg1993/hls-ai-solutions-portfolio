# Commercial ROI Model & Deterministic Assumptions

## 1. Core Mathematical Model
All financial calculations originate exclusively from deterministic Python logic in `app/services/roi_service.py`.

### 1.1 Field Representative Time Savings:
$$\text{Total Annual Calls} = \text{Reps} \times \text{Calls per Rep per Month} \times 12$$
$$\text{Annual Hours Saved} = \frac{\text{Total Annual Calls} \times \text{Minutes Saved per Call}}{60}$$
$$\text{Productivity Economic Value} = \text{Annual Hours Saved} \times \text{Rep Hourly Rate}$$

### 1.2 Detailing Conversion Uplift:
$$\text{Incremental Converted Calls} = \text{Total Annual Calls} \times \text{Baseline Conversion Rate} \times \text{Conversion Lift Percentage}$$
$$\text{Incremental Gross Revenue} = \text{Incremental Converted Calls} \times \text{Average Revenue per Converted Rx}$$

### 1.3 Net Economic Impact:
$$\text{Total Net Benefit} = \text{Productivity Economic Value} + \text{Incremental Gross Revenue}$$

## 2. Standard Baseline Assumptions (Illustrative)
- **Field Force Size**: 50 full-time commercial representatives.
- **Detaiing Cadence**: 120 calls per rep per month.
- **Pre-Call Planning Efficiency Gain**: 15 minutes saved per call.
- **Fully-Loaded Rep Cost**: $75/hour.
- **Baseline Detailing Conversion**: 8.0%.
- **Expected NBA Uplift**: +15% relative improvement (moving conversion from 8.0% to 9.2%).
- **Gross Value per Initiated Treatment**: $1,500.
- **Calculated Annual Economic Impact**: **$1,650,000+**.

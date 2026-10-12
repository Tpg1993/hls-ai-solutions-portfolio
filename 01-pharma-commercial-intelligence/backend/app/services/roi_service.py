from app.schemas.roi import ROIInputs, ROIOutputs

class ROIService:
    @staticmethod
    def calculate_commercial_roi(inputs: ROIInputs) -> ROIOutputs:
        """
        Calculates deterministic commercial impact from NBA adoption:
        1. Time & Productivity Savings:
           Annual hours saved = (reps * calls/rep/month * 12 * minutes_saved) / 60
           Productivity value = hours_saved * rep_hourly_rate
        2. Commercial Detailing Revenue Uplift:
           Total calls = reps * calls/rep/month * 12
           Incremental conversions = total_calls * baseline_conversion * conversion_lift
           Incremental gross revenue = incremental_conversions * average_rx_revenue
        3. Net Economic Benefit & ROI:
           Total benefit = productivity_value + incremental_gross_revenue
           ROI percentage = (Total benefit / (total_reps_salary_allocation)) * 100
        """
        total_annual_calls = inputs.num_reps * inputs.calls_per_rep_month * 12
        annual_hours_saved = (total_annual_calls * inputs.minutes_saved_per_call) / 60.0
        annual_productivity_val = annual_hours_saved * inputs.rep_hourly_rate

        incremental_conversions = (
            total_annual_calls * inputs.baseline_conversion_rate * inputs.conversion_lift_percentage
        )
        incremental_gross_rev = incremental_conversions * inputs.average_rx_revenue
        total_net_benefit = annual_productivity_val + incremental_gross_rev

        # Approximate investment baseline (estimated platform cost + change management: $250k)
        estimated_investment = 250000.0
        roi_percentage = ((total_net_benefit - estimated_investment) / estimated_investment) * 100.0

        return ROIOutputs(
            annual_hours_saved=round(annual_hours_saved, 1),
            annual_productivity_value=round(annual_productivity_val, 2),
            incremental_converted_calls=round(incremental_conversions, 1),
            incremental_gross_revenue=round(incremental_gross_rev, 2),
            total_net_economic_benefit=round(total_net_benefit, 2),
            roi_percentage=round(roi_percentage, 1),
        )

roi_service = ROIService()

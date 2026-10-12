from pydantic import BaseModel, Field

class ROIInputs(BaseModel):
    num_reps: int = Field(default=50, ge=1, le=500, description="Total field sales representatives")
    calls_per_rep_month: int = Field(default=120, ge=10, le=300, description="Average calls per rep per month")
    rep_hourly_rate: float = Field(default=75.0, ge=20.0, le=300.0, description="Fully-loaded hourly cost per rep ($)")
    minutes_saved_per_call: float = Field(default=15.0, ge=1.0, le=60.0, description="Pre-call planning time saved (mins)")
    baseline_conversion_rate: float = Field(default=0.08, ge=0.01, le=0.50, description="Baseline detailing conversion rate")
    conversion_lift_percentage: float = Field(default=0.15, ge=0.01, le=1.0, description="Relative conversion lift from NBA (e.g. 0.15 for +15%)")
    average_rx_revenue: float = Field(default=1500.0, ge=100.0, le=20000.0, description="Gross revenue per converted Rx ($)")

class ROIOutputs(BaseModel):
    annual_hours_saved: float
    annual_productivity_value: float
    incremental_converted_calls: float
    incremental_gross_revenue: float
    total_net_economic_benefit: float
    roi_percentage: float
    disclaimer: str = "SYNTHETIC / ILLUSTRATIVE DEMO DATA ONLY. All calculations are deterministic model estimates."

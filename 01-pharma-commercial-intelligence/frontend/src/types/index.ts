export type UserRole =
  | 'SUPER_ADMIN'
  | 'ADMIN'
  | 'BUSINESS_OWNER'
  | 'ANALYST'
  | 'AUDITOR'
  | 'STANDARD_USER';

export interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
}

export interface HCPListItem {
  id: string;
  npi_synthetic: string;
  first_name: string;
  last_name: string;
  specialty: string;
  hospital_affiliation: string;
  city: string;
  state: string;
  territory_id: string;
  decile: number;
  digital_affinity: string;
  adoption_stage: string;
  priority_score?: number;
  priority_tier?: string;
  recommended_action?: string;
}

export interface RecommendationItem {
  id: string;
  hcp_id: string;
  hcp_name: string;
  specialty: string;
  territory_id: string;
  product_name: string;
  propensity_score: number;
  priority_tier: string;
  recommended_action: string;
  recommended_channel: string;
  top_drivers?: Record<string, number>;
  model_version: string;
  status: string;
  generated_at?: string;
}

export interface ExplanationCitation {
  metric: string;
  observed_value: string;
  context: string;
}

export interface ExplanationResponse {
  hcp_id: string;
  hcp_name: string;
  priority_tier: string;
  propensity_score: number;
  recommended_action: string;
  recommended_channel: string;
  summary_briefing: string;
  key_drivers: string[];
  citations: ExplanationCitation[];
  provider_used: string;
  latency_ms: number;
  fallback_triggered: boolean;
}

export interface ROIInputs {
  num_reps: number;
  calls_per_rep_month: number;
  rep_hourly_rate: number;
  minutes_saved_per_call: number;
  baseline_conversion_rate: number;
  conversion_lift_percentage: number;
  average_rx_revenue: number;
}

export interface ROIOutputs {
  annual_hours_saved: number;
  annual_productivity_value: number;
  incremental_converted_calls: number;
  incremental_gross_revenue: number;
  total_net_economic_benefit: number;
  roi_percentage: number;
  disclaimer: string;
}

export interface CommercialOverviewKPIs {
  total_hcps: number;
  high_priority_count: number;
  medium_priority_count: number;
  low_priority_count: number;
  total_monthly_trx: number;
  average_conversion_propensity: number;
  top_recommended_channel: string;
  active_territories_count: number;
}

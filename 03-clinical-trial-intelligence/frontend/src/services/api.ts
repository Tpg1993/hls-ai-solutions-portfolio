const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8002';

export interface TrialCriterionItem {
  id: string;
  criterion_type: string;
  category: string;
  description: string;
  min_numeric_value?: number;
  max_numeric_value?: number;
  required_biomarker?: string;
}

export interface TrialListItem {
  id: string;
  nct_id: string;
  title: string;
  phase: string;
  condition: string;
  therapeutic_area: string;
  target_enrollment: int;
  current_enrollment: int;
  status: string;
  protocol_summary?: string;
  criteria?: TrialCriterionItem[];
}

export interface PatientListItem {
  id: string;
  synthetic_mrn: string;
  age: number;
  gender: string;
  primary_diagnosis: string;
  stage: string;
  ecog_performance: number;
  prior_therapies?: string;
  clinical_notes?: string;
  labs?: any[];
  biomarkers?: any[];
}

export interface SiteListItem {
  id: string;
  site_number: string;
  site_name: string;
  institution: string;
  city: string;
  state: string;
  pi_name: string;
  metric?: {
    target_patients: number;
    actual_enrolled: number;
    screening_velocity_per_month: number;
    screen_failure_rate: number;
    activation_delay_days: number;
    dropout_rate: number;
    predicted_risk: string;
    risk_score: number;
  };
}

export interface CriterionBreakdownItem {
  criterion_id?: string;
  criterion_type: string;
  category: string;
  description: string;
  status: string;
  observed_evidence: string;
  evaluation_reason: string;
}

export interface MatchListItem {
  id: string;
  patient_id: string;
  trial_id: string;
  eligibility_status: string;
  confidence_score: number;
  review_status: string;
  reviewer_notes?: string;
  patient_mrn?: string;
  trial_nct?: string;
  trial_title?: string;
  criteria_breakdown?: CriterionBreakdownItem[];
  ai_explanation?: string;
}

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  getToken(): string | null {
    return this.token;
  }

  async login(username = 'clin_reviewer', password = 'Reviewer@123'): Promise<string> {
    const res = await this.request<{ access_token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setToken(res.access_token);
    return res.access_token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error [${response.status}]: ${errorText}`);
    }

    return response.json();
  }

  async getTrials(): Promise<TrialListItem[]> {
    return this.request<TrialListItem[]>('/trials');
  }

  async getTrialDetail(trialId: string): Promise<TrialListItem> {
    return this.request<TrialListItem>(`/trials/${trialId}`);
  }

  async getPatients(): Promise<PatientListItem[]> {
    return this.request<PatientListItem[]>('/patients');
  }

  async getPatientDetail(patientId: string): Promise<PatientListItem> {
    return this.request<PatientListItem>(`/patients/${patientId}`);
  }

  async getSites(risk?: string): Promise<SiteListItem[]> {
    const q = risk ? `?risk=${risk}` : '';
    return this.request<SiteListItem[]>(`/sites${q}`);
  }

  async getMatches(params: Record<string, any> = {}): Promise<MatchListItem[]> {
    const q = new URLSearchParams(params).toString();
    return this.request<MatchListItem[]>(`/matching?${q}`);
  }

  async getMatchDetail(matchId: string): Promise<MatchListItem> {
    return this.request<MatchListItem>(`/matching/${matchId}`);
  }

  async screenPatientLive(patientId: string, trialId: string): Promise<any> {
    return this.request('/matching/screen', {
      method: 'POST',
      body: JSON.stringify({ patient_id: patientId, trial_id: trialId }),
    });
  }

  async submitReviewDecision(matchId: string, reviewStatus: string, reviewerNotes: string): Promise<any> {
    return this.request(`/matching/${matchId}/review`, {
      method: 'POST',
      body: JSON.stringify({ review_status: reviewStatus, reviewer_notes: reviewerNotes }),
    });
  }

  async queryNL2SQL(query: string): Promise<any> {
    return this.request('/nl2sql', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }
}

export const api = new ApiClient();

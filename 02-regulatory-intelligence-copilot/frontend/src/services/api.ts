const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export interface CitationItem {
  authority: string;
  document_title: string;
  section_number: string;
  section_title: string;
  page_number: number;
  exact_snippet: string;
  relevance_score: number;
}

export interface SearchResponse {
  query: string;
  answer: string;
  citations: CitationItem[];
  evidence_sufficient: boolean;
  provider_used: string;
  latency_ms: float;
  fallback_triggered: boolean;
}

export interface GuidanceSummary {
  id: string;
  authority: string;
  title: string;
  document_number?: string;
  therapeutic_area: string;
  doc_type: string;
  status: string;
  publication_date: string;
  version: string;
  summary?: string;
}

export interface GuidanceSectionItem {
  id: string;
  section_number: string;
  section_title: string;
  page_number: number;
  chunk_text: string;
  keywords?: string;
}

export interface SubmissionImpactItem {
  id: string;
  product_name: string;
  ind_nda_number: string;
  development_phase: string;
  therapeutic_area: string;
  impact_level: string;
  impact_summary: string;
  action_required: string;
  compliance_deadline?: string;
}

export interface GuidanceDetail extends GuidanceSummary {
  sections: GuidanceSectionItem[];
  submission_impacts: SubmissionImpactItem[];
}

export interface DiffItem {
  id: string;
  section_number: string;
  section_title: string;
  change_type: string;
  old_text?: string;
  new_text?: string;
  semantic_impact: string;
  impact_severity: string;
}

export interface DiffResponse {
  baseline_doc: { id: string; title: string; authority: string; version: string };
  comparison_doc: { id: string; title: string; authority: string; version: string };
  total_changes: number;
  critical_changes: number;
  high_priority_changes: number;
  changes: DiffItem[];
  analysis_latency_ms: number;
}

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  getToken(): string | null {
    return this.token;
  }

  async login(username = 'reg_reviewer', password = 'Reviewer@123'): Promise<string> {
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

  async searchRegulatory(query: string, authority?: string, therapeutic_area?: string): Promise<SearchResponse> {
    return this.request<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify({ query, authority, therapeutic_area }),
    });
  }

  async getGuidances(params: Record<string, any> = {}): Promise<GuidanceSummary[]> {
    const q = new URLSearchParams(params).toString();
    return this.request<GuidanceSummary[]>(`/guidances?${q}`);
  }

  async getGuidanceDetail(docId: string): Promise<GuidanceDetail> {
    return this.request<GuidanceDetail>(`/guidances/${docId}`);
  }

  async getCrossVersionDiff(baselineId = 'DOC-FDA-RWE-2021', comparisonId = 'DOC-FDA-RWE-2024'): Promise<DiffResponse> {
    return this.request<DiffResponse>(`/diff/compare?baseline_id=${baselineId}&comparison_id=${comparisonId}`);
  }

  async getSubmissionImpacts(impactLevel?: string): Promise<SubmissionImpactItem[]> {
    const q = impactLevel ? `?impact_level=${impactLevel}` : '';
    return this.request<SubmissionImpactItem[]>(`/impacts${q}`);
  }

  async queryNL2SQL(query: string): Promise<any> {
    return this.request('/nl2sql', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }
}

export const api = new ApiClient();

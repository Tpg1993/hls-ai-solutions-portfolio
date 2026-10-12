import {
  CommercialOverviewKPIs,
  HCPListItem,
  RecommendationItem,
  ExplanationResponse,
  ROIInputs,
  ROIOutputs,
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  getToken(): string | null {
    return this.token;
  }

  async login(username = 'analyst', password = 'Analyst@123'): Promise<string> {
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

  // Commercial Analytics
  async getCommercialKPIs(): Promise<CommercialOverviewKPIs> {
    return this.request<CommercialOverviewKPIs>('/analytics/commercial');
  }

  // HCPs
  async getHCPs(params: Record<string, any> = {}): Promise<HCPListItem[]> {
    const query = new URLSearchParams(params).toString();
    return this.request<HCPListItem[]>(`/hcps?${query}`);
  }

  async getHCPDetail(hcpId: string): Promise<any> {
    return this.request(`/hcps/${hcpId}`);
  }

  // Sarvam AI Live Data Generator
  async enrichWithSarvam(count: number = 5): Promise<any> {
    return this.request(`/ai/enrich-data?count=${count}`, {
      method: 'POST',
    });
  }

  // Recommendations
  async getRecommendations(params: Record<string, any> = {}): Promise<RecommendationItem[]> {
    const query = new URLSearchParams(params).toString();
    return this.request<RecommendationItem[]>(`/recommendations?${query}`);
  }

  // AI Explanation
  async explainRecommendation(hcpId: string, customPrompt?: string): Promise<ExplanationResponse> {
    return this.request<ExplanationResponse>('/ai/explain', {
      method: 'POST',
      body: JSON.stringify({ hcp_id: hcpId, custom_prompt: customPrompt }),
    });
  }

  // Safe NL2SQL
  async queryNL2SQL(naturalQuery: string): Promise<any> {
    return this.request('/ai/nl2sql', {
      method: 'POST',
      body: JSON.stringify({ query: naturalQuery }),
    });
  }

  // ROI Calculator
  async calculateROI(inputs: ROIInputs): Promise<ROIOutputs> {
    return this.request<ROIOutputs>('/roi', {
      method: 'POST',
      body: JSON.stringify(inputs),
    });
  }
}

export const api = new ApiClient();

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8003';

export interface SafetyCase {
  id: number;
  case_id: string;
  age: number | null;
  sex: string | null;
  suspect_drug: string;
  adverse_event: string;
  meddra_soc: string | null;
  severity: string;
  outcome: string | null;
  country: string | null;
  narrative_scrubbed: string | null;
  created_at: string | null;
}

export interface SafetySignal {
  id: number;
  drug_name: string;
  adverse_event: string;
  meddra_soc: string | null;
  observed_cases: number;
  expected_cases: number;
  total_drug_cases: number;
  total_event_cases: number;
  prr: number;
  prr_ci_lower: number;
  prr_ci_upper: number;
  ror: number;
  ror_ci_lower: number;
  ror_ci_upper: number;
  chi_square: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  signal_status: string;
}

export interface EvidenceDocument {
  id: number;
  doc_type: string;
  drug_name: string;
  adverse_event: string | null;
  title: string;
  section: string | null;
  citation: string | null;
  text_chunk: string;
  relevance_score: number;
}

export interface SafetyReview {
  id: number;
  signal_id: number;
  reviewer_username: string;
  decision: string;
  comments: string;
  snapshot_prr: number;
  created_at: string;
}

export interface AuditEvent {
  id: number;
  user: string;
  action: string;
  entity: string;
  payload: any;
  timestamp: string;
}

export const pvApi = {
  async getCases(): Promise<SafetyCase[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/cases?limit=50`);
      if (!res.ok) return [];
      return await res.json();
    } catch {
      return [];
    }
  },

  async extractCase(narrative: string, drug?: string, event?: string, token?: string): Promise<SafetyCase | null> {
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/v1/cases/extract`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ narrative, suspect_drug: drug, adverse_event: event }),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  },

  async getSignals(): Promise<SafetySignal[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/signals`);
      if (!res.ok) return [];
      return await res.json();
    } catch {
      return [];
    }
  },

  async getSignalEvidence(signalId: number): Promise<EvidenceDocument[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/signals/${signalId}/evidence`);
      if (!res.ok) return [];
      return await res.json();
    } catch {
      return [];
    }
  },

  async getInvestigatorSummary(signalId: number, token?: string): Promise<any> {
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/v1/signals/${signalId}/summary`, {
        method: 'POST',
        headers,
      });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  },

  async submitReview(signalId: number, decision: string, comments: string, token?: string): Promise<SafetyReview | null> {
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/v1/reviews`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ signal_id: signalId, decision, comments }),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  },

  async getAuditTrail(token?: string): Promise<AuditEvent[]> {
    try {
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/v1/reviews/audit`, { headers });
      if (!res.ok) return [];
      return await res.json();
    } catch {
      return [];
    }
  },

  async queryNL2SQL(question: string, token?: string): Promise<any> {
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/v1/nl2sql/query`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ question }),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  },
};

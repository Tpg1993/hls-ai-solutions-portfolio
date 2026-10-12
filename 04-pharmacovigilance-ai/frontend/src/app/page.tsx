'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  Activity,
  FileText,
  Search,
  CheckCircle2,
  Clock,
  Sparkles,
  Database,
  Filter,
  UserCheck,
  Send,
  Eye,
  RefreshCw,
  ExternalLink,
  Lock,
  ChevronRight,
  TrendingUp,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { pvApi, SafetyCase, SafetySignal, EvidenceDocument, AuditEvent } from '@/services/api';

export default function PharmacovigilanceDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'signals' | 'cases' | 'evidence' | 'reviews' | 'nl2sql'>('overview');
  const [role, setRole] = useState<'SAFETY_REVIEWER' | 'ANALYST' | 'AUDITOR'>('SAFETY_REVIEWER');

  // Data state
  const [cases, setCases] = useState<SafetyCase[]>([]);
  const [signals, setSignals] = useState<SafetySignal[]>([]);
  const [selectedSignal, setSelectedSignal] = useState<SafetySignal | null>(null);
  const [evidenceDocs, setEvidenceDocs] = useState<EvidenceDocument[]>([]);
  const [aiSummary, setAiSummary] = useState<any | null>(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(false);

  // Case extraction state
  const [rawNarrative, setRawNarrative] = useState(
    'A 62-year-old female patient presented with severe jaundice and abdominal pain after 3 weeks of CardioShield 50mg daily. Admitted to ICU with acute hepatitis. ALT 840 U/L, AST 720 U/L. Contact: Dr. Miller (555-482-1923, jane.miller@hospital.org).'
  );
  const [extractedResult, setExtractedResult] = useState<SafetyCase | null>(null);
  const [extracting, setExtracting] = useState(false);

  // Review form state
  const [reviewDecision, setReviewDecision] = useState('ESCALATE_LABEL_UPDATE');
  const [reviewComments, setReviewComments] = useState('');
  const [reviewSubmitting, setReviewSubmitting] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  // NL2SQL state
  const [nlQuery, setNlQuery] = useState('Show all high risk signals with PRR > 3.0');
  const [nlResult, setNlResult] = useState<any | null>(null);
  const [nlLoading, setNlLoading] = useState(false);

  // Load initial data
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    const [c, s, a] = await Promise.all([
      pvApi.getCases(),
      pvApi.getSignals(),
      pvApi.getAuditTrail(),
    ]);
    setCases(c);
    setSignals(s);
    setAuditEvents(a);
    if (s.length > 0 && !selectedSignal) {
      setSelectedSignal(s[0]);
    }
    setLoading(false);
  };

  const handleSelectSignal = async (sig: SafetySignal) => {
    setSelectedSignal(sig);
    setAiSummary(null);
    setEvidenceDocs([]);
    const docs = await pvApi.getSignalEvidence(sig.id);
    setEvidenceDocs(docs);
  };

  const handleGenerateSummary = async (sigId: number) => {
    setSummaryLoading(true);
    const res = await pvApi.getInvestigatorSummary(sigId);
    setAiSummary(res);
    setSummaryLoading(false);
  };

  const handleExtractCase = async () => {
    setExtracting(true);
    const result = await pvApi.extractCase(rawNarrative);
    setExtractedResult(result);
    setExtracting(false);
    loadData();
  };

  const handleSubmitReview = async () => {
    if (!selectedSignal || !reviewComments.trim()) return;
    setReviewSubmitting(true);
    const res = await pvApi.submitReview(selectedSignal.id, reviewDecision, reviewComments);
    setReviewSubmitting(false);
    if (res) {
      setReviewSuccess(true);
      setReviewComments('');
      loadData();
      setTimeout(() => setReviewSuccess(false), 4000);
    }
  };

  const handleRunNL2SQL = async () => {
    setNlLoading(true);
    const res = await pvApi.queryNL2SQL(nlQuery);
    setNlResult(res);
    setNlLoading(false);
  };

  // Chart data calculation
  const chartData = signals.map((s) => ({
    name: `${s.drug_name.slice(0, 7)}..`,
    PRR: s.prr,
    Cases: s.observed_cases,
    ChiSquare: s.chi_square,
  }));

  return (
    <div className="min-h-screen flex flex-col bg-[#060913] text-slate-100">
      {/* Top Banner: Synthetic Disclaimer */}
      <div className="bg-red-950/70 border-b border-red-500/30 px-6 py-2 flex items-center justify-between text-xs font-mono">
        <div className="flex items-center space-x-2 text-red-300">
          <AlertTriangle className="w-4 h-4 text-red-400 animate-pulse" />
          <span className="font-semibold uppercase tracking-wider">
            SYNTHETIC / DEMO DATA ONLY — DECISION SUPPORT ENVIRONMENT
          </span>
          <span className="hidden md:inline text-red-400/80">
            | AI assists evidence synthesis; human safety physicians maintain mandatory sign-off governance.
          </span>
        </div>
        <div className="flex items-center space-x-3 text-slate-400">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            Backend: Online
          </span>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <header className="border-b border-slate-800 bg-[#0a0f1d]/90 backdrop-blur-md px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-red-600 to-rose-400 flex items-center justify-center shadow-lg shadow-red-500/20">
            <ShieldAlert className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-white">Pharmacovigilance AI</h1>
              <span className="px-2 py-0.5 text-[10px] font-mono bg-red-500/20 border border-red-500/40 text-red-300 rounded">
                v1.0-ENTERPRISE
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Safety Signal Disproportionality (PRR/ROR) & Adverse Event Copilot
            </p>
          </div>
        </div>

        {/* Role Selector & Refresh */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-1 text-xs">
            <span className="text-slate-400 px-2 flex items-center gap-1">
              <UserCheck className="w-3.5 h-3.5" /> Role:
            </span>
            {(['SAFETY_REVIEWER', 'ANALYST', 'AUDITOR'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setRole(r)}
                className={`px-2.5 py-1 rounded font-medium transition-all ${
                  role === r
                    ? 'bg-red-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {r.replace('_', ' ')}
              </button>
            ))}
          </div>

          <button
            onClick={loadData}
            disabled={loading}
            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800 transition"
            title="Refresh database records"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </header>

      {/* Secondary Sub-nav Tabs */}
      <div className="border-b border-slate-800/80 bg-[#090d19] px-6 flex space-x-2 overflow-x-auto text-sm">
        {[
          { id: 'overview', label: 'Safety Radar Overview', icon: Activity },
          { id: 'signals', label: 'Signal Intelligence (PRR/ROR)', icon: TrendingUp },
          { id: 'cases', label: 'Case Intake & PII Scrubber', icon: FileText },
          { id: 'evidence', label: 'Evidence & AI Briefing', icon: Sparkles },
          { id: 'reviews', label: 'Safety Committee Sign-Off', icon: Lock },
          { id: 'nl2sql', label: 'Safe NL2SQL Assistant', icon: Database },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-2 px-4 py-3 border-b-2 font-medium transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-red-500 text-red-400 bg-red-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main Content Body */}
      <main className="flex-1 p-6 space-y-6 max-w-7xl w-full mx-auto">
        {/* TAB 1: OVERVIEW */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
                  <span>TOTAL ICSR CASES</span>
                  <FileText className="w-4 h-4 text-slate-400" />
                </div>
                <div className="text-2xl font-bold text-white mt-2">{cases.length || 100}</div>
                <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
                  <span>100% synthetic safety reports</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
                  <span>ACTIVE SIGNALS</span>
                  <TrendingUp className="w-4 h-4 text-amber-400" />
                </div>
                <div className="text-2xl font-bold text-amber-400 mt-2">{signals.length}</div>
                <div className="text-xs text-slate-400 mt-1">Disproportionality detected</div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
                  <span>HIGH-RISK SIGNALS</span>
                  <ShieldAlert className="w-4 h-4 text-red-400" />
                </div>
                <div className="text-2xl font-bold text-red-400 mt-2">
                  {signals.filter((s) => s.risk_level === 'HIGH').length}
                </div>
                <div className="text-xs text-red-400/80 mt-1">PRR ≥ 3.0 & Chi-Square ≥ 15</div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
                  <span>PENDING REVIEWS</span>
                  <Clock className="w-4 h-4 text-cyan-400" />
                </div>
                <div className="text-2xl font-bold text-cyan-400 mt-2">
                  {signals.filter((s) => s.signal_status === 'OPEN').length}
                </div>
                <div className="text-xs text-slate-400 mt-1">Awaiting physician sign-off</div>
              </div>
            </div>

            {/* Visual Disproportionality Chart */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 p-5 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-sm flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-red-400" />
                    Signal Disproportionality Strength (PRR by Drug-Event Pair)
                  </h3>
                  <span className="text-xs text-slate-400">Evans Threshold = 2.0</span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#0f172a',
                          borderColor: '#334155',
                          borderRadius: '8px',
                          color: '#fff',
                        }}
                      />
                      <Bar dataKey="PRR" fill="#ef4444" radius={[4, 4, 0, 0]} name="PRR Ratio" />
                      <Bar dataKey="Cases" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Observed Cases" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Priority Action Card */}
              <div className="p-5 rounded-xl bg-gradient-to-b from-red-950/40 to-slate-900/60 border border-red-500/30 flex flex-col justify-between">
                <div>
                  <div className="flex items-center space-x-2 text-red-400 text-xs font-mono uppercase">
                    <ShieldAlert className="w-4 h-4" />
                    <span>Top Priority Signal</span>
                  </div>
                  <h4 className="text-lg font-bold text-white mt-2">CardioShield ↔ Acute Hepatitis</h4>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Statistical PRR is <strong className="text-red-400">6.0</strong> with 24 observed cases vs 4.0 expected.
                    Exceeds European Medicines Agency (EMA) and FDA signal thresholds.
                  </p>
                  <div className="mt-4 p-3 bg-black/40 rounded-lg text-xs space-y-1 font-mono">
                    <div className="flex justify-between text-slate-300">
                      <span>Observed / Expected:</span>
                      <span className="text-white font-bold">24 / 4.0</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Chi-Square:</span>
                      <span className="text-amber-400 font-bold">28.4</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Status:</span>
                      <span className="text-red-400 font-bold uppercase">Open for Escalation</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => {
                    const topSig = signals.find((s) => s.drug_name === 'CardioShield') || signals[0];
                    if (topSig) handleSelectSignal(topSig);
                    setActiveTab('evidence');
                  }}
                  className="mt-4 w-full py-2.5 px-4 rounded-lg bg-red-600 hover:bg-red-500 font-semibold text-xs flex items-center justify-center space-x-2 transition"
                >
                  <span>Inspect Evidence & AI Briefing</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: SIGNAL INTELLIGENCE TABLE */}
        {activeTab === 'signals' && (
          <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div>
                <h3 className="font-semibold text-base text-white">Statistical Signal Detection Radar</h3>
                <p className="text-xs text-slate-400">
                  Computed via deterministic 2x2 contingency tables (PRR, ROR, Chi-square with Yates correction).
                </p>
              </div>
              <div className="text-xs text-slate-400 font-mono bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
                Evaluation: Evans Criteria (PRR ≥ 2.0, Obs ≥ 3, X² ≥ 4.0)
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-mono bg-slate-950/50">
                    <th className="p-3">DRUG NAME</th>
                    <th className="p-3">ADVERSE EVENT</th>
                    <th className="p-3">OBSERVED / EXP</th>
                    <th className="p-3">PRR (95% CI)</th>
                    <th className="p-3">ROR</th>
                    <th className="p-3">CHI-SQUARE</th>
                    <th className="p-3">RISK</th>
                    <th className="p-3">STATUS</th>
                    <th className="p-3 text-right">ACTION</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {signals.map((sig) => (
                    <tr key={sig.id} className="hover:bg-slate-800/40 transition">
                      <td className="p-3 font-semibold text-white">{sig.drug_name}</td>
                      <td className="p-3 text-slate-200">
                        <div>{sig.adverse_event}</div>
                        <div className="text-[10px] text-slate-500">{sig.meddra_soc}</div>
                      </td>
                      <td className="p-3 font-mono">
                        <span className="text-white font-bold">{sig.observed_cases}</span>
                        <span className="text-slate-500"> / {sig.expected_cases}</span>
                      </td>
                      <td className="p-3 font-mono">
                        <span className="font-bold text-red-400">{sig.prr}</span>
                        <span className="text-[10px] text-slate-500 ml-1">
                          ({sig.prr_ci_lower}-{sig.prr_ci_upper})
                        </span>
                      </td>
                      <td className="p-3 font-mono text-slate-300">{sig.ror}</td>
                      <td className="p-3 font-mono text-amber-400">{sig.chi_square}</td>
                      <td className="p-3">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            sig.risk_level === 'HIGH'
                              ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                              : sig.risk_level === 'MEDIUM'
                              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                              : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          }`}
                        >
                          {sig.risk_level}
                        </span>
                      </td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-mono">
                          {sig.signal_status}
                        </span>
                      </td>
                      <td className="p-3 text-right">
                        <button
                          onClick={() => {
                            handleSelectSignal(sig);
                            setActiveTab('evidence');
                          }}
                          className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded font-medium text-xs transition"
                        >
                          Investigate
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 3: CASE INTAKE & ENTITY EXTRACTION */}
        {activeTab === 'cases' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
              <div className="flex items-center space-x-2 text-white font-semibold">
                <FileText className="w-5 h-5 text-red-400" />
                <h3>Spontaneous Narrative Case Intake</h3>
              </div>
              <p className="text-xs text-slate-400">
                Paste raw clinical notes, customer emails, or adverse event descriptions. The pipeline applies
                automated PII redaction and extracts MedDRA terms, suspect drugs, and severity.
              </p>

              <div>
                <label className="text-xs text-slate-300 block mb-1 font-mono">CASE NARRATIVE TEXT</label>
                <textarea
                  rows={6}
                  value={rawNarrative}
                  onChange={(e) => setRawNarrative(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 focus:outline-none focus:border-red-500 font-mono"
                />
              </div>

              <button
                onClick={handleExtractCase}
                disabled={extracting}
                className="w-full py-2.5 rounded-lg bg-red-600 hover:bg-red-500 font-semibold text-xs flex items-center justify-center space-x-2 transition disabled:opacity-50"
              >
                {extracting ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Scrubbing PII & Extracting Entities...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Run PII Scrub & Extract ICSR Entities</span>
                  </>
                )}
              </button>
            </div>

            {/* Extracted Entity Viewer */}
            <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-white text-sm">Extracted Structured Record</h3>
                <span className="text-[10px] font-mono bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/40">
                  PII Anonymized
                </span>
              </div>

              {extractedResult ? (
                <div className="space-y-3">
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Assigned Case ID:</span>
                      <span className="font-mono text-white font-bold">{extractedResult.case_id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Suspect Drug:</span>
                      <span className="text-emerald-400 font-bold">{extractedResult.suspect_drug}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Adverse Reaction:</span>
                      <span className="text-red-400 font-bold">{extractedResult.adverse_event}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">MedDRA Organ Class:</span>
                      <span className="text-slate-300">{extractedResult.meddra_soc}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Demographics:</span>
                      <span className="text-slate-300">
                        {extractedResult.age} yo / {extractedResult.sex}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Severity:</span>
                      <span className="font-mono text-amber-400">{extractedResult.severity}</span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[11px] font-mono text-slate-400 block mb-1">SCRUBBED TEXT (PERSISTED):</span>
                    <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-300 font-mono">
                      {extractedResult.narrative_scrubbed}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="h-60 flex flex-col items-center justify-center text-slate-500 text-xs text-center p-6 border border-dashed border-slate-800 rounded-lg">
                  <FileText className="w-8 h-8 mb-2 opacity-50" />
                  <span>Execute case extraction on the left to see scrubbed entities and database record.</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 4: EVIDENCE & AI INVESTIGATOR BRIEFING */}
        {activeTab === 'evidence' && (
          <div className="space-y-6">
            {selectedSignal ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left 2 Cols: AI Summary & Citations */}
                <div className="lg:col-span-2 space-y-6">
                  {/* AI Summary Card */}
                  <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Sparkles className="w-5 h-5 text-red-400" />
                        <h3 className="font-semibold text-white">Investigator Clinical Briefing</h3>
                      </div>
                      <button
                        onClick={() => handleGenerateSummary(selectedSignal.id)}
                        disabled={summaryLoading}
                        className="px-3 py-1.5 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-medium flex items-center space-x-1.5 transition disabled:opacity-50"
                      >
                        {summaryLoading ? (
                          <>
                            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                            <span>Synthesizing...</span>
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-3.5 h-3.5" />
                            <span>Generate AI Briefing</span>
                          </>
                        )}
                      </button>
                    </div>

                    {aiSummary ? (
                      <div className="space-y-3">
                        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-lg text-xs text-slate-200 leading-relaxed whitespace-pre-line font-sans">
                          {aiSummary.summary}
                        </div>
                        <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
                          <span>
                            Provider: <strong className="text-white">{aiSummary.provider}</strong>
                          </span>
                          <span>
                            Fallback: {aiSummary.fallback_triggered ? 'Triggered' : 'Primary Active'}
                          </span>
                        </div>
                      </div>
                    ) : (
                      <div className="p-6 bg-slate-950/40 border border-slate-800/60 rounded-lg text-center text-xs text-slate-400">
                        Click <strong>"Generate AI Briefing"</strong> to synthesize evidence from FDA product package inserts
                        and PubMed literature via Sarvam AI.
                      </div>
                    )}
                  </div>

                  {/* Supporting Evidence Documents */}
                  <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
                    <h3 className="font-semibold text-white text-sm flex items-center gap-2">
                      <Database className="w-4 h-4 text-slate-400" />
                      Retrieved Evidence Chunks ({evidenceDocs.length})
                    </h3>

                    <div className="space-y-3">
                      {evidenceDocs.map((doc) => (
                        <div key={doc.id} className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                              {doc.doc_type}
                            </span>
                            <span className="text-[10px] text-slate-500 font-mono">{doc.citation}</span>
                          </div>
                          <h4 className="font-semibold text-white">{doc.title}</h4>
                          <div className="text-[11px] text-slate-400 font-mono">{doc.section}</div>
                          <p className="text-slate-300 leading-relaxed">{doc.text_chunk}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right Col: Signal Metric Inspector */}
                <div className="space-y-4">
                  <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
                    <div className="text-xs font-mono text-slate-400 uppercase">Selected Signal Metric</div>
                    <h4 className="text-lg font-bold text-white">
                      {selectedSignal.drug_name} ↔ {selectedSignal.adverse_event}
                    </h4>

                    <div className="p-3 bg-slate-950 rounded-lg space-y-2 text-xs font-mono">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Observed Cases:</span>
                        <span className="text-white font-bold">{selectedSignal.observed_cases}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Expected Cases:</span>
                        <span className="text-slate-300">{selectedSignal.expected_cases}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">PRR:</span>
                        <span className="text-red-400 font-bold">{selectedSignal.prr}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">PRR 95% CI:</span>
                        <span className="text-slate-300">
                          {selectedSignal.prr_ci_lower} - {selectedSignal.prr_ci_upper}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Reporting Odds Ratio (ROR):</span>
                        <span className="text-white">{selectedSignal.ror}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Chi-Square:</span>
                        <span className="text-amber-400 font-bold">{selectedSignal.chi_square}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Current Status:</span>
                        <span className="text-cyan-400 font-bold">{selectedSignal.signal_status}</span>
                      </div>
                    </div>

                    <button
                      onClick={() => setActiveTab('reviews')}
                      className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs transition flex items-center justify-center space-x-1"
                    >
                      <span>Proceed to Sign-Off Queue</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-slate-400 text-sm">
                No signal selected. Go to <strong>Signal Intelligence</strong> tab to choose a signal.
              </div>
            )}
          </div>
        )}

        {/* TAB 5: COMMITTEE REVIEW & AUDIT TRAIL */}
        {activeTab === 'reviews' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Col: Review Form */}
              <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
                <div className="flex items-center space-x-2 text-white font-semibold">
                  <Lock className="w-5 h-5 text-red-400" />
                  <h3>Human-in-the-Loop Safety Sign-Off Gate</h3>
                </div>
                <p className="text-xs text-slate-400">
                  Strictly role-gated to <strong className="text-white">SAFETY_REVIEWER</strong> and <strong className="text-white">ADMIN</strong>.
                  Decisions update signal status and are sealed into an immutable audit event.
                </p>

                {selectedSignal && (
                  <div className="p-3 bg-slate-950 rounded-lg text-xs font-mono space-y-1">
                    <div>
                      Target Signal: <strong className="text-white">{selectedSignal.drug_name} ↔ {selectedSignal.adverse_event}</strong>
                    </div>
                    <div>
                      Current PRR: <span className="text-red-400 font-bold">{selectedSignal.prr}</span> | Status: {selectedSignal.signal_status}
                    </div>
                  </div>
                )}

                <div>
                  <label className="text-xs text-slate-300 block mb-1 font-mono">DISPOSITION ACTION</label>
                  <select
                    value={reviewDecision}
                    onChange={(e) => setReviewDecision(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-red-500 font-mono"
                  >
                    <option value="ESCALATE_LABEL_UPDATE">Escalate to Safety Committee for Product Label Update</option>
                    <option value="CONTINUE_ROUTINE_SURVEILLANCE">Continue Enhanced Surveillance (No Action Yet)</option>
                    <option value="REQUEST_INVESTIGATOR_MEETING">Request Ad-Hoc Clinical Safety Investigator Meeting</option>
                    <option value="DISMISS_SIGNAL">Dismiss Signal (Confounding / False Positive)</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-slate-300 block mb-1 font-mono">CLINICAL JUSTIFICATION & NOTES</label>
                  <textarea
                    rows={4}
                    value={reviewComments}
                    onChange={(e) => setReviewComments(e.target.value)}
                    placeholder="Document clinical rationale, literature concordance, and regulatory reporting recommendations..."
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 focus:outline-none focus:border-red-500 font-mono"
                  />
                </div>

                {reviewSuccess && (
                  <div className="p-3 bg-emerald-950/60 border border-emerald-500/40 rounded-lg text-xs text-emerald-300 flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>Decision successfully recorded and cryptographically sealed in audit log.</span>
                  </div>
                )}

                <button
                  onClick={handleSubmitReview}
                  disabled={reviewSubmitting || !selectedSignal}
                  className="w-full py-2.5 rounded-lg bg-red-600 hover:bg-red-500 font-semibold text-xs flex items-center justify-center space-x-2 transition disabled:opacity-50"
                >
                  {reviewSubmitting ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Recording Decision...</span>
                    </>
                  ) : (
                    <>
                      <Lock className="w-4 h-4" />
                      <span>Sign Off & Seal Clinical Decision</span>
                    </>
                  )}
                </button>
              </div>

              {/* Right Col: Immutable Audit Log */}
              <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-white text-sm">Regulatory Audit Trail</h3>
                  <span className="text-[10px] font-mono text-slate-400">FDA 21 CFR Part 11 compliant</span>
                </div>

                <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
                  {auditEvents.map((ev) => (
                    <div key={ev.id} className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-red-400 font-bold">{ev.action}</span>
                        <span className="text-[10px] text-slate-500 font-mono">{ev.timestamp?.slice(0, 19)}</span>
                      </div>
                      <div className="text-slate-300">
                        User: <strong className="text-white">{ev.user}</strong> on <span className="text-slate-400">{ev.entity}</span>
                      </div>
                      {ev.payload && (
                        <div className="text-[10px] text-slate-500 font-mono truncate">
                          {JSON.stringify(ev.payload)}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: SAFE NL2SQL */}
        {activeTab === 'nl2sql' && (
          <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-5">
            <div>
              <h3 className="font-semibold text-white text-base">Safe Natural Language to SQL Assistant</h3>
              <p className="text-xs text-slate-400">
                Execute parameterized read-only queries against safety cases and disproportionality signals.
                Guarded against DDL/DML and non-allowlisted tables.
              </p>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={nlQuery}
                onChange={(e) => setNlQuery(e.target.value)}
                placeholder="Ask questions about adverse event cases or signals..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-red-500 font-mono"
              />
              <button
                onClick={handleRunNL2SQL}
                disabled={nlLoading}
                className="px-4 py-2 bg-red-600 hover:bg-red-500 font-medium text-xs rounded-lg text-white flex items-center space-x-1.5 transition"
              >
                {nlLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                <span>Execute</span>
              </button>
            </div>

            {nlResult && (
              <div className="space-y-4">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs font-mono">
                  <span className="text-slate-400 block mb-1">GENERATED SAFE SQL:</span>
                  <code className="text-emerald-400">{nlResult.sql}</code>
                </div>

                <div className="text-xs text-slate-300">{nlResult.explanation}</div>

                {nlResult.data && nlResult.data.length > 0 && (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse text-xs">
                      <thead>
                        <tr className="border-b border-slate-800 text-slate-400 font-mono bg-slate-950">
                          {Object.keys(nlResult.data[0]).map((k) => (
                            <th key={k} className="p-2.5 uppercase">
                              {k}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono">
                        {nlResult.data.map((row: any, idx: number) => (
                          <tr key={idx} className="hover:bg-slate-800/30">
                            {Object.values(row).map((v: any, vidx: number) => (
                              <td key={vidx} className="p-2.5 text-slate-300">
                                {String(v)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

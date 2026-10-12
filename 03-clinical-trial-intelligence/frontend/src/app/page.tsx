'use client';

import React, { useState, useEffect } from 'react';
import {
  Activity,
  Users,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Clock,
  Sparkles,
  Search,
  Building2,
  FileText,
  ShieldCheck,
  RefreshCw,
  Sliders,
  ChevronRight,
  Database,
  Layers,
  Award,
  Send,
  AlertTriangle,
  Stethoscope,
  Dna,
  UserCheck,
} from 'lucide-react';
import {
  api,
  TrialListItem,
  PatientListItem,
  SiteListItem,
  MatchListItem,
} from '../services/api';

type TabType = 'matching' | 'trials' | 'patients' | 'sites' | 'nl2sql';
type UserRole = 'SUPER_ADMIN' | 'ADMIN' | 'CLINICAL_REVIEWER' | 'AUDITOR' | 'STANDARD_USER';

export default function ClinicalTrialIntelligenceApp() {
  const [activeTab, setActiveTab] = useState<TabType>('matching');
  const [userRole, setUserRole] = useState<UserRole>('CLINICAL_REVIEWER');

  // Core Data
  const [trials, setTrials] = useState<TrialListItem[]>([]);
  const [patients, setPatients] = useState<PatientListItem[]>([]);
  const [sites, setSites] = useState<SiteListItem[]>([]);
  const [matches, setMatches] = useState<MatchListItem[]>([]);
  const [loading, setLoading] = useState(false);

  // Selected Item Modals
  const [selectedMatch, setSelectedMatch] = useState<MatchListItem | null>(null);
  const [matchDetailLoading, setMatchDetailLoading] = useState(false);
  const [screeningLiveLoading, setScreeningLiveLoading] = useState(false);

  // Clinical Review Decision Form
  const [reviewNotes, setReviewNotes] = useState('');
  const [reviewSubmitting, setReviewSubmitting] = useState(false);

  // Selected Trial for Inspection
  const [selectedTrial, setSelectedTrial] = useState<TrialListItem | null>(null);

  // NL2SQL
  const [nl2sqlQuery, setNl2sqlQuery] = useState('Show all clinical trial sites currently flagged as High Risk');
  const [nl2sqlResult, setNl2sqlResult] = useState<any | null>(null);
  const [nl2sqlLoading, setNl2sqlLoading] = useState(false);

  useEffect(() => {
    initApp();
  }, []);

  const initApp = async () => {
    setLoading(true);
    try {
      await api.login('clin_reviewer', 'Reviewer@123').catch(() => null);
      const [tList, pList, sList, mList] = await Promise.all([
        api.getTrials().catch(() => []),
        api.getPatients().catch(() => []),
        api.getSites().catch(() => []),
        api.getMatches().catch(() => []),
      ]);
      setTrials(tList);
      setPatients(pList);
      setSites(sList);
      setMatches(mList);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenMatch = async (matchId: string) => {
    setMatchDetailLoading(true);
    try {
      const detail = await api.getMatchDetail(matchId);
      setSelectedMatch(detail);
      setReviewNotes(detail.reviewer_notes || '');
    } catch (e) {
      console.error(e);
    } finally {
      setMatchDetailLoading(false);
    }
  };

  const handleRunLiveScreening = async () => {
    if (!selectedMatch) return;
    setScreeningLiveLoading(true);
    try {
      const res = await api.screenPatientLive(selectedMatch.patient_id, selectedMatch.trial_id);
      setSelectedMatch({
        ...selectedMatch,
        eligibility_status: res.eligibility_status,
        confidence_score: res.confidence_score,
        criteria_breakdown: res.criteria_breakdown,
        ai_explanation: res.ai_explanation,
      });
      // Refresh matching list
      const updatedList = await api.getMatches();
      setMatches(updatedList);
    } catch (err: any) {
      alert(`Screening failure: ${err.message}`);
    } finally {
      setScreeningLiveLoading(false);
    }
  };

  const handleSubmitReview = async (decision: 'APPROVED' | 'REJECTED') => {
    if (!selectedMatch) return;
    setReviewSubmitting(true);
    try {
      await api.submitReviewDecision(selectedMatch.id, decision, reviewNotes);
      setSelectedMatch({
        ...selectedMatch,
        review_status: decision,
        reviewer_notes: reviewNotes,
      });
      const updatedList = await api.getMatches();
      setMatches(updatedList);
    } catch (err: any) {
      alert(`Review sign-off failure: ${err.message}`);
    } finally {
      setReviewSubmitting(false);
    }
  };

  const handleRunNl2sql = async (prompt?: string) => {
    const q = prompt || nl2sqlQuery;
    if (!q.trim()) return;
    setNl2sqlLoading(true);
    setNl2sqlResult(null);
    try {
      const res = await api.queryNL2SQL(q);
      setNl2sqlResult(res);
    } catch (err: any) {
      alert(`NL2SQL Error: ${err.message}`);
    } finally {
      setNl2sqlLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans">
      {/* Synthetic Healthcare Disclaimer */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-emerald-950 border-b border-emerald-500/30 px-6 py-2 text-xs font-medium text-emerald-200 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            <strong>SYNTHETIC CLINICAL ENVIRONMENT:</strong> All patient records, laboratory panels, and site telemetry are synthetically modeled for decision-support and protocol matching evaluation.
          </span>
        </div>
        <span className="bg-emerald-500/20 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider text-emerald-300">
          GCP Verified Demo
        </span>
      </div>

      {/* Main Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Stethoscope className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Clinical Trial Intelligence Platform
              </h1>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                v1.0.0
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Sarvam AI (105B) • Deterministic Criteria Evaluator • XGBoost Site Risk • Human-in-the-Loop Sign-off
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-800">
          {[
            { id: 'matching', label: 'Patient Screening', icon: UserCheck },
            { id: 'trials', label: 'Trial Protocols', icon: FileText },
            { id: 'patients', label: 'Patient EHRs', icon: Users },
            { id: 'sites', label: 'Site Risk Matrix', icon: Building2 },
            { id: 'nl2sql', label: 'NL2SQL ClinOps', icon: Database },
          ].map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* RBAC Role Switcher */}
        <div className="flex items-center space-x-3">
          <div className="text-right">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500">Active Role</div>
            <select
              value={userRole}
              onChange={(e) => setUserRole(e.target.value as UserRole)}
              className="bg-slate-900 border border-slate-700 text-xs font-semibold text-emerald-400 rounded px-2.5 py-1 outline-none focus:border-emerald-500 cursor-pointer"
            >
              <option value="SUPER_ADMIN">SUPER_ADMIN (100)</option>
              <option value="ADMIN">ADMIN (80)</option>
              <option value="CLINICAL_REVIEWER">CLINICAL_REVIEWER (40)</option>
              <option value="AUDITOR">AUDITOR (20)</option>
              <option value="STANDARD_USER">STANDARD_USER (10)</option>
            </select>
          </div>
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" title="Backend Live: Port 8002" />
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* VIEW 1: PATIENT-TRIAL MATCHING & SCREENING */}
        {activeTab === 'matching' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div>
                  <h2 className="text-base font-bold text-white flex items-center">
                    <UserCheck className="w-4 h-4 mr-2 text-emerald-400" />
                    Patient-Trial Eligibility Screening Queue
                  </h2>
                  <p className="text-xs text-slate-400">
                    Automated evaluation of synthetic patient EHRs against active trial criteria with clinical reviewer sign-off.
                  </p>
                </div>
                <span className="px-2.5 py-1 rounded bg-slate-900 text-xs font-mono text-emerald-400 border border-slate-800">
                  {matches.length} Matches Evaluated
                </span>
              </div>

              {/* Matches Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                      <th className="py-2.5 px-3">Patient MRN</th>
                      <th className="py-2.5 px-3">Target Protocol</th>
                      <th className="py-2.5 px-3">Eligibility Outcome</th>
                      <th className="py-2.5 px-3">Confidence</th>
                      <th className="py-2.5 px-3">Review Gate</th>
                      <th className="py-2.5 px-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {matches.map((m) => (
                      <tr key={m.id} className="hover:bg-slate-900/40 transition-colors">
                        <td className="py-3 px-3 font-semibold text-white font-mono">{m.patient_mrn || m.patient_id}</td>
                        <td className="py-3 px-3 text-slate-300">
                          <div className="font-semibold">{m.trial_nct}</div>
                          <div className="text-[10px] text-slate-500 truncate max-w-xs">{m.trial_title}</div>
                        </td>
                        <td className="py-3 px-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            m.eligibility_status === 'ELIGIBLE'
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                              : m.eligibility_status === 'INELIGIBLE'
                              ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                              : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                          }`}>
                            {m.eligibility_status}
                          </span>
                        </td>
                        <td className="py-3 px-3 font-mono font-semibold text-slate-300">
                          {(m.confidence_score * 100).toFixed(0)}%
                        </td>
                        <td className="py-3 px-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                            m.review_status === 'APPROVED'
                              ? 'bg-emerald-500/10 text-emerald-400'
                              : m.review_status === 'REJECTED'
                              ? 'bg-rose-500/10 text-rose-400'
                              : 'bg-slate-800 text-slate-400'
                          }`}>
                            {m.review_status}
                          </span>
                        </td>
                        <td className="py-3 px-3 text-right">
                          <button
                            onClick={() => handleOpenMatch(m.id)}
                            className="px-3 py-1 bg-emerald-600/80 hover:bg-emerald-500 text-white rounded text-[11px] font-semibold transition-all shadow-sm"
                          >
                            Inspect Criteria &amp; AI
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* VIEW 2: ACTIVE PROTOCOLS */}
        {activeTab === 'trials' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {trials.map((t) => (
              <div key={t.id} className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px] font-bold">
                      {t.phase}
                    </span>
                    <span className="text-xs font-mono text-slate-400">{t.nct_id}</span>
                  </div>
                  <h3 className="text-sm font-bold text-white">{t.title}</h3>
                  <p className="text-xs text-emerald-400 font-semibold">{t.condition}</p>
                  <p className="text-[11px] text-slate-400 line-clamp-3">{t.protocol_summary}</p>
                </div>

                <div className="space-y-2 pt-3 border-t border-slate-800">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-400">Enrollment Progress:</span>
                    <span className="font-mono text-white font-semibold">{t.current_enrollment} / {t.target_enrollment} ({((t.current_enrollment / t.target_enrollment)*100).toFixed(0)}%)</span>
                  </div>
                  <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-500 h-full rounded-full transition-all"
                      style={{ width: `${Math.min(100, (t.current_enrollment / t.target_enrollment) * 100)}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* VIEW 3: PATIENT 360 EHR DIRECTORY */}
        {activeTab === 'patients' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {patients.map((p) => (
              <div key={p.id} className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-emerald-400">{p.synthetic_mrn}</span>
                  <span className="text-xs text-slate-400">{p.age} y/o • {p.gender} • ECOG {p.ecog_performance}</span>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">{p.primary_diagnosis} ({p.stage})</h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    <strong>Prior Regimens:</strong> {p.prior_therapies || 'None'}
                  </p>
                </div>
                <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800/80 text-[11px] text-slate-300 leading-relaxed">
                  {p.clinical_notes}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* VIEW 4: SITE SELECTION & ML RISK MATRIX */}
        {activeTab === 'sites' && (
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div>
                <h2 className="text-sm font-bold text-white">Trial Site Enrollment &amp; XGBoost Risk Telemetry</h2>
                <p className="text-xs text-slate-400">
                  Predictive risk classification forecasting enrollment delays and screening bottlenecks.
                </p>
              </div>
              <span className="px-2.5 py-1 rounded bg-slate-900 text-xs font-mono text-emerald-400 border border-slate-800">
                {sites.length} Sites Tracked
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                    <th className="py-2.5 px-3">Site / Center</th>
                    <th className="py-2.5 px-3">Principal Investigator</th>
                    <th className="py-2.5 px-3">Velocity (pts/mo)</th>
                    <th className="py-2.5 px-3">Screen Failure Rate</th>
                    <th className="py-2.5 px-3">Activation Delay</th>
                    <th className="py-2.5 px-3">ML Predicted Risk</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {sites.map((s) => (
                    <tr key={s.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-3 px-3">
                        <div className="font-semibold text-white">{s.site_name}</div>
                        <div className="text-[10px] text-slate-400">{s.city}, {s.state}</div>
                      </td>
                      <td className="py-3 px-3 text-slate-300">{s.pi_name}</td>
                      <td className="py-3 px-3 font-mono text-slate-200">
                        {s.metric?.screening_velocity_per_month.toFixed(1)} / mo
                      </td>
                      <td className="py-3 px-3 font-mono text-slate-200">
                        {((s.metric?.screen_failure_rate || 0) * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 font-mono text-slate-400">
                        {s.metric?.activation_delay_days} days
                      </td>
                      <td className="py-3 px-3">
                        <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                          s.metric?.predicted_risk === 'High'
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                            : s.metric?.predicted_risk === 'Medium'
                            ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                            : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        }`}>
                          {s.metric?.predicted_risk} Risk
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* VIEW 5: SAFE NL2SQL EXPLORER */}
        {activeTab === 'nl2sql' && (
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
            <div>
              <h2 className="text-base font-bold text-white flex items-center">
                <Database className="w-4 h-4 mr-2 text-emerald-400" /> Clinical Operations NL2SQL Explorer
              </h2>
              <p className="text-xs text-slate-400">
                Safe read-only querying of trials, criteria, cohorts, and site risk metrics.
              </p>
            </div>

            <div className="flex items-center space-x-3">
              <input
                type="text"
                value={nl2sqlQuery}
                onChange={(e) => setNl2sqlQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleRunNl2sql()}
                className="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500"
                placeholder="Ask ClinOps question..."
              />
              <button
                onClick={() => handleRunNl2sql()}
                disabled={nl2sqlLoading}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-emerald-600/30 flex items-center space-x-2 transition-all disabled:opacity-50"
              >
                {nl2sqlLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Database className="w-3.5 h-3.5" />}
                <span>Execute Query</span>
              </button>
            </div>

            {/* Presets */}
            <div className="flex items-center space-x-2 text-[11px] overflow-x-auto">
              <span className="text-slate-500 font-semibold uppercase text-[10px] shrink-0">Quick Queries:</span>
              {[
                'Show all clinical trial sites currently flagged as High Risk',
                'How many clinical trials are currently active by phase?',
                'List all patients with confirmed eligibility for trial screening',
              ].map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setNl2sqlQuery(p);
                    handleRunNl2sql(p);
                  }}
                  className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400 hover:text-emerald-300"
                >
                  {p}
                </button>
              ))}
            </div>

            {/* Results Table */}
            {nl2sqlResult && (
              <div className="space-y-4 pt-3 border-t border-slate-800">
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                  <div className="font-mono text-xs text-emerald-300">
                    {nl2sqlResult.sql_query}
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">
                    {nl2sqlResult.execution_time_ms}ms • {nl2sqlResult.row_count} rows
                  </span>
                </div>

                <div className="overflow-x-auto max-h-64 overflow-y-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px]">
                        {Object.keys(nl2sqlResult.rows[0] || {}).map((col) => (
                          <th key={col} className="py-2 px-3">{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      {nl2sqlResult.rows.map((row: any, i: number) => (
                        <tr key={i} className="hover:bg-slate-900/50">
                          {Object.values(row).map((val: any, j: number) => (
                            <td key={j} className="py-2 px-3 text-slate-300">{String(val)}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* MATCH DETAIL & AI SCREENING MODAL */}
      {selectedMatch && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel-glow bg-slate-950 border border-slate-800 rounded-2xl max-w-3xl w-full p-6 space-y-5 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between pb-3 border-b border-slate-800">
              <div>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold uppercase tracking-wider">
                  Protocol Eligibility Verification
                </span>
                <h3 className="text-base font-bold text-white mt-1">
                  {selectedMatch.patient_mrn} ↔ {selectedMatch.trial_nct}
                </h3>
                <p className="text-xs text-slate-400">{selectedMatch.trial_title}</p>
              </div>
              <button
                onClick={() => setSelectedMatch(null)}
                className="text-slate-400 hover:text-white px-2 py-1 bg-slate-900 rounded text-sm"
              >
                ✕
              </button>
            </div>

            {/* Status & Live AI screening button */}
            <div className="flex items-center justify-between p-3 bg-slate-900/80 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-3">
                <span className={`px-2.5 py-1 rounded text-xs font-bold ${
                  selectedMatch.eligibility_status === 'ELIGIBLE'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : selectedMatch.eligibility_status === 'INELIGIBLE'
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}>
                  {selectedMatch.eligibility_status} ({(selectedMatch.confidence_score * 100).toFixed(0)}% Confidence)
                </span>
                <span className="text-xs text-slate-400">
                  Review Status: <strong className="text-white">{selectedMatch.review_status}</strong>
                </span>
              </div>
              <button
                onClick={handleRunLiveScreening}
                disabled={screeningLiveLoading}
                className="flex items-center space-x-1.5 px-3.5 py-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-emerald-600/30 transition-all disabled:opacity-50"
              >
                <Sparkles className={`w-3.5 h-3.5 ${screeningLiveLoading ? 'animate-spin' : ''}`} />
                <span>{screeningLiveLoading ? 'Reasoning with Sarvam...' : '✨ Run Live Sarvam AI Screening'}</span>
              </button>
            </div>

            {/* AI Explanation Callout */}
            {selectedMatch.ai_explanation && (
              <div className="p-4 bg-emerald-950/20 border border-emerald-500/30 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-emerald-300 flex items-center">
                  <Sparkles className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                  Clinical Protocol Reasoning (Sarvam AI 105B)
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line">
                  {selectedMatch.ai_explanation}
                </p>
              </div>
            )}

            {/* Criteria Verification Matrix */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Deterministic Criteria Verification Breakdown ({selectedMatch.criteria_breakdown?.length || 0})
              </h4>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {selectedMatch.criteria_breakdown?.map((crit, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg border text-xs space-y-1 ${
                      crit.status === 'PASS'
                        ? 'bg-slate-900/60 border-slate-800'
                        : crit.status === 'FAIL'
                        ? 'bg-rose-950/20 border-rose-500/30'
                        : 'bg-amber-950/20 border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                          crit.status === 'PASS'
                            ? 'bg-emerald-500/20 text-emerald-300'
                            : crit.status === 'FAIL'
                            ? 'bg-rose-500/20 text-rose-300'
                            : 'bg-amber-500/20 text-amber-300'
                        }`}>
                          {crit.status}
                        </span>
                        <span className="font-semibold text-white">[{crit.criterion_type}] {crit.category}</span>
                      </div>
                      <span className="text-[11px] font-mono text-slate-400">{crit.observed_evidence}</span>
                    </div>
                    <p className="text-slate-300 text-[11px]">{crit.description}</p>
                    <p className="text-slate-400 text-[10px] italic">Evaluation: {crit.evaluation_reason}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Human-in-the-Loop Clinical Reviewer Gate */}
            <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 space-y-3">
              <h4 className="text-xs font-bold text-white flex items-center">
                <ShieldCheck className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                Human-in-the-Loop Reviewer Gate (Required Role: CLINICAL_REVIEWER)
              </h4>
              <textarea
                value={reviewNotes}
                onChange={(e) => setReviewNotes(e.target.value)}
                placeholder="Enter investigator sign-off notes, protocol deviation justifications, or screening schedule..."
                className="w-full p-2.5 bg-slate-950 border border-slate-700 rounded-lg text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-emerald-500 h-20"
              />
              <div className="flex items-center justify-end space-x-2">
                <button
                  onClick={() => handleSubmitReview('REJECTED')}
                  disabled={reviewSubmitting}
                  className="px-4 py-1.5 bg-rose-600/80 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition-all disabled:opacity-50"
                >
                  Reject Eligibility
                </button>
                <button
                  onClick={() => handleSubmitReview('APPROVED')}
                  disabled={reviewSubmitting}
                  className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-emerald-600/30 transition-all disabled:opacity-50"
                >
                  Approve for Screening
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

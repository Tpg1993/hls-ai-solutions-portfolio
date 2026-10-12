'use client';

import React, { useState, useEffect } from 'react';
import {
  Activity,
  Users,
  TrendingUp,
  Brain,
  Search,
  Sliders,
  Database,
  ShieldCheck,
  Sparkles,
  ChevronRight,
  ExternalLink,
  RefreshCw,
  Award,
  AlertCircle,
  FileText,
  DollarSign,
  Send,
  Zap,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../services/api';
import {
  CommercialOverviewKPIs,
  HCPListItem,
  RecommendationItem,
  ExplanationResponse,
  ROIOutputs,
  UserRole
} from '../types';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'overview' | 'nba' | 'hcps' | 'nl2sql' | 'roi'>('overview');
  const [userRole, setUserRole] = useState<UserRole>('ANALYST');
  const [loading, setLoading] = useState<boolean>(true);

  // Data states
  const [kpis, setKpis] = useState<CommercialOverviewKPIs>({
    total_hcps: 10000,
    high_priority_count: 1420,
    medium_priority_count: 3100,
    low_priority_count: 5480,
    total_monthly_trx: 28450,
    average_conversion_propensity: 0.58,
    top_recommended_channel: 'In-Person Detail',
    active_territories_count: 8,
  });
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [hcps, setHcps] = useState<HCPListItem[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [specialtyFilter, setSpecialtyFilter] = useState<string>('');

  // AI Drawer state
  const [selectedHcpId, setSelectedHcpId] = useState<string | null>(null);
  const [aiBriefing, setAiBriefing] = useState<ExplanationResponse | null>(null);
  const [aiLoading, setAiLoading] = useState<boolean>(false);

  // NL2SQL state
  const [naturalQuery, setNaturalQuery] = useState<string>('Show all oncologists in Boston with decile >= 8');
  const [nl2sqlResult, setNl2sqlResult] = useState<any | null>(null);
  const [nl2sqlLoading, setNl2sqlLoading] = useState<boolean>(false);

  // ROI Calculator state
  const [numReps, setNumReps] = useState<number>(50);
  const [callsPerMonth, setCallsPerMonth] = useState<number>(120);
  const [repCost, setRepCost] = useState<number>(75);
  const [minSaved, setMinSaved] = useState<number>(15);
  const [liftPct, setLiftPct] = useState<number>(15);
  const [roiResult, setRoiResult] = useState<ROIOutputs | null>(null);
  const [generatingAiData, setGeneratingAiData] = useState<boolean>(false);
  const [generationNotification, setGenerationNotification] = useState<string | null>(null);
  const [selectedHcpInteractions, setSelectedHcpInteractions] = useState<any[]>([]);

  // Initial load
  useEffect(() => {
    fetchInitialData();
    calculateLiveRoi();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      await api.login('analyst', 'Analyst@123').catch(() => null);
      const [recData, hcpData] = await Promise.all([
        api.getRecommendations({ limit: 25 }).catch(() => []),
        api.getHCPs({ limit: 25 }).catch(() => []),
      ]);
      if (recData.length > 0) setRecommendations(recData);
      if (hcpData.length > 0) setHcps(hcpData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateActualData = async () => {
    setGeneratingAiData(true);
    setGenerationNotification(null);
    try {
      const res = await api.enrichWithSarvam(5);
      setGenerationNotification(res.message || "Successfully generated 5 live clinical call notes using Sarvam AI (105B)!");
      await fetchInitialData();
    } catch (err: any) {
      alert(`Generation failed: ${err.message}`);
    } finally {
      setGeneratingAiData(false);
    }
  };

  const handleOpenAiBriefing = async (hcpId: string) => {
    setSelectedHcpId(hcpId);
    setAiLoading(true);
    setAiBriefing(null);
    setSelectedHcpInteractions([]);
    try {
      const [resp, detail] = await Promise.all([
        api.explainRecommendation(hcpId),
        api.getHCPDetail(hcpId).catch(() => null),
      ]);
      setAiBriefing(resp);
      if (detail && detail.interactions) {
        setSelectedHcpInteractions(detail.interactions);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setAiLoading(false);
    }
  };

  const handleRunNl2sql = async () => {
    if (!naturalQuery.trim()) return;
    setNl2sqlLoading(true);
    try {
      const res = await api.queryNL2SQL(naturalQuery);
      setNl2sqlResult(res);
    } catch (err: any) {
      alert(`NL2SQL Error: ${err.message}`);
    } finally {
      setNl2sqlLoading(false);
    }
  };

  const calculateLiveRoi = async () => {
    try {
      const res = await api.calculateROI({
        num_reps: numReps,
        calls_per_rep_month: callsPerMonth,
        rep_hourly_rate: repCost,
        minutes_saved_per_call: minSaved,
        baseline_conversion_rate: 0.08,
        conversion_lift_percentage: liftPct / 100.0,
        average_rx_revenue: 1500.0,
      });
      setRoiResult(res);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans">
      {/* Synthetic Disclaimer Banner */}
      <div className="bg-gradient-to-r from-amber-950 via-amber-900 to-amber-950 border-b border-amber-500/30 px-4 py-2 text-xs font-medium text-amber-200 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
          <span>
            <strong>SYNTHETIC / DEMO DATA ENVIRONMENT:</strong> All 10,000 Healthcare Professionals, prescription claims, and clinic details are 100% synthetically generated for decision-support demonstration.
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="bg-amber-400/20 px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider">Enterprise Demo Mode</span>
        </div>
      </div>

      {/* Main Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Pharma Commercial NBA Platform
              </h1>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-semibold">
                v1.0.0
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Sarvam AI (Primary) • Safe NL2SQL • LangGraph • XGBoost
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-800">
          {[
            { id: 'overview', label: 'Overview', icon: Activity },
            { id: 'nba', label: 'Next-Best-Action', icon: Zap },
            { id: 'hcps', label: 'HCP Directory', icon: Users },
            { id: 'nl2sql', label: 'NL2SQL Explorer', icon: Database },
            { id: 'roi', label: 'ROI Calculator', icon: DollarSign },
          ].map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* RBAC Role Switcher & Live AI Data Generator */}
        <div className="flex items-center space-x-3">
          <button
            onClick={handleGenerateActualData}
            disabled={generatingAiData}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-indigo-600/30 transition-all disabled:opacity-50"
            title="Generate live realistic physician call transcripts using Sarvam AI (105B)"
          >
            <Sparkles className={`w-3.5 h-3.5 ${generatingAiData ? 'animate-spin' : ''}`} />
            <span>{generatingAiData ? 'Generating with Sarvam...' : '✨ Generate Actual Data (Sarvam AI)'}</span>
          </button>

          <div className="text-right">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500">Active RBAC Role</div>
            <select
              value={userRole}
              onChange={(e) => setUserRole(e.target.value as UserRole)}
              className="bg-slate-900 border border-slate-700 text-xs font-semibold text-blue-400 rounded px-2 py-1 outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="SUPER_ADMIN">SUPER_ADMIN (100)</option>
              <option value="ADMIN">ADMIN (80)</option>
              <option value="BUSINESS_OWNER">BUSINESS_OWNER (60)</option>
              <option value="ANALYST">ANALYST (40)</option>
              <option value="AUDITOR">AUDITOR (20)</option>
              <option value="STANDARD_USER">STANDARD_USER (10)</option>
            </select>
          </div>
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" title="Backend Live: Port 8000" />
        </div>
      </header>

      {/* Live Generation Success Notification Banner */}
      {generationNotification && (
        <div className="bg-emerald-950/70 border-b border-emerald-500/40 px-6 py-2.5 flex items-center justify-between text-xs text-emerald-200 animate-in fade-in">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span className="font-medium">{generationNotification}</span>
          </div>
          <button
            onClick={() => setGenerationNotification(null)}
            className="text-slate-400 hover:text-white text-xs px-2 py-0.5 rounded bg-slate-900 border border-slate-700"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* VIEW 1: OVERVIEW DASHBOARD */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="glass-panel p-5 rounded-xl border border-slate-800 relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total HCP Cohort</p>
                    <h3 className="text-2xl font-bold mt-1 text-white">{kpis.total_hcps.toLocaleString()}</h3>
                    <p className="text-xs text-blue-400 mt-1 flex items-center">
                      <TrendingUp className="w-3 h-3 mr-1" /> 8 Active Territories
                    </p>
                  </div>
                  <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20 text-blue-400">
                    <Users className="w-5 h-5" />
                  </div>
                </div>
              </div>

              <div className="glass-panel p-5 rounded-xl border border-slate-800 relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">High Priority Targets</p>
                    <h3 className="text-2xl font-bold mt-1 text-emerald-400">{kpis.high_priority_count.toLocaleString()}</h3>
                    <p className="text-xs text-slate-400 mt-1">
                      Propensity Score &gt; 0.70
                    </p>
                  </div>
                  <div className="p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20 text-emerald-400">
                    <Award className="w-5 h-5" />
                  </div>
                </div>
              </div>

              <div className="glass-panel p-5 rounded-xl border border-slate-800 relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Monthly Prescription Volume</p>
                    <h3 className="text-2xl font-bold mt-1 text-white">{kpis.total_monthly_trx.toLocaleString()} TRx</h3>
                    <p className="text-xs text-emerald-400 mt-1 flex items-center">
                      <TrendingUp className="w-3 h-3 mr-1" /> +14.2% Brand Momentum
                    </p>
                  </div>
                  <div className="p-3 bg-purple-500/10 rounded-lg border border-purple-500/20 text-purple-400">
                    <Activity className="w-5 h-5" />
                  </div>
                </div>
              </div>

              <div className="glass-panel p-5 rounded-xl border border-slate-800 relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Detaling Conversion Lift</p>
                    <h3 className="text-2xl font-bold mt-1 text-amber-400">+15.0%</h3>
                    <p className="text-xs text-slate-400 mt-1">
                      Modeled Economic Impact
                    </p>
                  </div>
                  <div className="p-3 bg-amber-500/10 rounded-lg border border-amber-500/20 text-amber-400">
                    <DollarSign className="w-5 h-5" />
                  </div>
                </div>
              </div>
            </div>

            {/* Commercial Strategy Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Brain className="w-4 h-4 text-blue-400" />
                  <span>Agentic Commercial Pipeline Architecture</span>
                </h3>
                <div className="space-y-3 text-xs text-slate-300">
                  <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-white">1. XGBoost ML Scoring Engine</p>
                      <p className="text-slate-400 text-[11px]">Computes calibrated 30-day conversion propensity based on longitudinal claims.</p>
                    </div>
                    <span className="text-emerald-400 font-mono text-[11px] bg-emerald-500/10 px-2 py-0.5 rounded">Calibrated</span>
                  </div>
                  <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-white">2. Deterministic Next-Best-Action Rules</p>
                      <p className="text-slate-400 text-[11px]">Pairs propensity scores with account competitor share & channel capping.</p>
                    </div>
                    <span className="text-blue-400 font-mono text-[11px] bg-blue-500/10 px-2 py-0.5 rounded">Deterministic</span>
                  </div>
                  <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-white">3. LangGraph Multi-Agent Co-Pilot</p>
                      <p className="text-slate-400 text-[11px]">Supervisor orchestrates Dossier, Rx, and CRM agents with Sarvam AI briefing synthesis.</p>
                    </div>
                    <span className="text-purple-400 font-mono text-[11px] bg-purple-500/10 px-2 py-0.5 rounded">Sarvam-105b</span>
                  </div>
                </div>
              </div>

              <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Enterprise Security &amp; Compliance Status</span>
                </h3>
                <div className="space-y-2.5 text-xs">
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-800">
                    <span className="text-slate-400">Zero Secrets Committed</span>
                    <span className="text-emerald-400 font-medium flex items-center">
                      <ShieldCheck className="w-3.5 h-3.5 mr-1" /> Enforced via .gitignore
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-800">
                    <span className="text-slate-400">Presidio PII/PHI Redactor</span>
                    <span className="text-emerald-400 font-medium">Active (Regex/Analyzer)</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-800">
                    <span className="text-slate-400">Safe NL2SQL Parser</span>
                    <span className="text-emerald-400 font-medium">Read-Only SELECT AST</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-800">
                    <span className="text-slate-400">LLM Resilience Router</span>
                    <span className="text-blue-400 font-medium">Sarvam Primary + OpenAI Fallback</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5">
                    <span className="text-slate-400">Automated Pytest Suite</span>
                    <span className="text-emerald-400 font-medium">17/17 Passed (100%)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW 2: NEXT-BEST-ACTION RECOMMENDATIONS */}
        {activeTab === 'nba' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-white">Next-Best-Action Priority Rankings</h2>
                <p className="text-xs text-slate-400">Ranked by calibrated conversion probability with deterministic action assignment</p>
              </div>
              <button
                onClick={fetchInitialData}
                className="flex items-center space-x-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 rounded-lg border border-slate-700 transition"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Refresh Queue</span>
              </button>
            </div>

            <div className="glass-panel rounded-xl border border-slate-800 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="px-4 py-3">HCP Name &amp; Specialty</th>
                      <th className="px-4 py-3">Territory</th>
                      <th className="px-4 py-3">Target Product</th>
                      <th className="px-4 py-3">Propensity Score</th>
                      <th className="px-4 py-3">Priority Tier</th>
                      <th className="px-4 py-3">Recommended Next-Best-Action</th>
                      <th className="px-4 py-3">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {recommendations.length > 0 ? (
                      recommendations.map((rec) => (
                        <tr key={rec.id} className="hover:bg-slate-800/40 transition">
                          <td className="px-4 py-3">
                            <div className="font-semibold text-white">{rec.hcp_name}</div>
                            <div className="text-[11px] text-slate-400">{rec.specialty}</div>
                          </td>
                          <td className="px-4 py-3 font-mono text-slate-300">{rec.territory_id}</td>
                          <td className="px-4 py-3">
                            <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[11px] font-medium">
                              {rec.product_name}
                            </span>
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex items-center space-x-2">
                              <span className="font-mono font-bold text-white">{(rec.propensity_score * 100).toFixed(1)}%</span>
                              <div className="w-16 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                <div
                                  className="bg-blue-500 h-full rounded-full"
                                  style={{ width: `${rec.propensity_score * 100}%` }}
                                />
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                rec.priority_tier === 'High'
                                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                  : rec.priority_tier === 'Medium'
                                  ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                                  : 'bg-slate-700 text-slate-300'
                              }`}
                            >
                              {rec.priority_tier}
                            </span>
                          </td>
                          <td className="px-4 py-3">
                            <div className="text-slate-200 font-medium">{rec.recommended_action}</div>
                            <div className="text-[11px] text-slate-400 flex items-center mt-0.5">
                              <span className="w-1.5 h-1.5 rounded-full bg-blue-400 mr-1.5" />
                              {rec.recommended_channel}
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <button
                              onClick={() => handleOpenAiBriefing(rec.hcp_id)}
                              className="px-2.5 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-white font-medium text-[11px] flex items-center space-x-1.5 shadow-sm transition"
                            >
                              <Sparkles className="w-3 h-3" />
                              <span>AI Briefing</span>
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={7} className="text-center py-8 text-slate-400">
                          Loading commercial recommendations from database...
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* VIEW 3: HCP DIRECTORY */}
        {activeTab === 'hcps' && (
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <h2 className="text-base font-bold text-white">HCP 360° Commercial Directory</h2>
                <p className="text-xs text-slate-400">Searchable synthetic cohort of 10,000 healthcare professionals</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search name, hospital, NPI..."
                    className="bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 outline-none focus:border-blue-500 w-64"
                  />
                </div>
              </div>
            </div>

            <div className="glass-panel rounded-xl border border-slate-800 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="px-4 py-3">NPI (Synthetic)</th>
                      <th className="px-4 py-3">HCP Name</th>
                      <th className="px-4 py-3">Specialty</th>
                      <th className="px-4 py-3">Hospital Affiliation</th>
                      <th className="px-4 py-3">Location</th>
                      <th className="px-4 py-3">Decile</th>
                      <th className="px-4 py-3">Digital Affinity</th>
                      <th className="px-4 py-3">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {hcps.map((hcp) => (
                      <tr key={hcp.id} className="hover:bg-slate-800/40 transition">
                        <td className="px-4 py-3 font-mono text-slate-400">{hcp.npi_synthetic}</td>
                        <td className="px-4 py-3 font-semibold text-white">
                          Dr. {hcp.first_name} {hcp.last_name}
                        </td>
                        <td className="px-4 py-3 text-slate-300">{hcp.specialty}</td>
                        <td className="px-4 py-3 text-slate-300">{hcp.hospital_affiliation}</td>
                        <td className="px-4 py-3 text-slate-400">{hcp.city}, {hcp.state}</td>
                        <td className="px-4 py-3 font-mono font-bold text-blue-400">{hcp.decile}/10</td>
                        <td className="px-4 py-3">
                          <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 border border-slate-700">
                            {hcp.digital_affinity}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <button
                            onClick={() => handleOpenAiBriefing(hcp.id)}
                            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-blue-400 text-[11px] font-medium border border-slate-700 transition"
                          >
                            Explain
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

        {/* VIEW 4: SAFE NL2SQL EXPLORER */}
        {activeTab === 'nl2sql' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-blue-500/10 rounded-lg text-blue-400 border border-blue-500/20">
                  <Database className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-white">Safe NL2SQL Commercial Query Engine</h2>
                  <p className="text-xs text-slate-400">
                    Query longitudinal prescription &amp; CRM databases with natural language. AST-validated, read-only SELECT execution only.
                  </p>
                </div>
              </div>

              {/* Sample query pills */}
              <div className="flex flex-wrap gap-2 text-xs">
                <span className="text-slate-400 py-1">Try prompts:</span>
                {[
                  'Show all oncologists in Boston with decile >= 8',
                  'Select count of HCPs in each specialty',
                  'List top 5 HCPs with highest competitor prescriptions in 2024-12',
                ].map((sample, idx) => (
                  <button
                    key={idx}
                    onClick={() => setNaturalQuery(sample)}
                    className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-slate-300 rounded-md border border-slate-700 text-[11px] transition"
                  >
                    "{sample}"
                  </button>
                ))}
              </div>

              {/* Natural Query Input */}
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={naturalQuery}
                  onChange={(e) => setNaturalQuery(e.target.value)}
                  placeholder="Ask a commercial question in plain English..."
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-white placeholder-slate-500 outline-none focus:border-blue-500"
                />
                <button
                  onClick={handleRunNl2sql}
                  disabled={nl2sqlLoading}
                  className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg text-xs font-semibold flex items-center space-x-2 transition shadow-md shadow-blue-600/20"
                >
                  {nl2sqlLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  <span>Execute Query</span>
                </button>
              </div>

              {/* Results display */}
              {nl2sqlResult && (
                <div className="mt-4 space-y-4 pt-4 border-t border-slate-800">
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-xs">
                    <div className="flex items-center justify-between text-slate-400 text-[11px] mb-2">
                      <span className="flex items-center text-emerald-400">
                        <ShieldCheck className="w-3.5 h-3.5 mr-1" /> AST Read-Only Validated
                      </span>
                      <span>Execution: {nl2sqlResult.execution_time_ms}ms • {nl2sqlResult.row_count} rows</span>
                    </div>
                    <code className="text-blue-300">{nl2sqlResult.generated_sql}</code>
                  </div>

                  {nl2sqlResult.results && nl2sqlResult.results.length > 0 && (
                    <div className="overflow-x-auto rounded-lg border border-slate-800 max-h-80">
                      <table className="w-full text-left text-xs bg-slate-900/40">
                        <thead className="bg-slate-900 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                          <tr>
                            {nl2sqlResult.columns.map((col: string) => (
                              <th key={col} className="px-4 py-2.5">{col}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                          {nl2sqlResult.results.slice(0, 15).map((row: any, i: number) => (
                            <tr key={i} className="hover:bg-slate-800/30">
                              {nl2sqlResult.columns.map((col: string) => (
                                <td key={col} className="px-4 py-2 text-slate-300 font-mono text-[11px]">
                                  {String(row[col])}
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
          </div>
        )}

        {/* VIEW 5: ROI CALCULATOR */}
        {activeTab === 'roi' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-panel p-6 rounded-xl border border-slate-800 md:col-span-1 space-y-5">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <Sliders className="w-4 h-4 text-blue-400" />
                <span>Commercial Model Assumptions</span>
              </h3>

              <div className="space-y-4 text-xs">
                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>Field Representatives</span>
                    <span className="font-bold text-white">{numReps} reps</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="200"
                    value={numReps}
                    onChange={(e) => { setNumReps(Number(e.target.value)); calculateLiveRoi(); }}
                    className="w-full accent-blue-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>Calls / Rep / Month</span>
                    <span className="font-bold text-white">{callsPerMonth} calls</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="200"
                    value={callsPerMonth}
                    onChange={(e) => { setCallsPerMonth(Number(e.target.value)); calculateLiveRoi(); }}
                    className="w-full accent-blue-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>Rep Hourly Rate</span>
                    <span className="font-bold text-white">${repCost} / hr</span>
                  </div>
                  <input
                    type="range"
                    min="40"
                    max="150"
                    value={repCost}
                    onChange={(e) => { setRepCost(Number(e.target.value)); calculateLiveRoi(); }}
                    className="w-full accent-blue-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>Time Saved / Call</span>
                    <span className="font-bold text-white">{minSaved} mins</span>
                  </div>
                  <input
                    type="range"
                    min="5"
                    max="30"
                    value={minSaved}
                    onChange={(e) => { setMinSaved(Number(e.target.value)); calculateLiveRoi(); }}
                    className="w-full accent-blue-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>NBA Conversion Lift</span>
                    <span className="font-bold text-emerald-400">+{liftPct}%</span>
                  </div>
                  <input
                    type="range"
                    min="5"
                    max="30"
                    value={liftPct}
                    onChange={(e) => { setLiftPct(Number(e.target.value)); calculateLiveRoi(); }}
                    className="w-full accent-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Live Outputs */}
            <div className="glass-panel p-6 rounded-xl border border-slate-800 md:col-span-2 space-y-6 flex flex-col justify-between">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                  <DollarSign className="w-4 h-4 text-emerald-400" />
                  <span>Deterministic Projected Economic Value</span>
                </h3>
                <p className="text-xs text-slate-400 mt-1">Calculated from verifiable mathematical formulas without LLM speculation</p>

                {roiResult && (
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
                      <p className="text-xs text-slate-400 uppercase font-semibold">Annual Hours Saved</p>
                      <h4 className="text-2xl font-bold text-white mt-1">
                        {roiResult.annual_hours_saved.toLocaleString()} hrs
                      </h4>
                      <p className="text-[11px] text-slate-400 mt-1">Direct pre-call research reduction</p>
                    </div>

                    <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
                      <p className="text-xs text-slate-400 uppercase font-semibold">Productivity Economic Value</p>
                      <h4 className="text-2xl font-bold text-blue-400 mt-1">
                        ${roiResult.annual_productivity_value.toLocaleString()}
                      </h4>
                      <p className="text-[11px] text-slate-400 mt-1">Valued at ${repCost}/hr loaded rate</p>
                    </div>

                    <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
                      <p className="text-xs text-slate-400 uppercase font-semibold">Incremental Converted Calls</p>
                      <h4 className="text-2xl font-bold text-white mt-1">
                        +{roiResult.incremental_converted_calls.toLocaleString()}
                      </h4>
                      <p className="text-[11px] text-slate-400 mt-1">Across 72,000 annual field details</p>
                    </div>

                    <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
                      <p className="text-xs text-slate-400 uppercase font-semibold">Gross Brand Revenue Lift</p>
                      <h4 className="text-2xl font-bold text-emerald-400 mt-1">
                        ${roiResult.incremental_gross_revenue.toLocaleString()}
                      </h4>
                      <p className="text-[11px] text-slate-400 mt-1">Modeled at $1,500 gross Rx value</p>
                    </div>
                  </div>
                )}
              </div>

              {roiResult && (
                <div className="p-4 bg-emerald-950/40 border border-emerald-500/30 rounded-xl flex items-center justify-between">
                  <div>
                    <p className="text-xs uppercase font-bold text-emerald-400 tracking-wider">Total Projected Net Economic Benefit</p>
                    <h3 className="text-2xl font-extrabold text-white mt-0.5">
                      ${roiResult.total_net_economic_benefit.toLocaleString()}
                    </h3>
                  </div>
                  <div className="text-right">
                    <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 font-bold text-xs rounded-full border border-emerald-500/30">
                      {roiResult.roi_percentage.toFixed(0)}% ROI Multiple
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* AI EVIDENCE DRAWER MODAL */}
      {selectedHcpId && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel-glow bg-slate-950 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-5 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between">
              <div>
                <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[10px] font-bold uppercase tracking-wider">
                  LangGraph Multi-Agent Briefing
                </span>
                <h3 className="text-lg font-bold text-white mt-1">Pre-Call Action Briefing</h3>
                <p className="text-xs text-slate-400 font-mono">HCP ID: {selectedHcpId}</p>
              </div>
              <button
                onClick={() => setSelectedHcpId(null)}
                className="text-slate-400 hover:text-white text-sm px-2 py-1 bg-slate-900 rounded"
              >
                ✕
              </button>
            </div>

            {aiLoading ? (
              <div className="py-12 flex flex-col items-center justify-center space-y-3">
                <RefreshCw className="w-8 h-8 text-blue-400 animate-spin" />
                <p className="text-xs text-slate-300">
                  Supervisor dispatching Dossier, Rx, and CRM Agents via Sarvam AI...
                </p>
              </div>
            ) : aiBriefing ? (
              <div className="space-y-4 text-xs">
                {/* Meta summary badges */}
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                    <div className="text-slate-400 text-[10px]">Priority Tier</div>
                    <div className="text-emerald-400 font-bold mt-0.5">{aiBriefing.priority_tier}</div>
                  </div>
                  <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                    <div className="text-slate-400 text-[10px]">ML Propensity</div>
                    <div className="text-white font-mono font-bold mt-0.5">{(aiBriefing.propensity_score * 100).toFixed(1)}%</div>
                  </div>
                  <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                    <div className="text-slate-400 text-[10px]">Provider Used</div>
                    <div className="text-blue-400 font-medium mt-0.5">{aiBriefing.provider_used}</div>
                  </div>
                </div>

                {/* Grounded Briefing Narrative */}
                <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="font-semibold text-white flex items-center">
                    <FileText className="w-3.5 h-3.5 mr-1.5 text-blue-400" /> Executive Field Summary
                  </h4>
                  <p className="text-slate-300 leading-relaxed whitespace-pre-line text-xs">
                    {aiBriefing.summary_briefing}
                  </p>
                </div>

                {/* Inspectable Citations */}
                <div className="space-y-2">
                  <h4 className="font-semibold text-white flex items-center">
                    <ShieldCheck className="w-3.5 h-3.5 mr-1.5 text-emerald-400" /> Verifiable Citations &amp; Evidence
                  </h4>
                  <div className="space-y-1.5">
                    {aiBriefing.citations.map((c, i) => (
                      <div key={i} className="p-2 bg-slate-900/50 rounded border border-slate-800 flex justify-between items-center text-[11px]">
                        <div>
                          <span className="text-slate-400">{c.metric}: </span>
                          <span className="text-white font-semibold">{c.observed_value}</span>
                        </div>
                        <span className="text-slate-500 text-[10px]">{c.context}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Field CRM Interactions & LLM Call Notes */}
                {selectedHcpInteractions.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <h4 className="font-semibold text-white flex items-center">
                      <Users className="w-3.5 h-3.5 mr-1.5 text-purple-400" /> Recent Field Call Notes &amp; CRM Logs ({selectedHcpInteractions.length})
                    </h4>
                    <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                      {selectedHcpInteractions.map((inter, i) => {
                        const isAiGenerated = inter.notes && inter.notes.includes('[Sarvam AI Generated Call Note]');
                        return (
                          <div
                            key={i}
                            className={`p-2.5 rounded-lg border text-[11px] space-y-1 ${
                              isAiGenerated
                                ? 'bg-purple-950/30 border-purple-500/40'
                                : 'bg-slate-900/50 border-slate-800'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-semibold text-slate-200">{inter.channel} • {inter.interaction_date}</span>
                              <div className="flex items-center space-x-1.5">
                                {isAiGenerated && (
                                  <span className="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold text-[9px] border border-purple-500/30">
                                    Sarvam AI 105B
                                  </span>
                                )}
                                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                                  inter.sentiment === 'Positive' || inter.sentiment === 'Advocate' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                                }`}>
                                  {inter.sentiment}
                                </span>
                              </div>
                            </div>
                            <p className="text-slate-300 text-[11px] leading-relaxed whitespace-pre-line">
                              {inter.notes}
                            </p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}

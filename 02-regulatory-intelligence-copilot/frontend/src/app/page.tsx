'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  Search,
  BookOpen,
  GitCompare,
  FileCheck2,
  Database,
  Sparkles,
  ExternalLink,
  ChevronRight,
  Filter,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Layers,
  Send,
  Building2,
  FileText,
  BadgeAlert,
  RefreshCw,
} from 'lucide-react';
import {
  api,
  SearchResponse,
  GuidanceSummary,
  GuidanceDetail,
  DiffResponse,
  SubmissionImpactItem,
} from '../services/api';

type TabType = 'search' | 'guidances' | 'diff' | 'impacts' | 'nl2sql';
type UserRole = 'SUPER_ADMIN' | 'ADMIN' | 'REGULATORY_REVIEWER' | 'AUDITOR' | 'STANDARD_USER';

export default function RegulatoryIntelligenceApp() {
  const [activeTab, setActiveTab] = useState<TabType>('search');
  const [userRole, setUserRole] = useState<UserRole>('REGULATORY_REVIEWER');

  // Search State
  const [searchQuery, setSearchQuery] = useState('');
  const [authorityFilter, setAuthorityFilter] = useState('');
  const [therapeuticFilter, setTherapeuticFilter] = useState('');
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchResult, setSearchResult] = useState<SearchResponse | null>(null);

  // Guidance Library State
  const [guidances, setGuidances] = useState<GuidanceSummary[]>([]);
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);
  const [selectedDocDetail, setSelectedDocDetail] = useState<GuidanceDetail | null>(null);
  const [docLoading, setDocLoading] = useState(false);

  // Cross-Version Diff State
  const [diffResult, setDiffResult] = useState<DiffResponse | null>(null);
  const [diffLoading, setDiffLoading] = useState(false);

  // Pipeline Impacts State
  const [impacts, setImpacts] = useState<SubmissionImpactItem[]>([]);
  const [impactLoading, setImpactLoading] = useState(false);

  // NL2SQL State
  const [nl2sqlQuery, setNl2sqlQuery] = useState('How many guidance documents were published by FDA in oncology?');
  const [nl2sqlResult, setNl2sqlResult] = useState<any | null>(null);
  const [nl2sqlLoading, setNl2sqlLoading] = useState(false);

  // Citation Drawer State
  const [activeCitation, setActiveCitation] = useState<any | null>(null);

  // Initial Load
  useEffect(() => {
    initApp();
  }, []);

  const initApp = async () => {
    try {
      await api.login('reg_reviewer', 'Reviewer@123').catch(() => null);
      loadGuidances();
      loadImpacts();
      loadDiff();
    } catch (e) {
      console.error(e);
    }
  };

  const loadGuidances = async () => {
    try {
      const docs = await api.getGuidances();
      setGuidances(docs);
    } catch (e) {
      console.error(e);
    }
  };

  const loadImpacts = async () => {
    setImpactLoading(true);
    try {
      const data = await api.getSubmissionImpacts();
      setImpacts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setImpactLoading(false);
    }
  };

  const loadDiff = async () => {
    setDiffLoading(true);
    try {
      const data = await api.getCrossVersionDiff('DOC-FDA-RWE-2021', 'DOC-FDA-RWE-2024');
      setDiffResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setDiffLoading(false);
    }
  };

  const handleSearch = async (queryText?: string) => {
    const q = queryText || searchQuery;
    if (!q.trim()) return;
    setSearchLoading(true);
    setSearchResult(null);
    try {
      const res = await api.searchRegulatory(q, authorityFilter || undefined, therapeuticFilter || undefined);
      setSearchResult(res);
    } catch (err: any) {
      alert(`Search failed: ${err.message}`);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSelectDoc = async (docId: string) => {
    setSelectedDocId(docId);
    setDocLoading(true);
    try {
      const detail = await api.getGuidanceDetail(docId);
      setSelectedDocDetail(detail);
    } catch (e) {
      console.error(e);
    } finally {
      setDocLoading(false);
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
      alert(`NL2SQL error: ${err.message}`);
    } finally {
      setNl2sqlLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans">
      {/* Synthetic Data Disclaimer Banner */}
      <div className="bg-gradient-to-r from-indigo-950 via-slate-900 to-indigo-950 border-b border-indigo-500/30 px-6 py-2 text-xs font-medium text-indigo-200 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-indigo-400 shrink-0" />
          <span>
            <strong>SYNTHETIC REGULATORY BENCHMARK:</strong> Official guidance summaries from FDA, EMA, ICH, PMDA, and WHO are curated for automated AI impact analysis and decision-support verification.
          </span>
        </div>
        <span className="bg-indigo-500/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider text-indigo-300">
          Enterprise Demo Mode
        </span>
      </div>

      {/* Main Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Pharma Regulatory Intelligence Copilot
              </h1>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold">
                v1.0.0
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Sarvam AI (105B) • LangGraph Evidence Verification • Safe NL2SQL • Cross-Version Diff
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-800">
          {[
            { id: 'search', label: 'Copilot Search', icon: Search },
            { id: 'guidances', label: 'Guidance Library', icon: Layers },
            { id: 'diff', label: 'Version Diff', icon: GitCompare },
            { id: 'impacts', label: 'Pipeline Impacts', icon: FileCheck2 },
            { id: 'nl2sql', label: 'NL2SQL Explorer', icon: Database },
          ].map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 font-semibold'
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
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500">Active RBAC Role</div>
            <select
              value={userRole}
              onChange={(e) => setUserRole(e.target.value as UserRole)}
              className="bg-slate-900 border border-slate-700 text-xs font-semibold text-indigo-400 rounded px-2.5 py-1 outline-none focus:border-indigo-500 cursor-pointer"
            >
              <option value="SUPER_ADMIN">SUPER_ADMIN (100)</option>
              <option value="ADMIN">ADMIN (80)</option>
              <option value="REGULATORY_REVIEWER">REGULATORY_REVIEWER (40)</option>
              <option value="AUDITOR">AUDITOR (20)</option>
              <option value="STANDARD_USER">STANDARD_USER (10)</option>
            </select>
          </div>
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" title="Backend Live: Port 8001" />
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* VIEW 1: COPILOT SEARCH & HYBRID RAG */}
        {activeTab === 'search' && (
          <div className="space-y-6">
            {/* Search Input Box */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-white flex items-center">
                    <Sparkles className="w-4 h-4 mr-2 text-indigo-400" /> Grounded Regulatory Copilot Inquiry
                  </h2>
                  <p className="text-xs text-slate-400">
                    Ask questions across FDA, EMA, ICH, PMDA, and WHO guidances with verifiable chunk-level citations.
                  </p>
                </div>
                <div className="flex items-center space-x-2 text-xs">
                  <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">FDA 2024</span>
                  <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">EMA ICH E6(R3)</span>
                  <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">PMDA Registry</span>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="relative flex-1">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    placeholder="e.g., What are the mandatory source data verification (SDV) requirements for registry external control arms in FDA oncology submissions?"
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <button
                  onClick={() => handleSearch()}
                  disabled={searchLoading}
                  className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center space-x-2 transition-all disabled:opacity-50"
                >
                  {searchLoading ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      <span>Synthesizing...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-3.5 h-3.5" />
                      <span>Analyze Guidance</span>
                    </>
                  )}
                </button>
              </div>

              {/* Instant Prompt Presets */}
              <div className="flex items-center space-x-2 pt-1 text-[11px] overflow-x-auto">
                <span className="text-slate-500 font-semibold uppercase text-[10px] shrink-0">Sample Queries:</span>
                {[
                  'What are the 21 CFR Part 11 requirements for registry audit trails?',
                  'How does ICH E6(R3) govern digital health technologies & wearables?',
                  'What transparency standards does FDA mandate for AI/ML drug models?',
                  'What sensitivity analyses are required for unmeasured confounding in RWE?',
                ].map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSearchQuery(preset);
                      handleSearch(preset);
                    }}
                    className="px-2.5 py-1 rounded-md bg-slate-900/90 border border-slate-800 text-slate-400 hover:text-indigo-300 hover:border-indigo-500/50 shrink-0 transition-colors"
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Results Display */}
            {searchResult && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Synthesized Answer Card */}
                <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div className="flex items-center space-x-2">
                      <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold uppercase tracking-wider">
                        Verified Guidance Synthesis
                      </span>
                      <span className="text-xs text-slate-400 font-mono">
                        Latency: {searchResult.latency_ms}ms
                      </span>
                    </div>
                    <span className="text-xs text-indigo-400 font-medium">
                      Provider: {searchResult.provider_used}
                    </span>
                  </div>

                  <div className="text-xs text-slate-200 leading-relaxed whitespace-pre-line space-y-3 font-normal">
                    {searchResult.answer}
                  </div>
                </div>

                {/* Inspectable Citations List */}
                <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center">
                      <FileText className="w-3.5 h-3.5 mr-1.5 text-indigo-400" />
                      Authoritative Citations ({searchResult.citations.length})
                    </h3>
                  </div>

                  <div className="space-y-3">
                    {searchResult.citations.map((c, i) => (
                      <div
                        key={i}
                        onClick={() => setActiveCitation(c)}
                        className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 hover:border-indigo-500/50 cursor-pointer transition-all space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 text-[10px] font-bold">
                            {c.authority}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            Page {c.page_number}
                          </span>
                        </div>
                        <h4 className="text-xs font-bold text-slate-200">{c.section_number}: {c.section_title}</h4>
                        <p className="text-[11px] text-slate-400 line-clamp-2">
                          "{c.exact_snippet}"
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* VIEW 2: GUIDANCE LIBRARY & BROWSER */}
        {activeTab === 'guidances' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Guidance Document List */}
            <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div>
                  <h2 className="text-sm font-bold text-white">Global Guidance Catalog</h2>
                  <p className="text-xs text-slate-400">Indexed health authority documents with chunk-level parse tree.</p>
                </div>
                <span className="px-2.5 py-1 rounded bg-slate-900 text-xs font-mono text-indigo-400 border border-slate-800">
                  {guidances.length} Documents
                </span>
              </div>

              <div className="space-y-3">
                {guidances.map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => handleSelectDoc(doc.id)}
                    className={`p-4 rounded-xl border transition-all cursor-pointer ${
                      selectedDocId === doc.id
                        ? 'bg-indigo-950/40 border-indigo-500/50 shadow-md shadow-indigo-600/10'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center space-x-2">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300">
                          {doc.authority}
                        </span>
                        <span className="text-[11px] font-mono text-slate-400">{doc.document_number}</span>
                      </div>
                      <span className="text-[11px] text-slate-400">{doc.publication_date} • v{doc.version}</span>
                    </div>
                    <h3 className="text-xs font-bold text-white">{doc.title}</h3>
                    <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{doc.summary}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Document Detail & Sections Inspector */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center">
                <FileText className="w-3.5 h-3.5 mr-1.5 text-indigo-400" />
                Parsed Guidance Sections
              </h3>

              {docLoading ? (
                <div className="py-12 text-center text-xs text-slate-400">
                  <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-400" />
                  Loading document structure...
                </div>
              ) : selectedDocDetail ? (
                <div className="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
                  <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                    <span className="text-[10px] text-slate-500 uppercase font-semibold">Active Document</span>
                    <h4 className="text-xs font-bold text-white mt-0.5">{selectedDocDetail.title}</h4>
                  </div>

                  {selectedDocDetail.sections.map((sec) => (
                    <div key={sec.id} className="p-3 bg-slate-900/50 rounded-lg border border-slate-800 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] font-bold text-indigo-300">{sec.section_number}</span>
                        <span className="text-[10px] text-slate-400 font-mono">Page {sec.page_number}</span>
                      </div>
                      <div className="text-xs font-semibold text-slate-200">{sec.section_title}</div>
                      <p className="text-[11px] text-slate-400 leading-relaxed mt-1">
                        {sec.chunk_text}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-12 text-center text-xs text-slate-500">
                  Select a guidance document from the catalog to inspect sections.
                </div>
              )}
            </div>
          </div>
        )}

        {/* VIEW 3: CROSS-VERSION DIFF ANALYZER */}
        {activeTab === 'diff' && (
          <div className="space-y-6">
            {diffResult && (
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
                <div className="flex items-start justify-between pb-4 border-b border-slate-800">
                  <div>
                    <span className="px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-[10px] font-bold uppercase tracking-wider">
                      Automated Regulatory Diff Analysis
                    </span>
                    <h2 className="text-base font-bold text-white mt-1">
                      {diffResult.baseline_doc.title} (v{diffResult.baseline_doc.version}) vs. {diffResult.comparison_doc.title} (v{diffResult.comparison_doc.version})
                    </h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Analyzed via Sarvam AI • {diffResult.total_changes} structural differences identified
                    </p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="px-3 py-1.5 bg-rose-500/10 border border-rose-500/20 rounded-lg text-center">
                      <div className="text-[10px] text-rose-400 uppercase font-semibold">Critical Changes</div>
                      <div className="text-base font-bold text-rose-300">{diffResult.critical_changes}</div>
                    </div>
                    <div className="px-3 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-lg text-center">
                      <div className="text-[10px] text-amber-400 uppercase font-semibold">High Priority</div>
                      <div className="text-base font-bold text-amber-300">{diffResult.high_priority_changes}</div>
                    </div>
                  </div>
                </div>

                {/* Diff Comparison Cards */}
                <div className="space-y-4">
                  {diffResult.changes.map((change) => (
                    <div key={change.id} className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            change.impact_severity === 'CRITICAL'
                              ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                              : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                          }`}>
                            {change.impact_severity}
                          </span>
                          <span className="text-xs font-bold text-white">
                            {change.section_number}: {change.section_title}
                          </span>
                        </div>
                        <span className="text-[11px] font-mono text-indigo-400 font-semibold">{change.change_type}</span>
                      </div>

                      {/* Side-by-side text */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div className="p-3 bg-slate-950 rounded border border-rose-950/40 space-y-1">
                          <span className="text-[10px] font-semibold text-rose-400 uppercase">Baseline Text (2021 Draft)</span>
                          <p className="text-slate-400 text-[11px] leading-relaxed">
                            {change.old_text || 'Not present in baseline version.'}
                          </p>
                        </div>
                        <div className="p-3 bg-slate-950 rounded border border-emerald-950/40 space-y-1">
                          <span className="text-[10px] font-semibold text-emerald-400 uppercase">Updated Text (2024 Final)</span>
                          <p className="text-slate-200 text-[11px] leading-relaxed">
                            {change.new_text}
                          </p>
                        </div>
                      </div>

                      {/* Semantic Impact Callout */}
                      <div className="p-2.5 bg-indigo-950/30 border border-indigo-500/30 rounded-lg text-xs text-indigo-200 flex items-start space-x-2">
                        <Sparkles className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                        <div>
                          <strong className="text-white">Regulatory Impact Assessment:</strong> {change.semantic_impact}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* VIEW 4: PIPELINE SUBMISSION IMPACTS */}
        {activeTab === 'impacts' && (
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div>
                <h2 className="text-sm font-bold text-white">Active Pipeline Submission Impact Matrix</h2>
                <p className="text-xs text-slate-400">
                  Cross-referenced regulatory changes impacting ongoing clinical programs and IND/NDA filings.
                </p>
              </div>
              <span className="px-2.5 py-1 rounded bg-slate-900 text-xs font-mono text-emerald-400 border border-slate-800">
                {impacts.length} Impacted Programs
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                    <th className="py-2.5 px-3">Product / Program</th>
                    <th className="py-2.5 px-3">Filing / Phase</th>
                    <th className="py-2.5 px-3">Therapeutic Area</th>
                    <th className="py-2.5 px-3">Impact Level</th>
                    <th className="py-2.5 px-3">Action Required</th>
                    <th className="py-2.5 px-3">Compliance Deadline</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {impacts.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-3 px-3 font-semibold text-white">{item.product_name}</td>
                      <td className="py-3 px-3 text-slate-300 font-mono">{item.ind_nda_number} ({item.development_phase})</td>
                      <td className="py-3 px-3 text-slate-400">{item.therapeutic_area}</td>
                      <td className="py-3 px-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          item.impact_level === 'Critical'
                            ? 'bg-rose-500/20 text-rose-300'
                            : item.impact_level === 'High'
                            ? 'bg-amber-500/20 text-amber-300'
                            : 'bg-blue-500/20 text-blue-300'
                        }`}>
                          {item.impact_level}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-slate-300 max-w-xs">{item.action_required}</td>
                      <td className="py-3 px-3 font-mono text-slate-400">{item.compliance_deadline || 'Open'}</td>
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
                <Database className="w-4 h-4 mr-2 text-indigo-400" /> Safe Regulatory NL2SQL Explorer
              </h2>
              <p className="text-xs text-slate-400">
                Execute natural language queries across guidance registries, authorities, and submission impact tables.
              </p>
            </div>

            <div className="flex items-center space-x-3">
              <input
                type="text"
                value={nl2sqlQuery}
                onChange={(e) => setNl2sqlQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleRunNl2sql()}
                className="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="Ask in natural language..."
              />
              <button
                onClick={() => handleRunNl2sql()}
                disabled={nl2sqlLoading}
                className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center space-x-2 transition-all disabled:opacity-50"
              >
                {nl2sqlLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Database className="w-3.5 h-3.5" />}
                <span>Execute Query</span>
              </button>
            </div>

            {/* Presets */}
            <div className="flex items-center space-x-2 text-[11px] overflow-x-auto">
              <span className="text-slate-500 font-semibold uppercase text-[10px] shrink-0">Quick Queries:</span>
              {[
                'How many guidances are published by each authority?',
                'Show all critical impact submissions and actions',
                'List all FDA guidances concerning oncology',
              ].map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setNl2sqlQuery(p);
                    handleRunNl2sql(p);
                  }}
                  className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400 hover:text-indigo-300"
                >
                  {p}
                </button>
              ))}
            </div>

            {/* SQL Results */}
            {nl2sqlResult && (
              <div className="space-y-4 pt-3 border-t border-slate-800">
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                  <div className="font-mono text-xs text-indigo-300">
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

      {/* CITATION MODAL DRAWER */}
      {activeCitation && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel-glow bg-slate-950 border border-slate-800 rounded-2xl max-w-xl w-full p-6 space-y-4 max-h-[85vh] overflow-y-auto">
            <div className="flex items-start justify-between">
              <div>
                <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-[10px] font-bold">
                  {activeCitation.authority}
                </span>
                <h3 className="text-base font-bold text-white mt-1">
                  {activeCitation.section_number}: {activeCitation.section_title}
                </h3>
                <p className="text-xs text-slate-400">{activeCitation.document_title} • Page {activeCitation.page_number}</p>
              </div>
              <button
                onClick={() => setActiveCitation(null)}
                className="text-slate-400 hover:text-white px-2 py-1 bg-slate-900 rounded text-sm"
              >
                ✕
              </button>
            </div>

            <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 text-xs text-slate-200 leading-relaxed">
              {activeCitation.exact_snippet}
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setActiveCitation(null)}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold"
              >
                Close Evidence
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

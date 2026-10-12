# Business Use Case: Pharma Commercial Intelligence & Next-Best-Action (NBA) Platform

## 1. Executive Summary
In life sciences commercial operations, pharmaceutical sales representatives and Medical Science Liaisons (MSLs) manage portfolios of thousands of Healthcare Professionals (HCPs). Despite massive investments in enterprise CRMs and prescription databases, commercial teams struggle with prioritization fatigue, suboptimal channel selection, and delayed responses to market shifts (such as competitor launches or sudden drops in new patient starts).

This platform acts as an **AI-powered commercial co-pilot** combining:
1. **Predictive Machine Learning**: High-precision XGBoost conversion/propensity models predicting 30-day treatment adoption.
2. **Deterministic Next-Best-Action (NBA) Logic**: Transparent commercial rule matrices that assign channels, messages, and timing.
3. **Safe NL2SQL & Analytical Tools**: Agents querying longitudinal prescription datasets directly in SQL with read-only guarantees.
4. **Agentic Orchestration (LangGraph)**: Multi-agent collaboration delivering executive briefings grounded in empirical evidence via Sarvam AI (with resilient OpenAI fallback).

---

## 2. Target Industry & Employers
- **Therapeutic Focus**: High-value specialty pharma (Oncology, Cardiology, Immunology, Rare Disease).
- **Target Employers**: Pfizer, AstraZeneca, Novartis, Johnson & Johnson, GlaxoSmithKline (GSK), Sanofi, Roche/Genentech.

---

## 3. Current State vs. Target State

| Dimension | Current State (Legacy Pharma Commercial) | Target State (AI-Driven Commercial NBA) |
| :--- | :--- | :--- |
| **HCP Prioritization** | Static quarterly call lists based on historical Rx volume. Slow to adapt to recent shifts. | Dynamic, weekly propensity scoring driven by real-time Rx changes, sentiment, and digital behavior. |
| **Pre-Call Planning** | Sales reps spend 30–45 minutes per call digging through CRM notes, Excel sheets, and claims portals. | Reps open a 1-page dossier with AI briefings, top 3 drivers, and recommended action generated in <3 seconds. |
| **Channel Optimization** | Heavy reliance on in-person visits regardless of HCP digital responsiveness. | Omnichannel affinity matching (Email vs. In-Person vs. Webinar vs. Peer Advisory) with fatigue capping. |
| **Trust & Adoption** | Reps ignore "black-box" scores because they cannot see *why* an HCP was prioritized. | 100% explainable drivers, SHAP waterfall charts, verifiable Rx trends, and grounded LLM reasoning. |
| **Territory Alignment** | Territory managers lack immediate visibility into rep workload vs. high-potential opportunity gaps. | Real-time territory opportunity heatmaps and quota tracking. |

---

## 4. Primary Personas & User Journeys

### Persona A: Commercial Sales Representative (Field Rep)
- **Pain Point**: "I have 180 oncologists in my territory. I only have time for 25 details this month. Who do I call first and what clinical study should I bring up?"
- **User Journey**:
  1. Rep logs in and opens the **Recommendations View**.
  2. Filters by assigned territory (`Territory: North-East Metro`).
  3. Inspects Top 5 high-priority HCPs. Clicks "Explain Action" for Dr. Sarah Chen.
  4. Reviews the AI Briefing: *"Dr. Chen experienced a 22% drop in OncoVex NRx over the last 60 days, coinciding with 2 competitor details. Her digital engagement indicates interest in biomarker selection. Recommended Action: Schedule F2F clinical detail with Biomarker Study X."*
  5. Rep executes call with targeted messaging.

### Persona B: Sales Manager / Territory Director
- **Pain Point**: "Our territory is trailing quota by 14%. Which accounts have high latent potential that our reps haven't visited in >45 days?"
- **User Journey**:
  1. Opens **Territory Analytics Dashboard**.
  2. Identifies territories with high competitor penetration but low rep touch frequency.
  3. Adjusts prioritization weights or reallocates reps to high-density clusters.

### Persona C: Commercial Operations & Business Owner
- **Pain Point**: "What is the financial return of implementing an automated Next-Best-Action platform across our 50-rep field force?"
- **User Journey**:
  1. Navigates to **ROI Calculator**.
  2. Inputs: 50 reps, 120 calls/month, $80/hr cost, +2.5% expected conversion uplift.
  3. Platform outputs deterministic annual savings of $288,000 in rep planning time and $1.4M in incremental brand revenue.

---

## 5. Agentic AI & NL2SQL Architecture in the Business Context

Rather than relying on hallucination-prone chatbots, the system employs **structured multi-agent collaboration**:
1. **Natural Language to SQL (NL2SQL)**: When an analyst asks, *"Show me all cardiologists in Texas with over 40 competitor prescriptions who haven't had a visit in 30 days"*, the NL2SQL tool generates safe, parameterized read-only SQL, queries PostgreSQL, and returns exact tabular data.
2. **LangGraph Multi-Agent Team**:
   - `HCP Profile Agent`: Retrieves clinical specialty, hospital affiliations, and decile tiers.
   - `Rx Trend Agent`: Analyzes 12-month rolling prescription trajectory.
   - `Engagement Agent`: Reviews CRM touchpoints, rep notes, and digital open rates.
   - `Market Agent`: Benchmarks against competitor market share.
   - `Explanation Synthesizer`: Uses Sarvam AI (or OpenAI fallback) to draft a tailored pre-call action plan citing verifiable facts.

---

## 6. Measurable Business KPIs & Financial ROI

- **Time Saved**: 45% reduction in rep pre-call research time (saving ~6 hours/rep/week).
- **Conversion Lift**: +12% to +18% increase in detailing conversion rate due to contextual messaging.
- **HCP Satisfaction**: Reduced message fatigue via multi-channel capping rules (max 2 touches/month).
- **Revenue Impact**: For a mid-size brand with 50 reps, estimated annual net impact exceeds **$1.65 Million** (modeled deterministically in the platform's ROI engine).

# Feature: LangGraph Agentic Briefings & Explanation Synthesizer

## 1. Purpose & Business Context
Delivers pre-call commercial briefings to field representatives explaining *why* an HCP is prioritized and *what* messaging should be used, eliminating black-box distrust.

## 2. Agentic Multi-Agent Workflow
1. **Supervisor Node**: Analyzes analyst intent and dispatches tasks.
2. **HCP Dossier Node**: Extracts verified profile facts from DB.
3. **Rx Analytics Node**: Summarizes longitudinal prescription trajectory.
4. **CRM Engagement Node**: Reviews past rep touchpoints and HCP sentiment.
5. **Explanation Synthesizer**: Powered by Sarvam AI (`sarvam-105b`) with resilient fallback to OpenAI (`gpt-4o-mini`).

## 3. Strict Guardrails
- LLM is strictly prohibited from inventing numerical scores.
- Every claim cites verifiable facts (e.g. "3-month TRx growth is +18%").

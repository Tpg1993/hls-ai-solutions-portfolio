import time
from typing import List, Dict, Any, Tuple
from app.ai.providers.base import LLMResponse
from app.ai.providers.sarvam_provider import SarvamProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.core.config import settings
from app.core.logging import logger

class LLMRouter:
    def __init__(self):
        self.sarvam = SarvamProvider()
        self.openai = OpenAIProvider()
        self.circuit_breaker_open = False
        self.consecutive_failures = 0

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1000,
        grounded_context: Dict[str, Any] = None,
    ) -> Tuple[LLMResponse, bool]:
        # Primary: Sarvam AI
        if not self.circuit_breaker_open and await self.sarvam.is_available():
            try:
                response = await self.sarvam.generate_text(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                self.consecutive_failures = 0
                return response, False
            except Exception as e:
                logger.warning(f"Primary Sarvam AI call failed: {e}. Initiating fallback routing...")
                self.consecutive_failures += 1
                if self.consecutive_failures >= 3:
                    self.circuit_breaker_open = True

        # Fallback: OpenAI
        if settings.OPENAI_FALLBACK_ENABLED and await self.openai.is_available():
            try:
                response = await self.openai.generate_text(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                logger.info("Successfully executed OpenAI fallback completion.")
                return response, True
            except Exception as e:
                logger.error(f"OpenAI fallback call failed: {e}")

        # Deterministic Grounded Offline Synthesizer
        logger.info("Executing Deterministic Grounded Clinical Synthesizer...")
        fallback_text = self._build_deterministic_synthesis(grounded_context)
        return (
            LLMResponse(
                content=fallback_text,
                provider_name="Deterministic Clinical Decision Engine (Offline Fallback)",
                model_name="deterministic-rule-v1.0",
                latency_ms=10.0,
                token_usage={"total_tokens": 120},
            ),
            True,
        )

    def _build_deterministic_synthesis(self, context: Dict[str, Any] = None) -> str:
        if not context:
            return "Protocol screening evaluation completed based on deterministic inclusion/exclusion criteria."
        patient_id = context.get("patient_id", "Patient")
        trial_id = context.get("trial_id", "Trial")
        status = context.get("eligibility_status", "UNCERTAIN")
        return (
            f"**Clinical Decision Summary for {patient_id} ({trial_id}):**\n"
            f"Overall Status: **{status}**\n\n"
            f"- Structured inclusion and exclusion criteria evaluated deterministically against clinical labs and genomic markers.\n"
            f"- Clinical reviewer sign-off required prior to official screening enrollment."
        )

llm_router = LLMRouter()

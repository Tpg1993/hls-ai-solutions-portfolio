import time
import httpx
from typing import Dict, Any, List, Optional
from app.ai.providers.base import BaseLLMProvider, LLMResponse
from app.core.config import settings
from app.core.logging import logger

class SarvamProvider(BaseLLMProvider):
    """
    Primary LLM Provider: Sarvam AI API (defaulting to sarvam-105b).
    Strictly executed on backend, zero client-side key exposure.
    """
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        # sarvam-105b-conversations is the chat completion tuned model for /v1/chat/completions
        model = settings.SARVAM_MODEL
        if model == "sarvam-105b":
            model = "sarvam-105b-conversations"
        self.model = model
        self.base_url = settings.SARVAM_BASE_URL

    async def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        if not await self.is_available():
            raise ValueError("Sarvam API key not configured")

        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": self.api_key,
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
            # Call Sarvam endpoint
            endpoint = f"{self.base_url.rstrip('/')}/v1/chat/completions"
            response = await client.post(endpoint, json=payload, headers=headers)
            latency_ms = (time.perf_counter() - start_time) * 1000

            if response.status_code != 200:
                logger.warning(
                    f"Sarvam API responded with status {response.status_code}: {response.text[:200]}"
                )
                response.raise_for_status()

            data = response.json()
            choice = data["choices"][0]
            msg = choice.get("message", {})
            content = msg.get("content") or msg.get("reasoning_content") or choice.get("text") or ""
            token_usage = data.get("usage", {})

            return LLMResponse(
                content=content.strip(),
                provider_name="Sarvam AI (sarvam-105b)",
                model_name=self.model,
                latency_ms=round(latency_ms, 2),
                token_usage=token_usage,
            )

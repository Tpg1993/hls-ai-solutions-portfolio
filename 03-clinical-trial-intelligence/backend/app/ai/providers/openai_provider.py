import time
import httpx
from typing import Dict, Any, List
from app.ai.providers.base import BaseLLMProvider, LLMResponse
from app.core.config import settings
from app.core.logging import logger

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        if not await self.is_available():
            raise ValueError("OpenAI API key not configured")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            latency_ms = (time.perf_counter() - start_time) * 1000

            if response.status_code != 200:
                logger.warning(f"OpenAI API responded with status {response.status_code}: {response.text[:200]}")
                response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            token_usage = data.get("usage", {})

            return LLMResponse(
                content=content.strip(),
                provider_name="OpenAI (gpt-4o-mini)",
                model_name=self.model,
                latency_ms=round(latency_ms, 2),
                token_usage=token_usage,
            )

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: str
    provider_name: str
    model_name: str
    latency_ms: float
    token_usage: Optional[Dict[str, Any]] = None

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        pass

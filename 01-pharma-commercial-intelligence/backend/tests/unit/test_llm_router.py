import pytest
from unittest.mock import patch, AsyncMock
from app.ai.router import llm_router

@pytest.mark.asyncio
async def test_deterministic_local_briefing_fallback():
    facts = {
        "hcp_name": "Dr. Sarah Chen",
        "specialty": "Oncology",
        "priority_tier": "High",
        "recommended_action": "Clinical Detail - Head-to-Head Efficacy Data",
        "recommended_channel": "In-Person Detail",
        "trx_growth_3m": 0.18,
        "competitor_share": 0.52,
    }
    messages = [{"role": "user", "content": "Explain recommendation"}]
    
    # In test environment without external API keys configured, router safely returns deterministic briefing
    with patch.object(llm_router.sarvam, "is_available", new_callable=AsyncMock, return_value=False), \
         patch.object(llm_router.openai, "is_available", new_callable=AsyncMock, return_value=False):
        response, fallback = await llm_router.generate_completion(messages, grounded_facts=facts)
        assert response is not None
        assert "Dr. Sarah Chen" in response.content
        assert "High" in response.content
        assert response.latency_ms > 0

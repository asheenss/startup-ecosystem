from __future__ import annotations

import json
import logging

from openai import OpenAI

from app.core.config import settings
from app.core.prompts import PROMPT_VERSION, STARTUP_EVALUATION_PROMPT
from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse

logger = logging.getLogger(__name__)


class StartupEvaluationAgent(BaseAgent):
    name = "StartupEvaluationAgent"

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _fallback(self, evidence_map: dict[str, list[str]]) -> dict:
        base = 7
        return {
            "problem_score": base,
            "market_score": base,
            "product_score": base,
            "traction_score": 6,
            "team_score": 7,
            "financial_score": 6,
            "total_score": 66,
            "strengths": ["Clear product thesis", "Readable narrative"],
            "weaknesses": ["Financial depth is limited", "Traction proof could be stronger"],
            "suggestions": [
                "Add clearer market sizing evidence.",
                "Show customer or pilot traction on a dedicated slide.",
                "Explain financial assumptions behind the funding ask.",
            ],
            "reasoning": "Fallback rubric based on extracted evidence coverage.",
            "confidence_score": 0.45,
            "evidence_map": evidence_map,
        }

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        startup_profile = message.data["startup_profile"]
        evidence_map = message.data["evidence_map"]

        if not self.client:
            return ProtocolResponse(sender=self.name, data=self._fallback(evidence_map))

        prompt = STARTUP_EVALUATION_PROMPT.format(
            startup_profile=json.dumps(startup_profile, indent=2),
            evidence=json.dumps(evidence_map, indent=2),
        )

        try:
            response = self.client.responses.create(model=settings.openai_model, input=prompt)
            payload = json.loads(response.output_text.replace("```json", "").replace("```", "").strip())
            payload["prompt_version"] = PROMPT_VERSION
            return ProtocolResponse(sender=self.name, data=payload)
        except Exception as exc:
            logger.warning("Startup evaluation failed, using fallback: %s", exc)
            return ProtocolResponse(sender=self.name, data=self._fallback(evidence_map))

from __future__ import annotations

import json
import logging

from openai import OpenAI

from app.core.config import settings
from app.core.prompts import IMPROVEMENT_SUGGESTION_PROMPT
from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse

logger = logging.getLogger(__name__)


class ImprovementSuggestionAgent(BaseAgent):
    name = "ImprovementSuggestionAgent"

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        evaluation = message.data["evaluation"]
        if not self.client:
            return ProtocolResponse(
                sender=self.name,
                data={
                    "suggestions": evaluation.get("suggestions", []),
                    "dashboard_insights": [
                        "Clarify market proof.",
                        "Strengthen traction narrative.",
                        "Make the funding ask more concrete.",
                    ],
                },
            )

        prompt = IMPROVEMENT_SUGGESTION_PROMPT.format(evaluation=json.dumps(evaluation, indent=2))
        try:
            response = self.client.responses.create(model=settings.openai_model, input=prompt)
            payload = json.loads(response.output_text.replace("```json", "").replace("```", "").strip())
            return ProtocolResponse(sender=self.name, data=payload)
        except Exception as exc:
            logger.warning("Improvement suggestion generation failed: %s", exc)
            return ProtocolResponse(
                sender=self.name,
                data={
                    "suggestions": evaluation.get("suggestions", []),
                    "dashboard_insights": ["AI fallback insights unavailable."],
                },
            )

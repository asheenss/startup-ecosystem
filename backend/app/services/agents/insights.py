from __future__ import annotations

import json
import logging

from openai import OpenAI

from app.core.config import settings
from app.core.prompts import DASHBOARD_INSIGHTS_PROMPT
from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse

logger = logging.getLogger(__name__)


class DashboardInsightsAgent(BaseAgent):
    name = "DashboardInsightsAgent"

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        startup_profile = message.data["startup_profile"]
        evaluation = message.data["evaluation"]
        matches = message.data["matches"]

        if not self.client:
            return ProtocolResponse(
                sender=self.name,
                data={
                    "summary": f"{startup_profile['startup_name']} scored {evaluation['total_score']} overall.",
                    "highlights": evaluation.get("strengths", []),
                    "next_actions": evaluation.get("suggestions", []),
                },
            )

        prompt = DASHBOARD_INSIGHTS_PROMPT.format(
            startup_profile=json.dumps(startup_profile, indent=2),
            evaluation=json.dumps(evaluation, indent=2),
            matches=json.dumps(matches, indent=2),
        )
        try:
            response = self.client.responses.create(model=settings.openai_model, input=prompt)
            payload = json.loads(response.output_text.replace("```json", "").replace("```", "").strip())
            return ProtocolResponse(sender=self.name, data=payload)
        except Exception as exc:
            logger.warning("Dashboard insights generation failed: %s", exc)
            return ProtocolResponse(
                sender=self.name,
                data={
                    "summary": f"{startup_profile['startup_name']} scored {evaluation['total_score']} overall.",
                    "highlights": evaluation.get("strengths", []),
                    "next_actions": evaluation.get("suggestions", []),
                },
            )

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.investor_profile import InvestorProfile
from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse
from app.services.vector_service import VectorService


class InvestorMatchingAgent(BaseAgent):
    name = "InvestorMatchingAgent"

    def __init__(self) -> None:
        self.vector_service = VectorService()

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        db: Session = message.data["db"]
        startup_profile = message.data["startup_profile"]
        evaluation = message.data["evaluation"]
        startup_embedding = self.vector_service.startup_embedding(startup_profile, evaluation)

        matches: list[dict] = []
        investors = db.query(InvestorProfile).all()
        for investor in investors:
            investor_payload = {
                "investor_id": investor.id,
                "investor_name": investor.investor_name,
                "interests": investor.interests,
                "funding_range": investor.funding_range,
                "preferred_industries": investor.preferred_industries,
            }
            investor_embedding = self.vector_service.investor_embedding(investor_payload)
            similarity_seed = sum(
                left * right for left, right in zip(startup_embedding[:64], investor_embedding[:64], strict=False)
            )
            normalized = max(0.0, min(100.0, 50.0 + (similarity_seed * 3)))

            if startup_profile["industry"].lower() in investor.preferred_industries.lower():
                normalized += 15
            if startup_profile["stage"].lower() in investor.interests.lower():
                normalized += 10

            matches.append(
                {
                    "investor_id": investor.id,
                    "match_score": round(min(normalized, 100), 2),
                    "rationale": f"{investor.investor_name} aligns with the startup's industry, stage, or semantic thesis.",
                    "evidence": startup_profile["industry"],
                }
            )

        matches.sort(key=lambda item: item["match_score"], reverse=True)
        return ProtocolResponse(sender=self.name, data={"matches": matches[:5]})

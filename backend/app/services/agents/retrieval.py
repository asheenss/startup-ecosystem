from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse
from app.services.vector_service import VectorService


class PitchEvidenceRetrievalAgent(BaseAgent):
    name = "PitchEvidenceRetrievalAgent"

    def __init__(self) -> None:
        self.vector_service = VectorService()

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        db = message.data["db"]
        analysis_id = message.data["analysis_id"]

        evidence_map = {
            "problem": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows problem clarity?", limit=3),
            "market": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows market opportunity and size?", limit=3),
            "product": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows product differentiation?", limit=3),
            "traction": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows traction or momentum?", limit=3),
            "team": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows team strength or founder expertise?", limit=3),
            "financial": self.vector_service.search_relevant_chunks(db, analysis_id, "What evidence shows business model or financial viability?", limit=3),
        }
        return ProtocolResponse(sender=self.name, data={"evidence_map": evidence_map})

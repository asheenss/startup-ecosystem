from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.agents.evaluation import StartupEvaluationAgent
from app.services.agents.extraction import PitchExtractionAgent
from app.services.agents.improvement import ImprovementSuggestionAgent
from app.services.agents.insights import DashboardInsightsAgent
from app.services.agents.matching import InvestorMatchingAgent
from app.services.agents.memory import AgentMemory
from app.services.agents.protocol import ProtocolMessage
from app.services.agents.retrieval import PitchEvidenceRetrievalAgent
from app.services.vector_service import VectorService


class AgentOrchestrator:
    def __init__(self) -> None:
        self.memory = AgentMemory()
        self.vector_service = VectorService()
        self.extraction_agent = PitchExtractionAgent()
        self.retrieval_agent = PitchEvidenceRetrievalAgent()
        self.evaluation_agent = StartupEvaluationAgent()
        self.improvement_agent = ImprovementSuggestionAgent()
        self.matching_agent = InvestorMatchingAgent()
        self.insight_agent = DashboardInsightsAgent()

    def run(self, db: Session, analysis_id: int, file_path: str, startup_profile: dict) -> dict:
        extraction = self.extraction_agent.run(
            ProtocolMessage(sender="orchestrator", task="extract_pitch", data={"file_path": file_path})
        )
        self.memory.set("extraction", extraction.data)

        self.vector_service.store_chunks(db, analysis_id, extraction.data["chunks"])

        retrieval = self.retrieval_agent.run(
            ProtocolMessage(
                sender="orchestrator",
                task="retrieve_evidence",
                data={"db": db, "analysis_id": analysis_id},
                memory=self.memory.snapshot(),
            )
        )
        self.memory.set("retrieval", retrieval.data)

        evaluation = self.evaluation_agent.run(
            ProtocolMessage(
                sender="orchestrator",
                task="evaluate_startup",
                data={"startup_profile": startup_profile, "evidence_map": retrieval.data["evidence_map"]},
                memory=self.memory.snapshot(),
            )
        )
        self.memory.set("evaluation", evaluation.data)

        improvement = self.improvement_agent.run(
            ProtocolMessage(
                sender="orchestrator",
                task="generate_improvements",
                data={"evaluation": evaluation.data},
                memory=self.memory.snapshot(),
            )
        )
        self.memory.set("improvement", improvement.data)

        matching = self.matching_agent.run(
            ProtocolMessage(
                sender="orchestrator",
                task="recommend_investors",
                data={"db": db, "startup_profile": startup_profile, "evaluation": evaluation.data},
                memory=self.memory.snapshot(),
            )
        )
        self.memory.set("matching", matching.data)

        insights = self.insight_agent.run(
            ProtocolMessage(
                sender="orchestrator",
                task="dashboard_insights",
                data={
                    "startup_profile": startup_profile,
                    "evaluation": evaluation.data,
                    "matches": matching.data["matches"],
                },
                memory=self.memory.snapshot(),
            )
        )
        self.memory.set("insights", insights.data)

        return self.memory.snapshot()

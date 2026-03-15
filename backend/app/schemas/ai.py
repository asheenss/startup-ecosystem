from pydantic import BaseModel


class InvestorRecommendationRead(BaseModel):
    investor_id: int
    match_score: float
    rationale: str
    evidence: str | None = None


class AIAnalysisRead(BaseModel):
    id: int
    pitch_deck_id: int | None = None
    startup_id: int
    status: str
    model_name: str | None = None
    prompt_version: str | None = None
    confidence_score: float | None = None
    llm_reasoning: str | None = None
    score: float | None = None
    problem_clarity: float | None = None
    market_size: float | None = None
    product_differentiation: float | None = None
    traction: float | None = None
    team_strength: float | None = None
    financial_potential: float | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    evidence_map: str | None = None
    dashboard_insights: str | None = None
    improvement_suggestions: str | None = None
    extracted_text: str | None = None

    class Config:
        from_attributes = True


class PitchUploadResponse(BaseModel):
    pitch_id: int
    startup_id: int
    status: str
    file_name: str


class PitchAnalyzeResponse(BaseModel):
    analysis_id: int
    pitch_id: int
    status: str


class PitchResultResponse(BaseModel):
    pitch_id: int
    startup_id: int
    analysis: AIAnalysisRead | None = None
    investor_matches: list[InvestorRecommendationRead]
    evidence_sections: dict[str, list[str]]

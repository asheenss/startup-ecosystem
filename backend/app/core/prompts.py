PROMPT_VERSION = "v2"

STARTUP_EVALUATION_PROMPT = """
You are a senior venture capital analyst.

Use only the startup profile and retrieved pitch-deck evidence below.
Return strict JSON.

Startup Profile:
{startup_profile}

Retrieved Evidence:
{evidence}

Return this schema:
{{
  "problem_score": 0-10,
  "market_score": 0-10,
  "product_score": 0-10,
  "traction_score": 0-10,
  "team_score": 0-10,
  "financial_score": 0-10,
  "total_score": 0-100,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."],
  "reasoning": "short explanation",
  "confidence_score": 0.0,
  "evidence_map": {{
    "problem": ["..."],
    "market": ["..."],
    "product": ["..."],
    "traction": ["..."],
    "team": ["..."],
    "financial": ["..."]
  }}
}}
"""

IMPROVEMENT_SUGGESTION_PROMPT = """
You are a startup coach.

Based on this evaluation, generate concise, actionable improvement suggestions.

Evaluation:
{evaluation}

Return JSON:
{{
  "suggestions": ["..."],
  "dashboard_insights": ["..."]
}}
"""

INVESTOR_MATCHING_PROMPT = """
You are an investment analyst.

Given the startup profile, the startup evaluation, and the investor list, recommend the best investors.

Startup Profile:
{startup_profile}

Evaluation:
{evaluation}

Investors:
{investors}

Return JSON:
{{
  "matches": [
    {{
      "investor_id": 1,
      "match_score": 0-100,
      "rationale": "why this investor fits",
      "evidence": "relevant evidence snippet"
    }}
  ]
}}
"""

DASHBOARD_INSIGHTS_PROMPT = """
You are a product analyst creating dashboard insights for founders and investors.

Startup:
{startup_profile}

Evaluation:
{evaluation}

Investor Matches:
{matches}

Return JSON:
{{
  "summary": "short summary",
  "highlights": ["..."],
  "next_actions": ["..."]
}}
"""

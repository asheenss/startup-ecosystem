from app.models.investor_profile import InvestorProfile
from app.models.startup_profile import StartupProfile


def rank_investors_for_startup(
    startup: StartupProfile, investors: list[InvestorProfile]
) -> list[dict]:
    ranked: list[dict] = []

    for investor in investors:
        score = 0
        preferred = [item.strip().lower() for item in investor.preferred_industries.split(",")]

        if startup.industry.lower() in preferred:
            score += 45

        if startup.stage.lower() in investor.interests.lower():
            score += 20

        funding_gap = abs(investor.funding_range - startup.funding_needed)
        score += max(0, 35 - int(funding_gap / 25000))

        ranked.append(
            {
                "id": investor.id,
                "investor_name": investor.investor_name,
                "funding_range": investor.funding_range,
                "preferred_industries": preferred,
                "match_score": min(score, 100),
            }
        )

    return sorted(ranked, key=lambda item: item["match_score"], reverse=True)

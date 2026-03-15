from app.models.investor_profile import InvestorProfile
from app.models.startup_profile import StartupProfile
from app.services.matching_service import rank_investors_for_startup


def test_rank_investors_for_startup_orders_best_match_first():
    startup = StartupProfile(
        id=1,
        startup_name="DevBridge",
        description="Developer collaboration platform",
        industry="Developer Tools",
        stage="Seed",
        pitch_deck_url=None,
        founders="Amina, Rayan",
        funding_needed=300000,
        owner_id=None,
    )
    strong_match = InvestorProfile(
        id=1,
        investor_name="Atlas",
        interests="Seed, developer tools",
        funding_range=300000,
        preferred_industries="developer tools, ai",
        owner_id=None,
    )
    weak_match = InvestorProfile(
        id=2,
        investor_name="Generalist",
        interests="Series A, fintech",
        funding_range=1500000,
        preferred_industries="fintech",
        owner_id=None,
    )

    ranked = rank_investors_for_startup(startup, [weak_match, strong_match])

    assert ranked[0]["investor_name"] == "Atlas"
    assert ranked[0]["match_score"] >= ranked[1]["match_score"]

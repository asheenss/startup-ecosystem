import pytest
import asyncio
from unittest.mock import patch
from app.models.ai_analysis import AIAnalysis
from app.services.agents.protocol import ProtocolResponse

@pytest.mark.asyncio
async def test_upload_and_analyze_pitch_deck(client, seeded_users, db_session):
    founder, _ = seeded_users
    # Create a startup for the founder
    from app.models.startup_profile import StartupProfile
    startup = StartupProfile(
        startup_name="Test Startup",
        description="Test description",
        industry="Tech",
        stage="Seed",
        founders="Test Founder",
        funding_needed=100000,
        owner_id=founder.id
    )
    db_session.add(startup)
    db_session.commit()
    db_session.refresh(startup)

    # 1. Upload
    files = {"file": ("test.pdf", b"pdf content", "application/pdf")}
    upload_response = client.post(
        f"/api/pitch/upload",
        data={"startup_id": startup.id},
        files=files
    )
    assert upload_response.status_code == 200
    pitch_id = upload_response.json()["pitch_id"]

    # 2. Analyze
    with patch("app.api.routes.pitch.process_pitch_deck") as mock_task:
        analyze_response = client.post(f"/api/pitch/analyze/{pitch_id}")
        assert analyze_response.status_code == 202
        analysis_id = analyze_response.json()["analysis_id"]

        # Verify DB record creation
        analysis = db_session.query(AIAnalysis).filter(AIAnalysis.id == analysis_id).first()
        assert analysis is not None
        assert analysis.status == "pending"

@pytest.mark.asyncio
async def test_get_dashboard_caching(client, seeded_users):
    founder, _ = seeded_users
    
    # First request - should fetch from DB and cache
    with patch("app.api.routes.dashboard.founder_dashboard") as mock_dash:
        mock_dash.return_value = {"startup_overview": {"name": "Test Startup"}}
        
        # We need to mock the cache service to verify it's being used
        with patch("app.api.routes.dashboard.cache") as mock_cache:
            mock_cache.get.return_value = None # Cache miss
            
            response = client.get(f"/api/dashboard/founder/{founder.id}")
            assert response.status_code == 200
            assert response.json()["startup_overview"]["name"] == "Test Startup"
            
            # Verify cache set was called
            assert mock_cache.set.called
            
            # Second request - should fetch from cache
            mock_cache.get.return_value = {"startup_overview": {"name": "Cached Startup"}}
            response = client.get(f"/api/dashboard/founder/{founder.id}")
            assert response.status_code == 200
            assert response.json()["startup_overview"]["name"] == "Cached Startup"
            # Verify dash service NOT called again
            assert mock_dash.call_count == 1

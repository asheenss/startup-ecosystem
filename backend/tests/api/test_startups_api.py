def test_create_and_list_startups(client):
    payload = {
        "startup_name": "Orbit Forge",
        "description": "Infra tooling for startups building internal AI platforms.",
        "industry": "Developer Tools",
        "stage": "Seed",
        "pitch_deck_url": None,
        "founders": "Amina, Sami",
        "funding_needed": 500000,
        "owner_id": None,
    }

    create_response = client.post("/api/startups", json=payload)
    list_response = client.get("/api/startups")

    assert create_response.status_code == 200
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["startup_name"] == "Orbit Forge"

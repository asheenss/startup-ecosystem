def test_connection_request_rejects_self_request(client, seeded_users):
    founder, _ = seeded_users

    response = client.post(
        "/api/connections/request",
        json={"sender_id": founder.id, "receiver_id": founder.id, "note": "Let's connect"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot create a connection request to yourself"


def test_connection_request_rejects_duplicates(client, seeded_users):
    founder, investor = seeded_users
    payload = {"sender_id": founder.id, "receiver_id": investor.id, "note": "Intro request"}

    first_response = client.post("/api/connections/request", json=payload)
    second_response = client.post("/api/connections/request", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Connection request already exists"

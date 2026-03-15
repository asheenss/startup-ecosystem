from datetime import datetime, timedelta

from app.models.event import Event


def test_register_for_event_prevents_duplicate_registration(client, db_session, seeded_users):
    founder, _ = seeded_users
    event = Event(
        title="Founder Dinner",
        description="Private dinner for founders and investors.",
        location="Dubai",
        event_date=datetime.utcnow() + timedelta(days=1),
        organizer_name="Platform",
        capacity=10,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    first_response = client.post(f"/api/events/{event.id}/register", json={"user_id": founder.id})
    second_response = client.post(f"/api/events/{event.id}/register", json={"user_id": founder.id})

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "User is already registered for this event"


def test_register_for_event_blocks_capacity_overflow(client, db_session, seeded_users):
    founder, investor = seeded_users
    event = Event(
        title="Invite-only Roundtable",
        description="Small roundtable for two ecosystem participants.",
        location="Dubai",
        event_date=datetime.utcnow() + timedelta(days=2),
        organizer_name="Platform",
        capacity=1,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    first_response = client.post(f"/api/events/{event.id}/register", json={"user_id": founder.id})
    second_response = client.post(f"/api/events/{event.id}/register", json={"user_id": investor.id})

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Event capacity has been reached"

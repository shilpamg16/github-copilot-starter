def test_signup_adds_student_to_activity(client):
    email = "new-student@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for Chess Club"
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregistering_student_removes_their_email(client):
    email = "new-student@mergington.edu"

    client.post(f"/activities/Chess Club/signup?email={email}")
    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unknown_activity_returns_not_found(client):
    response = client.post("/activities/Unknown Club/signup?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

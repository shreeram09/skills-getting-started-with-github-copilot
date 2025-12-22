from fastapi.testclient import TestClient
from src.main import create_app


def test_signup_new_student():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data

    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # signing up again should fail
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"

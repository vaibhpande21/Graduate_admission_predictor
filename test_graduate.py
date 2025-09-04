import pytest
from graduate import app


## proxy to a live server
@pytest.fixture
def client():
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>🎓 Graduate Admission Predictor is Running!</h1>"


def test_predict(client):
    test_data = {
        "gre": 320,
        "toefl": 110,
        "rating": 5,
        "sop": 4.5,
        "lor": 4.0,
        "cgpa": 9.0,
        "research": 1,
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "chance_of_admit" in response.json
    assert "numeric_score" in response.json
    assert "status" in response.json
    assert response.json["numeric_score"] >= 0
    assert response.json["numeric_score"] <= 100
    assert isinstance(response.json["status"], str)
    assert response.json["status"] == "Excellent chances! 🎯"

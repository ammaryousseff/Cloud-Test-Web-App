from app import app


def test_home_route() -> None:
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert "message" in data


def test_health_route() -> None:
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_dashboard_route() -> None:
    client = app.test_client()
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Cloud Deployment Test" in response.data

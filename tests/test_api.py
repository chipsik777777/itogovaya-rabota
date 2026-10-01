from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    """Проверка доступности эндпоинта /health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_endpoint_structure():
    """Проверка корректности структуры ответа /process (работает даже при fallback)."""
    payload = {
        "text": "Искусственный интеллект ускоряет разработку программного обеспечения.",
        "max_words": 5
    }
    response = client.post("/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "cached" in data
    assert isinstance(data["cached"], bool)
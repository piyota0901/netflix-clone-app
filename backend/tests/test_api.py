from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

def test_health():
    """ヘルスチェックのテスト
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
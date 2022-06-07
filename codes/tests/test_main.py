from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'name': 'RSS Reader',
        'Docs': '{base_url}/docs',
    }


def test_403():
    response = client.get('/publishers/publishers/?publisher_name=Google%20News')
    assert response.status_code == 403
    assert response.json() == {
        'detail': 'Not authenticated',
    }


def test_404():
    response = client.get('/not/existed/url')
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Not Found',
    }

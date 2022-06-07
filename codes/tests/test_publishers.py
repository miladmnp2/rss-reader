from fastapi.testclient import TestClient
from pytest import fixture

from db import database
from main import app


@fixture()
def client():
    with TestClient(app) as client:
        yield client


async def test_get_publisher(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get(
        '/publishers/publishers/?publisher_name=Google News',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert response.status_code == 200
    assert response.json()[0] == {
        'id': 1,
        'name': 'Google News',
        'description': 'Comprehensive up-to-date news coverage, aggregated '
                       'from sources all over the world by Google News.'
    }


async def test_get_invalid_publisher(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get(
        '/publishers/publishers/?publisher_name=Invalid Publisher',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_subscribe(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.post('/publishers/subscribe/?publisher_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 201
    assert response.json()['success']


async def test_get_subscribed(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/publishers/subscribed', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) > 0

from fastapi.testclient import TestClient
from pytest import fixture

from db import database
from main import app


@fixture()
def client():
    with TestClient(app) as client:
        yield client


async def test_get_user(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/users/users/?username=admin', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json()[0] == {
        'username': 'admin',
        'id': 1,
        'role': 'admin'
    }


async def test_get_invalid_user(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/users/users/?username=invalid_username', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_make_admin(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.put(f'/users/2/make-admin', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 204

async def test_get_make_scraper(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.put(f'/users/2/make-scraper', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 204


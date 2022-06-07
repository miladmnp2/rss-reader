from fastapi.testclient import TestClient
from pytest import fixture

from db import database
from main import app


@fixture()
def client():
    with TestClient(app) as client:
        yield client


async def test_get_feeds(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/feeds/?publisher_id=2', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_get_feeds_for_non_existant_publisher(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/feeds/?publisher_id=222222222', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_like(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.post('/feeds/like/?feed_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json()['success']


async def test_liked(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/liked', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_unlike(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.delete('/feeds/unlike/?feed_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json()['success']


async def test_comment(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.post('/feeds/comments/', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'feed_id': 1,
        'text': 'text'
    })
    assert response.status_code == 200
    assert response.json()['success']


async def test_get_comments(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/comments/?feed_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) > 0

async def test_get_comments_for_non_existant_feed(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/comments/?feed_id=111111111', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_uncomment(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.delete('/feeds/uncomment/?comment_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json()['success']


async def test_view(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.post('/feeds/view/?feed_id=1', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json()['success']


async def test_seen(client):
    # login
    response = client.post('/users/login/', json={
        'username': 'admin',
        'password': 'password',
    })
    token = response.json()['token']

    response = client.get('/feeds/seen', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert 'id' in response.json()[0]
    assert 'link' in response.json()[0]
    assert 'title' in response.json()[0]
    assert 'created_at' in response.json()[0]

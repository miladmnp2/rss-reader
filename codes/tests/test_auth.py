from random import randint

from fastapi.testclient import TestClient
from pytest import fixture

from db import database
from main import app

user = 'test%d' % randint(1001, 9999)


@fixture()
def client():
    with TestClient(app) as client:
        yield client


async def test_register(client):
    response = client.post('/users/register/', json={
        'username': user,
        'password': 'test',
    })
    assert response.status_code == 201
    assert 'token' in response.json()


async def test_register_duplicated_username(client):
    response = client.post('/users/register/', json={
        'username': user,
        'password': 'test'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'User with this username already exists',
    }


async def test_login(client):
    response = client.post('/users/login/', json={
        'username': user,
        'password': 'test',
    })
    assert response.status_code == 200
    assert 'token' in response.json()
    assert response.json()['role'] == 'reader'


async def test_login_invalid_username(client):
    response = client.post('/users/login/', json={
        'username': 'an-invalid-username',
        'password': 'test',
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Wrong username or password',
    }


async def test_login_invalid_password(client):
    response = client.post('/users/login/', json={
        'username': user,
        'password': 'an-invalid-password',
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Wrong username or password',
    }

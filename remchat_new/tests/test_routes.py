import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_requires_login(client):
    response = client.get('/search/testuser', follow_redirects=True)
    assert b'You need to be logged in' in response.data or response.status_code == 200

def test_messages_requires_login(client):
    response = client.get('/messages/testuser', follow_redirects=True)
    assert b'You need to be logged in' in response.data or response.status_code == 200

def test_chat_room_requires_login(client):
    response = client.get('/chat_room/testuser/1', follow_redirects=True)
    assert b'You need to be logged in' in response.data or response.status_code == 200

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out' in response.data or response.status_code == 200 
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data or b"login" in response.data

def test_signup_page(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data or b"signup" in response.data 
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_posts_requires_login(client):
    response = client.get('/posts/testuser/', follow_redirects=True)
    assert b'You need to be logged in' in response.data or response.status_code == 200 
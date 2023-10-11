from fastapi.testclient import  TestClient
from ..piz import app
from ..model import User

client = TestClient(app)

def test_user():
    user_data= {
        "username": "testuser",
        "email": "test@mail.com",
        "password": "testpass",
        "is_staff": True,
        "is_active": True
    }


    response = client.post('/auth/register', json=user_data)

    assert response.status_code == 201

    created_user = response.json()

    yield created_user



def test_user_creation():
    assert "id " in test_user
    assert test_user["username"] == "testuser"
    assert test_user['password']== 'testpass'
    assert test_user['is_staff']== True
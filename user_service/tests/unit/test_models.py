import pytest
from user_service.app.models import User

def test_user_creation():
    user = User(
        id=1,
        name="John",
        surname="Doe",
        username="johndoe",
        password_hash="hashed_pw",
        born_date="2000-01-01"
    )
    assert user.name == "John"
    assert user.username == "johndoe"


import pytest
from src.db_package import database_ORM

###chatGTP
user_packet = {
    "username": "testuser",
    "password": "securepassword123",  # hash this later if you haven't yet
    "email": "testuser@example.com",
    "address": "123 Main Street, Springfield",
    "phoneNumber": "555-123-4567",
    "description": "Test user account for database insertion"
}
###end chatGPT


def test_user():
    """Test creating a new user"""
    print("running_test user")
    user = database_ORM.User(
                username= user_packet["username"],  # type: ignore
                password= user_packet["password"], # type: ignore
                email= user_packet["email"], # type: ignore
                address= user_packet["address"], # type: ignore
                phoneNumber= user_packet["phoneNumber"], # type: ignore
                description= user_packet["description"] # type: ignore
                )
    
    assert user.username == 'testuser'





'''
User resource tests
'''

import pytest
import json
from vainamoinen.database import User
from vainamoinen import db, create_app


@pytest.fixture
def client():
    '''
    Create a test client for tests
    '''

    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "TESTING": True,
        #"CACHE_TYPE": "SimpleCache"
    }

    app = create_app(config)

    ctx = app.app_context()
    ctx.push()

    with app.app_context():
        db.create_all()
    _populate_db()

    yield app.test_client()

    db.session.rollback()
    db.drop_all()
    db.session.remove()
    ctx.pop()


def _populate_db():
    '''
    Populate database with test users
    '''
    user_json = _get_user_json(1)
    user = User()
    user.deserialize(user_json)
    db.session.add(user)

    user_json = _get_user_json(2)
    user = User()
    user.deserialize(user_json)
    db.session.add(user)

    db.session.commit()


def _get_user_json(number):
    '''
    Creates a valid user JSON object to be used for PUT and POST tests.
    '''
    return {
        "username": "test-user-{}".format(number),
        "password": "1234",
        "email": "email{}.com".format(number),
        "address": "Test Street 1",
        "phone_number": "123 456 7890",
        "description": "This is a Test User"
    }


class TestUserCollection:
    RESOURCE_URL = "/api/users"

    def test_get_users(self, client):
        '''
        Test getting all users
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)

        assert len(body) == 2

        for user in body:
            assert "username" in user
            assert "email" in user

    def test_post_user(self, client):
        '''
        Test posting a new user
        '''
        user = _get_user_json(3)
        resp = client.post(self.RESOURCE_URL, json=user)
        assert resp.status_code == 201

    def test_post_name_conflict(self, client):
        '''
        Test posting an existing user
        '''
        user = _get_user_json(1)
        resp = client.post(self.RESOURCE_URL, json=user)
        assert resp.status_code == 409

    def test_post_wrong_mediatype(self, client):
        '''
        Test posting with wrong mediatype
        '''
        resp = client.post(self.RESOURCE_URL, data="notJSON")
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        '''
        Test posting with missing fields
        '''
        user = _get_user_json(3)
        user.pop("phone_number")
        resp = client.post(self.RESOURCE_URL, json=user)
        assert resp.status_code == 400



class TestUserItem:
    RESOURCE_URL = "/api/users/test-user-1"
    INVALID_USER_URL = "/api/users/invalid-user-x"

    def test_get(self, client):
        '''
        Test getting a specific user
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "username" in body
        assert "email" in body
        assert body["username"] == "test-user-1"
        assert body["email"] == "email1.com"

    def test_get_not_found(self, client):
        '''
        Test getting a non-existent user
        '''
        resp = client.get(self.INVALID_USER_URL)
        assert resp.status_code == 404



    def test_put_valid_request(self, client):
        '''
        Test updating a user with valid data
        '''
        valid = _get_user_json(1)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

    def test_put_wrong_mediatype(self, client):
        '''
        Test updating a user with wrong mediatype
        '''
        resp = client.put(self.RESOURCE_URL, data="notJSON")
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        '''
        Test updating a user with missing fields
        '''
        not_valid = _get_user_json(1)
        not_valid.pop("phone_number")
        resp = client.put(self.RESOURCE_URL, json=not_valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        '''
        Test deleting user
        '''
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        '''
        Test deleting non-existent user
        '''
        resp = client.delete(self.INVALID_USER_URL)
        assert resp.status_code == 404

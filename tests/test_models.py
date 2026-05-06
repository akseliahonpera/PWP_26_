'''
Database model tests
'''

import pytest
from vainamoinen import db, create_app
from vainamoinen.database import User, Job, Timetable
from utils import _get_user_json, _get_job_json, _get_timetable_json

@pytest.fixture
def db_handle():
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "TESTING": True,
        "CACHE_TYPE": "SimpleCache"
    }

    app = create_app(config)

    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()
    _populate_db()
    yield db

    db.session.rollback()
    db.drop_all()
    db.session.remove()
    ctx.pop()

def _populate_db():
    '''
    Populate database for testing
    '''
    User.insert(_get_user_json(number=1))
    User.insert(_get_user_json(number=2))
    Job.insert(_get_job_json(job_number=1, user_number=1))
    Timetable.insert(_get_timetable_json(timetable_number=1, job_number=1, user_number=1))


def test_add_user(db_handle):
    '''
    Add a new user
    '''
    User.insert(_get_user_json(3))
    assert User.query.count() == 3

def test_query_users(db_handle):
    '''
    Query for all users
    '''
    users = User.query_all()
    assert len(users) == 2

def test_query_user(db_handle):
    '''
    Query for a specific user
    '''
    user = User.query_all(_filter_={"username": "test-user-2"})[0]
    assert "username" in user
    assert user["username"] == "test-user-2"

def test_delete_user(db_handle):
    '''
    Delete all users, also check if cascading delete works
    '''
    users = User.query.all()
    for user in users:
        user.delete()
    assert User.query.count() == 0
    assert Job.query.count() == 0
    assert Timetable.query.count() == 0

def test_add_job(db_handle):
    '''
    Add a new job
    '''
    Job.insert(_get_job_json(job_number=2, user_number=1))
    assert Job.query.count() == 2

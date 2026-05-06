'''
Test client and helper functions for testing
'''

import pytest
from vainamoinen.database import User, Job, Timetable, ApiKey
from vainamoinen import db, create_app

API_TEST_KEY = "api_test_key"

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
        db.drop_all()
        db.create_all()
    _populate_db()

    yield app.test_client()

    db.session.rollback()
    db.drop_all()
    db.session.remove()
    ctx.pop()


def _populate_db():
    '''
    Populate database with test users, jobs, timetables
    '''
    user_json = _get_user_json(1)
    user = User()
    user.deserialize(user_json)
    db.session.add(user)

    user_json = _get_user_json(2)
    user = User()
    user.deserialize(user_json)
    db.session.add(user)

    job_json = _get_job_json(job_number=1, user_number=1)
    job = Job()
    job.deserialize(job_json)
    db.session.add(job)

    timetable_json = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
    timetable = Timetable()
    timetable.deserialize(timetable_json)
    db.session.add(timetable)

    timetable_json = _get_timetable_json(timetable_number=2, job_number=1, user_number=1)
    timetable = Timetable()
    timetable.deserialize(timetable_json)
    db.session.add(timetable)

    db_key = ApiKey(
        key = ApiKey.key_hash(API_TEST_KEY),
        admin = True
    )
    db.session.add(db_key)

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

def _get_job_json(job_number, user_number):
    '''
    Creates a valid job JSON object to be used for PUT and POST tests.
    '''

    user = _get_user_json(user_number)

    return {
        "username": user["username"],
        "job_name": "test-job-{}".format(job_number),
        "job_description": "test description",
        "latitude":"12",
        "longitude":"34",
        "location": "test location",
        "opening_hours": "test hours",
        "category": "test category",
    }

def _get_timetable_json(timetable_number, job_number, user_number):
    '''
    Creates a valid timetable JSON object to be used for PUT and POST tests.
    '''

    user = _get_user_json(user_number)
    job = _get_job_json(job_number=job_number, user_number=user_number)


    return {
        "job_name": "test-job-{}".format(job_number),
        "title": "test-title-{}".format(timetable_number),
        "start_time": "2026-03-09T15:00:00",
        "end_time": "2026-03-09T16:00:00",
        "is_booked": False
    }

def _headers(json=True):
    '''
    Returns valid headers with test api key and content type set to JSON.
    However, if json=False, gives invalid content type for testing.
    '''
    content_type = "application/json"
    if not json:
        content_type = "text/plain"
    return {
        "Vainamoinen-Api-Key": API_TEST_KEY,
        "Content-Type": content_type
    }

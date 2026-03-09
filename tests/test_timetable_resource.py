'''
Timetable resource tests
'''

import pytest
import json
from vainamoinen.database import Timetable, User, Job
from vainamoinen import db, create_app
from test_user_resource import _get_user_json
from test_job_resource import _get_job_json

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
    Populate database with a test timetable
    '''
    user_json = _get_user_json(1)
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

    db.session.commit()


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


class TestTimeTableCollection:
    RESOURCE_URL = "/api/jobs/test-job-1/timetables"

    def test_get_timetables(self, client):
        '''
        Test getting all timetables
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)

        assert len(body) == 2

        for timetable in body:
            assert "title" in timetable

    def test_post_timetable(self, client):
        '''
        Test posting a new timetable succesfully
        '''
        timetable = _get_timetable_json(timetable_number=3, job_number=1, user_number=1)
        resp = client.post(self.RESOURCE_URL, json=timetable)
        assert resp.status_code == 201

    def test_post_name_conflict(self, client):
        '''
        Test posting an existing timetable
        '''
        timetable = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        resp = client.post(self.RESOURCE_URL, json=timetable)
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
        timetable = _get_timetable_json(timetable_number=2, job_number=1, user_number=1)
        timetable.pop("is_booked")
        resp = client.post(self.RESOURCE_URL, json=timetable)
        assert resp.status_code == 400



class TestTimeTableItem:
    RESOURCE_URL = "/api/jobs/test-job-1/timetables/test-title-1"
    INVALID_TIMETABLE_URL = "/api/jobs/test-job-1/timetables/invalid-title-x"

    def test_get(self, client):
        '''
        Test getting a specific timetable
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "title" in body
        assert body["title"] == "test-title-1"

    def test_get_not_found(self, client):
        '''
        Test getting a non-existent timetable
        '''
        resp = client.get(self.INVALID_TIMETABLE_URL)
        assert resp.status_code == 404



    def test_put_valid_request(self, client):
        '''
        Test updating a timetable with valid data
        '''
        valid = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        valid["is_booked"]=True
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

    def test_put_wrong_mediatype(self, client):
        '''
        Test updating a timetable with wrong mediatype
        '''
        resp = client.put(self.RESOURCE_URL, data="notJSON")
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        '''
        Test updating a timetable with missing fields
        '''
        not_valid = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        not_valid.pop("is_booked")
        resp = client.put(self.RESOURCE_URL, json=not_valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        '''
        Test deleting timetable
        '''
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        '''
        Test deleting non-existent timetable
        '''
        resp = client.delete(self.INVALID_TIMETABLE_URL)
        assert resp.status_code == 404

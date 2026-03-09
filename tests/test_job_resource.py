'''
Job resource tests
'''

import pytest
import json
from vainamoinen.database import User, Job
from vainamoinen import db, create_app
from test_user_resource import _get_user_json

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

    job_json = _get_job_json(job_number=1, user_number=1)
    job = Job()
    job.deserialize(job_json)
    db.session.add(job)

    db.session.commit()


def _get_job_json(job_number, user_number):
    '''
    Creates a valid job JSON object to be used for PUT and POST tests.
    '''

    user = _get_user_json(user_number)

    return {
        "username": user["username"],
        "job_name": "test-job-{}".format(job_number),
        "job_description": "test description",
        "location": "test location",
        "opening_hours": "test hours",
        "category": "test category",
    }


class TestJobCollection:
    RESOURCE_URL = "/api/jobs"

    def test_get_jobs(self, client):
        '''
        Test getting all jobs
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)

        assert len(body) == 1

        for job in body:
            assert "job_name" in job

    def test_post_job(self, client):
        '''
        Test posting a new job succesfully
        '''
        job = _get_job_json(job_number=2, user_number=1)
        resp = client.post(self.RESOURCE_URL, json=job)
        assert resp.status_code == 201

    def test_post_name_conflict(self, client):
        '''
        Test posting an existing job
        '''
        job = _get_job_json(job_number=1, user_number=1)
        resp = client.post(self.RESOURCE_URL, json=job)
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
        job = _get_job_json(job_number=2, user_number=1)
        job.pop("location")
        resp = client.post(self.RESOURCE_URL, json=job)
        assert resp.status_code == 400



class TestJobItem:
    RESOURCE_URL = "/api/jobs/test-job-1"
    INVALID_JOB_URL = "/api/jobs/invalid-job-x"

    def test_get(self, client):
        '''
        Test getting a specific job
        '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "job_name" in body
        assert body["job_name"] == "test-job-1"

    def test_get_not_found(self, client):
        '''
        Test getting a non-existent job
        '''
        resp = client.get(self.INVALID_JOB_URL)
        assert resp.status_code == 404



    def test_put_valid_request(self, client):
        '''
        Test updating a job with valid data
        '''
        valid = _get_job_json(job_number=1, user_number=1)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

    def test_put_wrong_mediatype(self, client):
        '''
        Test updating a job with wrong mediatype
        '''
        resp = client.put(self.RESOURCE_URL, data="notJSON")
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        '''
        Test updating a job with missing fields
        '''
        not_valid = _get_job_json(job_number=1, user_number=1)
        not_valid.pop("location")
        resp = client.put(self.RESOURCE_URL, json=not_valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        '''
        Test deleting job
        '''
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        '''
        Test deleting non-existent job
        '''
        resp = client.delete(self.INVALID_JOB_URL)
        assert resp.status_code == 404

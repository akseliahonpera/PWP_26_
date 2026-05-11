'''
Job resource tests
'''

from utils import client, _get_user_json, _get_job_json, _headers
import json

class TestJobCollection:
    RESOURCE_URL = "/api/jobs"

    def test_get_jobs(self, client):
        '''
        Test getting all jobs
        '''
        resp = client.get(
            self.RESOURCE_URL,
            headers = _headers()
        )
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
        resp = client.post(
            self.RESOURCE_URL,
            json=job,
            headers = _headers()
        )
        assert resp.status_code == 201

    def test_post_name_conflict(self, client):
        '''
        Test posting an existing job
        '''
        job = _get_job_json(job_number=1, user_number=1)
        resp = client.post(
            self.RESOURCE_URL,
            json=job,
            headers = _headers()
        )
        assert resp.status_code == 409

    def test_post_wrong_mediatype(self, client):
        '''
        Test posting with wrong mediatype
        '''
        resp = client.post(
            self.RESOURCE_URL,
            data="notJSON",
            headers = _headers(json=False)
        )
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        '''
        Test posting with missing fields
        '''
        job = _get_job_json(job_number=2, user_number=1)
        job.pop("location")
        resp = client.post(
            self.RESOURCE_URL,
            json=job,
            headers = _headers()
        )
        assert resp.status_code == 400



class TestJobItem:
    RESOURCE_URL = "/api/jobs/test-job-1"
    INVALID_JOB_URL = "/api/jobs/invalid-job-x"

    def test_get(self, client):
        '''
        Test getting a specific job
        '''
        resp = client.get(
            self.RESOURCE_URL,
            headers = _headers()
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "job_name" in body
        assert body["job_name"] == "test-job-1"

    def test_get_not_found(self, client):
        '''
        Test getting a non-existent job
        '''
        resp = client.get(
            self.INVALID_JOB_URL,
            headers = _headers()
        )
        assert resp.status_code == 404



    def test_put_valid_request(self, client):
        '''
        Test updating a job with valid data
        '''
        valid = _get_job_json(job_number=1, user_number=1)
        resp = client.put(
            self.RESOURCE_URL,
            json=valid,
            headers = _headers()
        )
        assert resp.status_code == 204

    def test_put_wrong_mediatype(self, client):
        '''
        Test updating a job with wrong mediatype
        '''
        resp = client.put(
            self.RESOURCE_URL,
            data="notJSON",
            headers = _headers(json=False)
        )
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        '''
        Test updating a job with missing fields
        '''
        not_valid = _get_job_json(job_number=1, user_number=1)
        not_valid.pop("location")
        resp = client.put(
            self.RESOURCE_URL,
            json=not_valid,
            headers = _headers()
        )
        assert resp.status_code == 400

    def test_delete(self, client):
        '''
        Test deleting job
        '''
        resp = client.delete(
            self.RESOURCE_URL,
            headers = _headers()
        )
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        '''
        Test deleting non-existent job
        '''
        resp = client.delete(
            self.INVALID_JOB_URL,
            headers = _headers()
        )
        assert resp.status_code == 404

    def test_cascade_delete(self, client):
        '''
        Test deleting a user, to see if their job is also deleted
        '''
        # Check that job exists first
        resp = client.get(
            "/api/jobs/test-job-1",
            headers = _headers()
        )
        assert resp.status_code == 200

        # Delete the user who owns the job
        resp = client.delete(
            "/api/users/test-user-1",
            headers = _headers()
        )
        assert resp.status_code == 204

        # Try to get the same job after deleting the user
        resp = client.get(
            "/api/jobs/test-job-1",
            headers = _headers()
        )
        assert resp.status_code == 404



class TestUserItemsJobCollection:
    RESOURCE_URL_1 = "/api/users/test-user-1/jobs"
    RESOURCE_URL_2 = "/api/users/test-user-2/jobs"

    def test_get(self, client):
        '''
        Test getting users' jobs
        test_user_1 should have 1 job.
        test_user_2 should have 0 jobs
        '''
        resp = client.get(
            self.RESOURCE_URL_1,
            headers = _headers()
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1

        resp = client.get(
            self.RESOURCE_URL_2,
            headers = _headers()
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 0

    #TODO: more tests

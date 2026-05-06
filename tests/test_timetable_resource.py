'''
Timetable resource tests
'''

from utils import client, _get_user_json, _get_job_json, _get_timetable_json, _headers
import json

class TestTimeTableCollection:
    RESOURCE_URL = "/api/jobs/test-job-1/timetables"

    def test_get_timetables(self, client):
        '''
        Test getting all timetables
        '''
        resp = client.get(
            self.RESOURCE_URL,
            headers = _headers()
        )
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
        resp = client.post(
            self.RESOURCE_URL, 
            json=timetable,
            headers = _headers()
        )
        assert resp.status_code == 201

    def test_post_name_conflict(self, client):
        '''
        Test posting an existing timetable
        '''
        timetable = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        resp = client.post(
            self.RESOURCE_URL, 
            json=timetable,
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
        timetable = _get_timetable_json(timetable_number=2, job_number=1, user_number=1)
        timetable.pop("is_booked")
        resp = client.post(
            self.RESOURCE_URL, 
            json=timetable,
            headers = _headers()
        )
        assert resp.status_code == 400



class TestTimeTableItem:
    RESOURCE_URL = "/api/jobs/test-job-1/timetables/test-title-1"
    INVALID_TIMETABLE_URL = "/api/jobs/test-job-1/timetables/invalid-title-x"

    def test_get(self, client):
        '''
        Test getting a specific timetable
        '''
        resp = client.get(
            self.RESOURCE_URL,
            headers = _headers()
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "title" in body
        assert body["title"] == "test-title-1"

    def test_get_not_found(self, client):
        '''
        Test getting a non-existent timetable
        '''
        resp = client.get(
            self.INVALID_TIMETABLE_URL,
            headers = _headers()
        )
        assert resp.status_code == 404



    def test_put_valid_request(self, client):
        '''
        Test updating a timetable with valid data
        '''
        valid = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        valid["is_booked"]=True
        resp = client.put(
            self.RESOURCE_URL, 
            json=valid,
            headers = _headers()
        )
        assert resp.status_code == 204

    def test_put_wrong_mediatype(self, client):
        '''
        Test updating a timetable with wrong mediatype
        '''
        resp = client.put(
            self.RESOURCE_URL, 
            data="notJSON",
            headers = _headers(json=False)
        )
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        '''
        Test updating a timetable with missing fields
        '''
        not_valid = _get_timetable_json(timetable_number=1, job_number=1, user_number=1)
        not_valid.pop("is_booked")
        resp = client.put(
            self.RESOURCE_URL, 
            json=not_valid,
            headers = _headers()
        )
        assert resp.status_code == 400

    def test_delete(self, client):
        '''
        Test deleting timetable
        '''
        resp = client.delete(
            self.RESOURCE_URL,
            headers = _headers()
        )
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        '''
        Test deleting non-existent timetable
        '''
        resp = client.delete(
            self.INVALID_TIMETABLE_URL,
            headers = _headers()
        )
        assert resp.status_code == 404

    def test_cascade_delete(self, client):
        '''
        Test deleting a job, to see if their timetable is also deleted
        '''
        # Check that timetable exists first
        resp = client.get(
            "/api/jobs/test-job-1/timetables/test-title-1",
            headers = _headers()
        )
        assert resp.status_code == 200

        # Delete the job that owns the timetable
        resp = client.delete(
            "/api/jobs/test-job-1",
            headers = _headers()
        )
        assert resp.status_code == 204

        # Try to get the same timetable after deleting the job
        resp = client.get(
            "/api/jobs/test-job-1/timetables/test-title-1",
            headers = _headers()
        )
        assert resp.status_code == 404

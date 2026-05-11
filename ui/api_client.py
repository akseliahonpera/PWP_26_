'''
Very important module docstring
Contains APIClient
'''
import requests

class APIClient:
    '''
    Client class that connects UI with API backend with HTTP requests
    '''
    def __init__(self):
        self.api_key = None
        self.ip = "http://localhost:5000/api"
        self.user = ""

    def set_api_key(self, key):
        '''
        Sets the api key, needed in some calls and included in all (even if for no effect)
        '''
        self.api_key = key

    def set_ip(self, ip="", localhost=False):
        '''
        Sets ip address to be used in all API calls
        (no check for validity, inform UI user)

        ip MUST include "/api" at the end for function calls to work, inform UI user
        (I'm not writing an ip checker and this crudeness will be just fine for this project)
        '''
        if localhost:
            self.ip = "http://localhost:5000/api"
        elif ip != "":
            self.ip = ip

    def set_user(self, user):
        '''
        Sets the username of the current user who logs in
        Used to get data of own account
        '''
        self.user = user

    def _headers(self):
        return {"Vainamoinen-Api-Key": self.api_key,
                "Content-Type": "application/json"
                }


    ############################
    # /jobs functions          #
    ############################

    def get_all_jobs(self):
        '''
        API call
        Get all jobs
        '''
        return requests.get(
            f"{self.ip}/jobs",
            headers=self._headers(),
            timeout=5.0
        )

    def post_job(self, job):
        '''
        API call
        Post a new job
        '''
        return requests.post(
            f"{self.ip}/jobs",
            json=job,
            headers=self._headers(),
            timeout=5.0
        )

    def delete_job(self, job_name):
        '''
        API call
        Delete a job
        '''
        return requests.delete(
            f"{self.ip}/jobs/{job_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_job(self, job_name):
        '''
        API call
        Get a specific job
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_job(self, job):
        '''
        API call
        Update a job with new data
        '''
        return requests.put(
            f"{self.ip}/jobs/{job['job_name']}",
            json=job,
            headers=self._headers(),
            timeout=5.0
        )

    ############################
    # /timetables functions    #
    ############################

    def get_timetables(self, job_name):
        '''
        API call
        Get all timetables of a job
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}/timetables",
            headers=self._headers(),
            timeout=5.0
        )

    def post_timetable(self, job_name, timetable):
        '''
        API Call
        Post a new timetable for a job
        '''
        return requests.post(
            f"{self.ip}/jobs/{job_name}/timetables",
            json=timetable,
            headers=self._headers(),
            timeout=5.0
        )

    def delete_timetable(self, job_name, timetable_name):
        '''
        API call
        Delete a timetable
        '''
        return requests.delete(
            f"{self.ip}/jobs/{job_name}/timetables/{timetable_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_timetable(self, job_name, timetable_name):
        '''
        API call
        Get a specific timetable
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}/timetables/{timetable_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_timetable(self, job_name, timetable):
        '''
        API call
        Update a timetable with new data
        '''
        return requests.put(
            f"{self.ip}/jobs/{job_name}/timetables/{timetable['title']}",
            json=timetable,
            headers=self._headers(),
            timeout=5.0
        )


    ############################
    # /users functions         #
    ############################

    def get_users(self):
        '''
        API call
        Get all users
        '''
        return requests.get(
            f"{self.ip}/users",
            headers=self._headers(),
            timeout=5.0
        )

    def post_user(self, user):
        '''
        API call
        Post a new user
        '''
        return requests.post(
            f"{self.ip}/users",
            json=user,
            headers=self._headers(),
            timeout=5.0
        )

    def delete_user(self, user_name):
        '''
        API call
        Delete a user
        '''
        return requests.delete(
            f"{self.ip}/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_user(self, user_name):
        '''
        API call
        Get a specific user
        '''
        return requests.get(
            f"{self.ip}/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_user(self, user):
        '''
        API call
        Update a user with new data
        '''
        return requests.put(
            f"{self.ip}/users/{user['user_name']}",
            json=user,
            headers=self._headers(),
            timeout=5.0
        )

    def get_user_jobs(self, user_name):
        '''
        API call
        Get jobs of a user
        '''
        return requests.get(
            f"{self.ip}/users/{user_name}/jobs",
            headers=self._headers(),
            timeout=5.0
        )


    ############################
    # /public/users functions  #
    ############################

    def get_users_public(self):
        '''
        API call
        Get all users
        '''
        return requests.get(
            f"{self.ip}/public/users",
            headers=self._headers(),
            timeout=5.0
        )

    def get_user_public(self, user_name):
        '''
        API call
        Get a user
        '''
        return requests.get(
            f"{self.ip}/public/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

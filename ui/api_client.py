import requests

class APIClient:
    def __init__(self):
        self.api_key = None
        self.ip = "http://localhost:5000/api"
    
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
        else:
            self.ip = ip
 

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
        '''
        return requests.get(
            f"{self.ip}/jobs",
            headers=self._headers(),
            timeout=5.0
        )

    def post_job(self, job):
        '''
        API call
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
        '''
        return requests.delete(
            f"{self.ip}/jobs/{job_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_job(self, job_name):
        '''
        API call
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_job(self, job):
        '''
        API call
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
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}/timetables",
            headers=self._headers(),
            timeout=5.0
        )

    def delete_timetable(self, job_name, timetable_name):
        '''
        API call
        '''
        return requests.delete(
            f"{self.ip}/jobs/{job_name}/timetables/{timetable_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_timetable(self, job_name, timetable_name):
        '''
        API call
        '''
        return requests.get(
            f"{self.ip}/jobs/{job_name}/timetables/{timetable_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_timetable(self, job_name, timetable):
        '''
        API call
        '''
        return requests.get(
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
        '''
        return requests.get(
            f"{self.ip}/users",
            headers=self._headers(),
            timeout=5.0
        )

    def post_user(self, user):
        '''
        API call
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
        '''
        return requests.delete(
            f"{self.ip}/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def get_user(self, user_name):
        '''
        API call
        '''
        return requests.get(
            f"{self.ip}/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

    def update_user(self, user):
        '''
        API call
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
        '''
        return requests.get(
            f"{self.ip}/public/users",
            headers=self._headers(),
            timeout=5.0
        )

    def get_user_public(self, user_name):
        '''
        API call
        '''
        return requests.get(
            f"{self.ip}/public/users/{user_name}",
            headers=self._headers(),
            timeout=5.0
        )

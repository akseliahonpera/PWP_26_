'''
Job resources
'''

from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen.database import Job


class JobItem(Resource):

    def get(self, job):
        '''
        Get a job (mene töihin)
        ---
        description: Get all data associated with a singular job
        parameters:
        - $ref: '#/components/parameters/job'
        responses:
          '200':
            description: All data of the chosen job 
            content:
              application/json:
                example:
                  id: 1
                  username: lawnmowerman734
                  job_name: lawnmowing
                  job_description: I'm available to cut your grass at 15e/hour!
                  location: Oulu area
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00
                  category: Yardwork
        '''
        return Job.serialize(job)

    def put(self, job):
        '''
        Update a job
        ---
        description: Replace a job with new values
        parameters:
        - $ref: '#/components/parameters/job'
        requestBody:
          description: JSON document that contains new data for the job 
          content:
            application/json:
              schema:
                $ref: '#components/schemas/Job'
              example:
                id: 1
                username: lawnmowerman734
                job_name: Smuggling
                job_description: I'm available to deliver contraband items within Finland!
                location: Finland
                created: 2026-04-05 10:24:34.875360
                opening_hours: Mon-Fri 8:00 - 17:00, Sat-Sun 10:00-14:00
                category: Black market
        responses:
          '204':
            description: Job was updated successfully
          '400':                
            description: Server couldn't validate the request
          '409':
            description: A conflict was raised when attempting to update job data
          '415':
            description: Provided media was not valid JSON
          '404':
            description: Job not found
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Job.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            job.update(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in JobItem put."
            )
        return Response(status=204)

    def delete(self, job):
        '''
        Delete a job
        ---
        description: Delete a job from the database
        parameters:
        - $ref: '#/components/parameters/job'
        responses:
          '204':
            description: job deleted successfully
          '409':
            description: A conflict was raised when attempting to delete job data
          '404':
            description: Job not found
        '''
        try:
            job.delete()
        except IntegrityError:
            raise Conflict(
                description="Error in JobItem delete."
            )
        return Response(status=204)


class JobCollection(Resource):

    def get(self):
        '''
        Get all jobs
        ---
        description: Get all jobs
        responses:
          '200':
            description: All data of the chosen job
            content:
              application/json:
                example:
                - id: 1
                  username: lawnmowerman734
                  job_name: Smuggling
                  job_description: I'm available to deliver contraband items within Finland!
                  location: Finland
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00, Sat-Sun 10:00-14:00
                  category: Black market
                - id: 2 
                  username: Jukka751 
                  job_name: Advertisement
                  job_description: I'm available to advertise your business outside with a sign!
                  location: Tampere
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00, Sat 10:00-14:00
                  category: Marketing 
        '''
        return Job.query_all()

    def post(self):
        '''
        Add a new job
        ---
        description: Add a new job to the database
        requestBody:
          description: JSON document that contains all data for the job 
          content:
            application/json:
              schema:
                $ref: '#components/schemas/Job'
              example:
                  id: 2 
                  username: Jukka751 
                  job_name: Advertisement
                  job_description: I'm available to advertise your business outside with a sign!
                  location: Tampere
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00, Sat 10:00-14:00
                  category: Marketing 
        responses:
          '201':
            description: Job was created and uploaded successfully
          '400':
            description: Server couldn't validate the request
          '409':
            description: A conflict was raised when attempting to add the new job
          '415':
            description: Provided media was not valid JSON
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Job.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            job = Job.insert(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in JobCollection post."
            )
        return Response(status=201, headers={"Location":url_for("api.jobitem", job=job)})


class UserItemsJobCollection(Resource):

    def get(self, user):
        '''
        Get user's jobs
        ---
        description: Get all jobs belonging to a specific user
        parameters:
        - $ref: '#/components/parameters/user'
        responses:
          '200':
            description: All data of the chosen job
            content:
              application/json:
                example:
                - id: 1
                  username: lawnmowerman734
                  job_name: Smuggling
                  job_description: I'm available to deliver contraband items within Finland!
                  location: Finland
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00, Sat-Sun 10:00-14:00
                  category: Black market
                - id: 2 
                  username: lawnmowerman734 
                  job_name: Advertisement
                  job_description: I'm available to advertise your business outside with a sign!
                  location: Tampere
                  created: 2026-04-05 10:24:34.875360
                  opening_hours: Mon-Fri 8:00 - 17:00, Sat 10:00-14:00
                  category: Marketing 
        '''
        return Job.query_all(_filter_={"username": user.username})

    # get probably enough

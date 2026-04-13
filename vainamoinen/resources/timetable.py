'''
Timetable resources
'''

from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate, FormatChecker
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen.database import Timetable

class TimeTableItem(Resource):
    '''
    Resource containing all HTTP methods for singular timetable items
    '''

    def get(self, job, timetable):
        '''
        Get a jobs' timetable
        ---
        description: Get timetable associated with a specific job
        parameters:
        - $ref: '#/components/parameters/timetable'
        - $ref: '#/components/parameters/job'
        responses:
          '200':
            description: All data of the chosen timetable
            content:
              application/json:
                examples:
                - id: 1
                  job_name: leafblowing
                  title: TO BE DETERMINED
                  start_time: 2024-04-05 10:24:34.875360
                  end_time: 2027-12-31 10:24:34.875360
                  is_booked: false
                  created: 2024-04-05 10:24:34.875360
                - id: 2
                  job_name: leafblowing
                  title: TO BE DETERMINED
                  is_booked: false
                  created: 2024-04-05 10:24:34.875360
        '''
        return timetable.serialize()

    def put(self, job, timetable):
        '''
        Update a jobs' timetable
        ---
        description: Replace a timetable with new values
        parameters:
        - $ref: '#/components/parameters/timetable'
        - $ref: '#/components/parameters/job'
        requestBody:
          description: JSON document that contains new data for the timetable
          content:
            application/json:
              schema:
                $ref: '#components/schemas/Job'
              example:
                  id: 1
                  job_name: Grass cutting
                  title: TO BE DETERMINED
                  start_time: 2024-04-05 10:24:34.875360
                  end_time: 2029-12-31 10:24:34.875360
                  is_booked: false
                  created: 2024-04-05 10:24:34.875360
        responses:
          '204':
            description: Timetable was updated successfully
          '400':                
            description: Server couldn't validate the request
          '409':
            description: A conflict was raised when attempting to update timetable data
          '415':
            description: Provided media was not valid JSON
          '404':
            description: Timetable not found
        '''
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Timetable.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            timetable.update(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in TimeTableItem put."
            )
        return Response(status=204)

    def delete(self, job, timetable):
        '''
        Delete a jobs' timetable
        ---
        description: Delete a timetable from a job
        parameters:
        - $ref: '#/components/parameters/job'
        - $ref: '#/components/parameters/timetable'
        responses:
          '204':
            description: timetable deleted successfully
          '409':
            description: A conflict was raised when attempting to delete timetable 
          '404':
            description: Timetable not found
        '''
        try:
            timetable.delete()
        except IntegrityError:
            raise Conflict(
                description="Error in TimeTableItem delete."
            )
        return Response(status=204)

class TimeTableCollection(Resource):
    '''
    Resource containing all HTTP methods for timetable collections
    '''

    def get(self, job):
        '''
        Get all timetables of a job
        ---
        description: Get all timetables associated with a specific job
        parameters:
        - $ref: '#/components/parameters/job'
        responses:
          '200':
            description: All data of the chosen timetables
            content:
              application/json:
                example:
                - id: 1
                  job_name: leafblowing
                  title: TO BE DETERMINED
                  start_time: 2024-04-05 10:24:34.875360
                  end_time: 2025-12-31 10:24:34.875360
                  is_booked: false
                  created: 2024-04-05 10:24:34.875360
                - id: 2 
                  job_name: leafblowing
                  title: TO BE DETERMINED
                  start_time: 2026-01-01 10:24:34.875360
                  is_booked: false
                  created: 2024-04-05 10:24:34.875360
        '''
        return Timetable.query_all(_filter_={"job_name": job.job_name})

    #TODO: Is this needed? no other Collection resource has a post. Commenting out for now
    """def post(self, job):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Timetable.json_schema(), format_checker=FormatChecker())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            timetable = Timetable.insert(request.json)
        except IntegrityError:
            raise Conflict(
                description="Error in TimeTableCollection post."
            )
        return Response(
            status=201, headers={"Location":url_for("api.timetableitem", timetable=timetable, job=job)}
        )"""

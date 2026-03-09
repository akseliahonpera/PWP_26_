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
        '''
        return Job.serialize(job)

    def put(self, job):
        '''
        Update a job
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
        '''
        return Job.query_all()

    def post(self):
        '''
        Add a new job
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

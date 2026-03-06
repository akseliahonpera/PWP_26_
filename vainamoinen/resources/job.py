from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen import Database, cache


class JobItem(Resource):

    '''
    Get a job (mene töihin)
    '''
    @cache.cached()
    def get(self, job):
        return Database.User.serialize(job)

    '''
    Update a job
    '''
    def put(self, job):
        pass

    '''
    
    ''' #unnecesessary?
    def post(self, job):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Database.Job.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        try:
            Database.insertJob(job)
        except IntegrityError:
            raise Conflict(
                description="something shitty happened in jobitem post"
            )
        return Response(status=204)

    '''
    Delete a job
    '''
    def delete(self, job):
        if Database.delete_job(job):
            return Response(status=204)
        return Response(status=400)


class JobCollection(Resource):

    '''
    Get all jobs
    '''
    def get(self, job):
        jobs = Database.query_job_all()
        return jobs

    '''
    Add a new job
    '''
    def post(self, job):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Database.Job.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        job = Database.Job()
        job.deserialize(request.json)
        try:
            Database.insertJob(job)

        except IntegrityError:
            raise Conflict(
                description="joku vittuilee jobcollection postissa"
            )
        return Response(status=201, headers={"Location":url_for("api.jobitem", job=job)})

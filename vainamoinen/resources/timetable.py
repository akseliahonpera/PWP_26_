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

    def get(self, job, timetable):
        '''
        TODO: doc-string
        '''
        return timetable.serialize()

    def put(self, job, timetable):
        '''
        TODO: doc-string
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
        TODO: doc-string
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
    TODO: doc-string
    '''

    def get(self, job):
        '''
        Get all timetables of a job
        '''
        return Timetable.query_all(_filter_={"job_name": job.job_name})

    def post(self, job):
        '''
        TODO: doc-string
        '''
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
        )

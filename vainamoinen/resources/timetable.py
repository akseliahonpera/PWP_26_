from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, UnsupportedMediaType

from vainamoinen import Database, cache

class TimeTableCollection(Resource):
    
    def get(self, timetable):
        pass

    def put(self, timetable):
        pass

    def post(self, timetable):
        pass

    def delete(self, timetable):
        pass

class TimeTableItem(Resource):
    
    def get(self, timetable):
        return Database.Timetable.serialize(timetable)

    def put(self, timetable):
        pass

    def post(self, timetable):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Database.Timetable.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        try:
            Database.insertJob(timetable)
        except IntegrityError:
            raise Conflict(
                description="something shitty happened in timetable post"
            )
        return Response(status=204)

    def delete(self, timetable):
        pass


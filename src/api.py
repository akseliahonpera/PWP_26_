from datetime import datetime
from typing import Any
from flask import Flask, Response, request
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from jsonschema import validate, ValidationError, FormatChecker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from werkzeug.exceptions import BadRequest, Conflict, NotFound, UnsupportedMediaType
from werkzeug.routing import BaseConverter
from db_package import Database
from instance_reference import api


##?? maybe execudet after database initiation??
print("api initialization")

"""
@event.listens_for(Engine, "connect")
def set_mysql_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

##user resources

class UserItem(Resource):
    
    def get(self, user):
        return Database.User.serialize(user)

    def put(self, user):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            Database.update_user(user, request.json)
        except IntegrityError:
            raise Conflict(
                description="Something shitty happened"
            )
        return Response(status=204)

    def post(self, user):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            Database.insertUser(request.json)
        except IntegrityError:
            raise Conflict(
                description="User with name '{username}' already in service".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, user):
        if Database.delete_user(user):
            return Response(status=204)
        return Response(status=400)

class UserCollection(Resource):
    print("in usercollection")
    def get(self):
        print("\nin usercollection get")
        users = Database.query_user_all()
        if users is None:
            return "no users"
        ret_viest = ""
        for user in users:
            ret_viest=ret_viest+str(user)
            return ret_viest
        return users

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try: 
            validate(request.json, Database.User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        try:
            user = Database.insertUser(request.json)
        except IntegrityError:
            raise Conflict(
                description="User with name '{username}' already in service".format(
                    **request.json
                )
            )
        return Response(status=201, headers={"Location":api.url_for(UserItem, user=user)})



##Job resources

#implement these
class JobCollection(Resource):

    def get(self, jobs):
        jobs = Database.query_job_all()
        return jobs


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
        return Response(status=201, headers={"Location":api.url_for(JobItem, job=job)})
        



#implement these
class JobItem(Resource):

    def get(self, job):
        return Database.Job.serialize(job)

    def put(self, job):
        pass

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

    def delete(self, job):
        if Database.delete_job(job):
            return Response(status=204)
        return Response(status=400)

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
            Database.insertTimetable(timetable) # type: ignore
        except IntegrityError:
            raise Conflict(
                description="something shitty happened in timetable post"
            )
        return Response(status=204)

    def delete(self, timetable):
        pass



##Converters
class JobConverter(BaseConverter):

    def to_python(self, job_name): # type: ignore #id?
        job = Database.query_job({"job_name":job_name})
        if job is None:
            raise NotFound
        return job
    
    def to_url(self, job): # type: ignore
        return Database.Job.serialize(job)["job_name"]


class UserConverter(BaseConverter):

    def to_python(self, user_name): # type: ignore #id?
        print(user_name)
        user=Database.query_user({"username":user_name})
        if user is None:
            raise NotFound
        return user

    def to_url(self, user): # type: ignore
        print(str(user))
        return Database.User.serialize(user)["username"]

"""##implement this
class TimeTableConverter(BaseConverter):
    def to_python(self, timetable_name): # type: ignore
        pass
    
    def to_url(self, timetable): # type: ignore
        return Database.Timetable.serialize(timetable)["title"]
"""


def initialize_converters(app):
    app.url_map.converters["job"] = JobConverter
    app.url_map.converters["user"] = UserConverter
    #app.url_map.converters["timetable"] = TimeTableConverter
    #tänne seuraavat

api.add_resource(JobCollection, "/api/jobs")
api.add_resource(JobItem, "/api/jobs/<job:job>")
api.add_resource(UserCollection, "/api/users")
api.add_resource(UserItem, "/api/users/<user:user>")


"""
api.add_resource(TimeTableItem, "/api/jobs/<job:job>/timetable/<timetable:timetable>")
"""
print("api initialization end")
from datetime import datetime
from flask import Flask, Response, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from jsonschema import validate, ValidationError, draft7_format_checker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from werkzeug.exceptions import BadRequest, Conflict, NotFound, UnsupportedMediaType
from werkzeug.routing import BaseConverter
from db_package import Database

from app import app

##?? maybe execudet after database initiation??
api = Api(app)

@event.listens_for(Engine, "connect")
def set_mysql_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


##user resources

class UserItem(Resource):
    
    def get(self, user):
        pass

    def put(self, user):
        pass

    def post(self, user):
        pass

    def delete(self, user):
        pass

class UserCollection(Resource):
    def get(self, user):
        pass

    def put(self, user):
        pass

    def post(self, user):
        pass

    def delete(self, user):
        pass


##Job resources

#implement these
class JobCollection(Resource):

    def get(self, job):
        pass

    def put(self, job):
        pass

    def post(self, job):
        pass

    def delete(self, job):
        pass

#implement these
class JobItem(Resource):

    def get(self, job):
        pass

    def put(self, job):
        pass

    def post(self, job):
        pass

    def delete(self, job):
        pass

##Converters
class JobConverter(BaseConverter):

    def to_python(self, job_name): # type: ignore #id?
        pass

    def to_url(self, db_sensor): # type: ignore
        pass


class UserConverter(BaseConverter):

    def to_python(self, user_name): # type: ignore #id?
        pass

    def to_url(self, user): # type: ignore
        pass

app.url_map.converters["job"] = JobConverter
app.url_map.converters["user"] = UserConverter
#tänne seuraavat
api.add_resource(JobCollection, "api/Jobs")
api.add_resource(JobItem, "api/jobs/<JobItem>")
api.add_resource(UserCollection, "api/users")
api.add_resource(UserItem, "api/users/<UserItem>")


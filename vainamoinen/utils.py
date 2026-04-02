'''
Converters and stuff
'''

from functools import wraps
import secrets

from werkzeug.exceptions import NotFound, Forbidden
from werkzeug.routing import BaseConverter

from flask import request

from .database import ApiKey, Job, User, Timetable

class JobConverter(BaseConverter):
    '''
    TODO: doc-string
    '''

    def to_python(self, value):
        '''
        TODO: doc-string
        '''
        db_sensor = Job.query.filter_by(job_name=value).first()
        if db_sensor is None:
            raise NotFound
        return db_sensor

    def to_url(self, value):
        '''
        TODO: doc-string
        '''
        return value.job_name


class UserConverter(BaseConverter):
    '''
    TODO: doc-string
    '''

    def to_python(self, value):
        '''
        TODO: doc-string
        '''
        db_user = User.query.filter_by(username=value).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        '''
        TODO: doc-string
        '''
        return value.username

##TODO: implement this
class TimeTableConverter(BaseConverter):
    '''
    TODO: doc-string
    '''

    def to_python(self, value):
        '''
        TODO: doc-string
        '''
        db_timetable = Timetable.query.filter_by(title=value).first()
        if db_timetable is None:
            raise NotFound
        return db_timetable

    def to_url(self, value):
        '''
        TODO: doc-string
        '''
        return value.title

def require_admin(func):
    '''
    Including this wrapper will create a requirement for the HTTP method to have an admin API key
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        key_hash = ApiKey.key_hash(request.headers.get("Vainamoinen-Api-Key", "").strip())
        db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, db_key.key): # type: ignore
            return func(*args, **kwargs)
        raise Forbidden
    return wrapper

def require_user(func):
    '''
    Including this wrapper will create a requirement for the HTTP method to have a user API key corresponding to the user in question
    In case the API key has admin permissions, the method will be accepted
    '''
    
    @wraps(func)
    def wrapper(self, user, *args, **kwargs):
        key_hash = ApiKey.key_hash(request.headers.get("Vainamoinen-Api-Key", "").strip())
        db_key = ApiKey.query.filter_by(user=user).first()
        admin_key = ApiKey.query.filter_by(admin=True).first()
        if db_key is not None and secrets.compare_digest(key_hash, db_key.key):
            return func(self, user, *args, **kwargs)
        if secrets.compare_digest(key_hash, admin_key.key): # type: ignore
            return func(self, user, *args, **kwargs)
        raise Forbidden
    return wrapper
        
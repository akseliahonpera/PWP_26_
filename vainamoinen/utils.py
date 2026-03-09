'''
Converters and stuff
'''

from werkzeug.exceptions import NotFound#, Forbidden
from werkzeug.routing import BaseConverter

from .database import Job, User#, Timetable

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

    def to_url(self, value):
        '''
        TODO: doc-string
        '''

from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter

from vainamoinen import Database

class JobConverter(BaseConverter):

    def to_python(self, job_name): # type: ignore #id?
        job = Database.query_job({"job_name":job_name})
        if job is None:
            raise NotFound
        return job
    
    def to_url(self, job): # type: ignore
        return Database.Job.serialize(job)["job_name"]


class UserConverter(BaseConverter):

    def to_python(self, user_name):
        db_user = Database.User.query.filter_by(username=user_name).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, user): # type: ignore
        return Database.User.serialize(user)["username"]

##implement this
class TimeTableConverter(BaseConverter):
    def to_python(self, timetable_name): # type: ignore
        pass
    
    def to_url(self, timetable): # type: ignore
        return Database.Timetable.serialize(timetable)["title"]

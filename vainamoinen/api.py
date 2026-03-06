from flask import Blueprint
from flask_restful import Api

from .resources.user import UserCollection, UserItem
from .resources.job import JobCollection, JobItem
#from .resources.timetable import TimeTableCollection, TimeTableItem

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)    

api.add_resource(JobCollection,     "/jobs")
api.add_resource(JobItem,           "/jobs/<job:job>")
api.add_resource(UserCollection,    "/users")
api.add_resource(UserItem,          "/users/<user:user>")

#api.add_resource(TimeTableItem, "api/jobs/<JobItem>/TimeTable/<TimeTableItem>")
#api.add_resource(TimeTableCollection, "api/jobs/<JobItem>/TimeTable")

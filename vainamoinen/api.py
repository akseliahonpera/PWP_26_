'''
Api blueprint and routing
'''

from flask import Blueprint
from flask_restful import Api

from .resources.user import UserCollection, UserItem, PublicUserCollection, PublicUserItem
from .resources.job import JobCollection, JobItem, UserItemsJobCollection
from .resources.timetable import TimeTableCollection, TimeTableItem

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(JobCollection,         "/jobs")
api.add_resource(JobItem,               "/jobs/<job:job>")

api.add_resource(UserCollection,        "/users")
api.add_resource(UserItem,              "/users/<user:user>")
api.add_resource(PublicUserCollection,  "/public/users")
api.add_resource(PublicUserItem,        "/public/users/<user:user>")

api.add_resource(UserItemsJobCollection,"/users/<user:user>/jobs")
api.add_resource(TimeTableCollection,   "/jobs/<job:job>/timetables")
api.add_resource(TimeTableItem,         "/jobs/<job:job>/timetables/<timetable:timetable>")

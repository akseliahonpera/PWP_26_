'''
Database models and functions
'''

import datetime
import random
from sqlalchemy.engine import Engine
from sqlalchemy import event

from . import db

@event.listens_for(Engine, "connect")
def set_mysql_pragma(dbapi_connection, _):
    '''Enable foreign keys'''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


###############################################################
######### Database global for module use ######################
###############################################################


class User(db.Model):
    '''
    User database model
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique= True, nullable=False) ##set unique to false to test
    password= db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(63), unique= False, nullable=False) ##set unique to false to test
    address = db.Column(db.String(63), nullable=False)
    phone_number = db.Column(db.String(31), nullable=False)
    description = db.Column(db.Text(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    job = db.relationship("Job",cascade="all,delete-orphan", back_populates = "user")###relation

    def serialize(self, include_jobs=False):
        '''
        TODO: doc-string
        '''
        user = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "description": self.description,
            "created": self.created.isoformat()
        }
        if include_jobs:
            user["jobs"] = []
            for single_job in self.job: # type: ignore
                user["jobs"].append(single_job.serialize())
        return user

    def deserialize(self, user):
        '''
        TODO: doc-string
        '''
        self.username = user["username"]
        self.password = user["password"]
        self.email = user["email"]
        self.address = user["address"]
        self.phone_number = user["phone_number"]
        self.description = user["description"]

    @staticmethod
    def json_schema():
        '''
        TODO: doc-string
        '''
        schema = {
            "type": "object",
            "required": ["username", "password","email","address","phone_number","description"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "Users unique username",
            "type": "string"
        }
        props["password"] = {
            "description": "users password, to be hashed by hashing and salting algo",
            "type": "string"
        }
        props["email"] = {
            "description": "users unique email",
            "type": "string"
        }
        props["address"] = {
            "description": "users address",
            "type": "string"
        }
        props["phone_number"] = {
            "description": "users phonenumber",
            "type": "string"
        }
        props["description"] = {
            "description": "users description, bio",
            "type": "string"
        }
        return schema

    @classmethod
    def query_all(cls):
        '''
        Get all users from database
        '''
        user_list = []
        users = cls.query.all()
        for user in users:
            user_list.append(user.serialize())
        return user_list

    @classmethod
    def insert(cls, request_json):
        '''
        Insert a new user into database with request_json
        '''
        user = cls()
        user.deserialize(request_json)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, request_json):
        '''
        Update a user in database with request_json
        '''
        self.deserialize(request_json)
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        '''
        Delete a user from database
        '''
        db.session.delete(self)
        db.session.commit()





class Job(db.Model):
    '''
    Job database model
    '''

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(32),db.ForeignKey(User.username,ondelete="CASCADE"),nullable=False)
    job_name = db.Column(db.String(63),unique=True, nullable=False)#lisätty kenttä resursseja varte
    job_description = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(63),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    opening_hours = db.Column(db.String(63),nullable=False)
    category = db.Column(db.String(31),nullable=False)
    user = db.relationship("User",  back_populates = "job")###relation
    timetable = db.relationship("Timetable",cascade="all,delete-orphan", back_populates= "job")

    def serialize(self):
        '''
        TODO: doc-string
        '''
        return {
            "id": self.id,
            "username": self.username,
            "job_name": self.job_name,
            "job_description": self.job_description,
            "location": self.location,
            "created": self.created.isoformat(),
            "opening_hours": self.opening_hours,
            "category": self.category,
            "user": self.user.serialize()
        }

    def deserialize(self, job):
        '''
        TODO: doc-string
        '''
        self.username=job["username"]
        self.job_name=job["job_name"]
        self.job_description=job["job_description"]
        self.location=job["location"]
        self.opening_hours=job["opening_hours"]
        self.category=job["category"]

    @staticmethod
    def json_schema():
        '''
        TODO: doc-string
        '''
        schema = {
            "type": "object",
            "required":[
                "username","job_name","job_description",
                "location","opening_hours","category"
            ]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "User's name",
            "type": "string"
        }
        props["job_name"] = {
            "description": "Jobs unique name",
            "type": "string"
        }
        props["job_description"] = {
            "description": "jobs description",
            "type": "string"
        }
        props["location"] = {
            "description": "jobs location",
            "type": "string"
        }
        props["opening_hours"] = {
            "description": "opening_hours",
            "type": "string"
        }
        props["category"] = {
            "description": "category",
            "type": "string"
        }
        return schema

    @classmethod
    def query_all(cls, filter_name=None):
        '''
        Get all jobs from database,
        if filter_name is set to a username, gets all user's jobs.

        Parameters:
            filter_name - username to filter with
        '''
        job_list = []
        query = cls.query

        if filter_name:
            query = query.filter_by(username=filter_name)

        jobs = query.all()
        for job in jobs:
            job_list.append(job.serialize())
        return job_list

    @classmethod
    def insert(cls, request_json):
        '''
        Insert a new job into database with request_json
        '''
        job = cls()
        job.deserialize(request_json)
        db.session.add(job)
        db.session.commit()
        return job

    def update(self, request_json):
        '''
        Update a job in database with request_json
        '''
        self.deserialize(request_json)
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        '''
        Delete a job from database
        '''
        db.session.delete(self)
        db.session.commit()


class Timetable(db.Model):
    '''
    Timetable database model
    '''
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey(Job.id,ondelete="CASCADE"),nullable=False)
    title= db.Column(db.String(63), nullable=False)####lisätty kenttä resursseja varten
    start_time = db.Column(db.DateTime, nullable=True)##unix tms
    end_time = db.Column(db.DateTime, nullable=True)##unix tms
    is_booked = db.Column(db.Boolean,nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    job = db.relationship("Job",  back_populates = "timetable")###relation


    def serialize(self):
        '''
        TODO: doc-string
        '''
        timetable = {"id":self.id}
        timetable["title"]=self.title
        timetable["start_time"]=self.start_time.isoformat()
        timetable["end_time"]=self.end_time.isoformat()
        timetable["is_booked"]=self.is_booked
        timetable["created"]=self.created.isoformat()
        return timetable

    def deserialize(self, timetable):
        '''
        TODO: doc-string
        '''
        self.title  = timetable["title"]
        self.start_time = timetable["start_time"]
        self.end_time = timetable["end_time"]
        self.is_booked = timetable["is_booked"]
        self.created = timetable["created"]

    @staticmethod
    def json_schema():
        '''
        TODO: doc-string
        '''
        schema = {
            "type": "object",
            "required": ["title", "start_time","end_time","is_booked"]
        }
        props = schema["properties"] = {}
        props["title"] = {
            "description": "tt entry title",
            "type": "string"
        }
        props["start_time"] = {
            "description": "start time",
            "type": "ISO_datetime"
        }
        props["end_time"] = {
            "description": "end time ",
            "type": "ISO_datetime"
        }
        props["is_booked"] = {
            "description": "resrevation status",
            "type": "boolean"
        }
        return schema














###############################################################
######### Database functions ##################################
###############################################################

def init_db():
    ''' Initialize database '''
    db.create_all()




###############################################################
######### Testing stuff      ##################################
###############################################################

###chatGPT
user_test_packet = {
    "username": "un",
    "password": "securepassword123",  # hash this later if you haven't yet
    "email": "testuser@example.com",
    "address": "123 Main Street, Springfield",
    "phone_number": "555-123-4567",
    "description": "Test user account for database insertion"
}

job_test_packet = {
    "userID": 1,  # make sure this user ID exists in your User table
    "job_description": "Looking for a part-time barista for weekend shifts",
    "job_name": "Barista at coffee shop",
    "timetable": {
        "title": "Weekend Morning Shift",
        "start_time": "2026-02-14T08:00:00",
        "end_time": "2026-02-14T14:00:00",
        "is_booked": False
    },
    "location": "Downtown Cafe, Springfield",
    "opening_hours": "08:00-14:00",
    "category": "Hospitality"
}
###chatGPT ends


def populate_database():
    """Function for populating the database users and jobs, change values on the size you want"""
    users = User.query_all()
    if users is None:
        userscount = 0
    else:
        userscount = len(users)
    samplesize = 50
    userdata= user_test_packet
    running_number_user = userdata["username"]
    jobdata= job_test_packet

    for _ in range(userscount,userscount+samplesize):
        userdata["username"] = running_number_user+f'{datetime.datetime.now()}'
        print(" USERNAMES::"+userdata["username"])
        User.insert(userdata)

    users = User.query_all()
    if users is None:
        print("No users available, aborting job creation")
    else:
        for _ in range(samplesize-25):
            random_user= random.randrange(1,len(users))
            print(random_user)
            jobdata["user_id"]= random_user
            jobdata["job_name"] = "j_name:"+f'{datetime.datetime.now()}'
            Job.insert(jobdata)

def main():
    """test for populating the database by running this module dircetly. """
    #init()

if __name__ == '__main__':
    main()

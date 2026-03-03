import datetime
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy_utils import database_exists
import random 
from app import app

###############################################################
######### Database global for module use ######################
###############################################################
app.config["SQLALCHEMY_DATABASE_URI"]= f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    
db = SQLAlchemy(app)



###############################################################
######### Models             ##################################
###############################################################


class User(db.Model):

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
        user = {"id": self.id, "username": self.username}
        user["email"]=self.email
        user["address"]=self.address
        user["phone_number"]=self.phone_number
        user["description"]= self.description
        user["created"] = self.created.isoformat()
        if include_jobs:
            user["jobs"] = []
            for single_job in self.job: # type: ignore
                user["jobs"].append(single_job.serialize())
        return user
    
    def deserialize(self, user):
        self.username = user["username"]
        self.password = user["password"]
        self.email = user["email"]
        self.address = user["address"]
        self.phone_number = user["phone_number"]
        self.description = user["description"]

    @staticmethod
    def json_schema():
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
            "type": "String"
        }
        return schema

class Job(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"),  nullable=False)
    job_name = db.Column(db.String(63),unique=True, nullable=False)####lisätty kenttä resursseja varten
    job_description = db.Column(db.String(255), nullable=False) 
    location = db.Column(db.String(63),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    opening_hours = db.Column(db.String(63),nullable=False)
    category = db.Column(db.String(31),nullable=False)
    user = db.relationship("User",  back_populates = "job")###relation
    timetable = db.relationship("Timetable",cascade="all,delete-orphan", back_populates= "job")
    
    def serialize(self):
        job = {"id":self.id}
        job["user_id"]=self.user_id
        job["job_name"]=self.job_name
        job["job_description"]=self.job_description
        job["location"]=self.location
        job["created"]=self.created.isoformat()
        job["opening_hours"]= self.opening_hours
        job["category"] = self.category
        job["user"] = self.user.serialize()
        return job
    
    def deserialize(self, job):
        self.user_id=job["user_id"]
        self.job_name=job["job_name"]
        self.job_description=job["job_description"]
        self.location=job["location"]
        self.opening_hours=job["opening_hours"]
        self.category=job["category"]
        #self.user=job["user"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["user_id", "job_description","location","opening_hours","category","user"]
        }
        props = schema["properties"] = {}
        props["user_id"] = {
            "description": "Jobs unique uuserID",
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
        props["user"] = {
            "description": "user reference object",
            "type": "object"
        }
        return schema
    


    
class Timetable(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey(Job.id, ondelete="CASCADE"),  nullable=False) # type: ignore
    title= db.Column(db.String(63), nullable=False)####lisätty kenttä resursseja varten
    start_time = db.Column(db.DateTime, nullable=True)##unix tms
    end_time = db.Column(db.DateTime, nullable=True)##unix tms
    is_booked = db.Column(db.Boolean,nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    job = db.relationship("Job",  back_populates = "timetable")###relation

    
    def serialize(self):
        timetable = {"id":self.id}
        timetable["title"]=self.title
        timetable["start_time"]=self.start_time.isoformat()
        timetable["end_time"]=self.end_time.isoformat()
        timetable["is_booked"]=self.is_booked
        timetable["created"]=self.created.isoformat()
        return timetable
    
    def deserialize(self, timetable):
        self.title  = timetable["title"]
        self.start_time = timetable["start_time"]
        self.end_time = timetable["end_time"]
        self.is_booked = timetable["is_booked"]
        self.created = timetable["created"]

    @staticmethod
    def json_schema():
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


def init():
    instantiateDatabase()


###############################################################
######### Database functions ##################################
###############################################################


def instantiateDatabase(): 
    """Creates all tables(defined models related to db) to the database, if this fails create the database itself first."""
    with app.app_context():
        if database_exists(f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset=utf8mb4'):
            ##This creates tables if they are not existing already. Works only if db already exists.
            db.create_all()
        else:
            print("database does not exist")

def createDataBase():
    """If database does not yet exist, create database to the database engine. """
    raise NotImplementedError

###############################################################
######### Insertions ##########################################
###############################################################

##USER RELATED
def insertUser(request_json):##MAybe implements checking if resource exists already??
    """"Gets user dict as parameter. Returns true or false depending on success."""
    try:
        with app.app_context():
            user = User()
            user.deserialize(request_json)
            db.session.add(user)
            db.session.commit()
            return user
    except Exception as e:
        print("failed to insert user", e)
        return None

##JOB RELATED
def insertJob(request_json):
    """"Gets job dict. Returns true or false depending on success."""
    try: 
        with app.app_context():
            job = Job()
            job.deserialize(request_json)
            db.session.add(job)
            db.session.commit()
            return job
    except Exception as e:
        print("insert job failure", e)
        return None

###############################################################
######### Queries #############################################
###############################################################

##USER RELATED
def query_user_all():
    """Returns all users as list[dictionary]
    """
    try:
        with app.app_context(): 
            user_rs= User.query.all()
            result_dict_list = []
            ##serialize to json list (dict)
            for i in user_rs:
                result_dict_list.append(User.serialize(i))
            #print(querything)
            return result_dict_list

    except Exception as e:
        print("query failed ", e)
        return None

    
#https://stackoverflow.com/questions/6718480/sqlalchemy-orm-declarative-how-to-build-query-from-key-values-in-a-dict?rq=3
def query_user(request_json):
    """Dynamic/Generic query method. 
    Takes json object/python dict as parameter, which contains the query data for the user.
        eg. {'id': 4,}
    Returns results as List[dictionary]
    """
    try:
        with app.app_context(): 
            user_rs= db.session.query(User).filter_by(**request_json).all()
            result_dict_list = []
             ##serialize to json list (dict)
            for i in user_rs:
                result_dict_list.append(User.serialize(i))
            #print(querything)
            return result_dict_list

    except Exception as e:
        print("qiuery failed ", e)
        return None

##JOB RELATED    
def query_job_all():
    """Query all jobs currently, Returns list[dict] of jobs"""
    try:
        with app.app_context():
            job_rs= Job.query.all()
            result_dict_list = []
             ##serialize to json list
            for i in job_rs:       
                result_dict_list.append(Job.serialize(i))
            #print(querything)
            return result_dict_list 
    except Exception as e:
        print("qieru failed ", e)
        return None
    
def query_job(request_json):
    """takes dictionary as parameter, builds query based on that"""
    print("Try job querying.")
    try:
        with app.app_context():
            
            job_rs = db.session.query(Job).filter_by(**request_json).all()
            result_dict_list = []
             ##serialize to json list
            for i in job_rs:       
                result_dict_list.append(Job.serialize(i))
            #print(querything)
            return result_dict_list

    except Exception as e:
        print("query failed ", e)
        return None

###############################################################
######### Delete functions   ##################################
###############################################################

##USER RELATED
def delete_user(user):
    """Delete user by object. Returns true if success, false otherwise"""
    try:
        with app.app_context():

            db.session.delete(user)
            db.session.commit()
            print("user deletion succesfull")
            return True
    except Exception as e:
        print("user deletion failed, try cascading delete?", e)
        return False


def delete_user_by_id(user_id):
    """Delete user by id. Returns true if success, false otherwise"""
    try:
        with app.app_context():
            print("q1")
            user = User.query.filter_by(id=user_id).first()
            print("q2 ")
            print(user)
            db.session.delete(user)
            db.session.commit()
            print("user deletion succesfull")
            return True
    except Exception as e:
        print("user deletion failed, try cascading delete?", e)
        return False


##JOB RELATED
def delete_job_by_request_json(request_json):
    """Delete job by request_json. Returns true if success, false otherwise"""
    try:
        with app.app_context():
            job = Job.query.filter_by(job_name=request_json["job_name"]).first()
            db.session.delete(job)
            db.session.commit()
            print("Job deletion succesfull")
            return True
    except Exception as e:
        print("job deletion failed ", e)
        return False

def delete_job(job):
    """Delete by job object. Returns true if success, false otherwise"""
    try:
        with app.app_context():
            db.session.delete(job)
            db.session.commit()
            print("Job deletion succesfull")
            return True
    except Exception as e:
        print("job deletion failed ", e)
        return False


def delete_job_by_id(job_id):
    """Delete by id. Returns true if success, false otherwise"""
    try:
        with app.app_context():
            job = Job.query.filter_by(id=job_id).first()
            db.session.delete(job)
            db.session.commit()
            print("Job deletion succesfull")
            return True
    except Exception as e:
        print("job deletion failed ", e)
        return False

###############################################################
######### Update functions   ##################################
###############################################################
 
##USER RELATED
def update_user(user, request_json):
    """ 
        Make sure only authorized users can access this per user!! 
        Gets update target user object and the update data as json dict, locates user and makes changes according to the new packet,shitty
    """
    try:
        with app.app_context():
            user = user.deserialize(request_json) 
            db.session.commit()
            return True
    except Exception as e:
        print("query failed ", e)
        return False

##JOB RELATED
def update_job(job, request_json):    
    """ Kinda unsafe.
        Make sure only authorized users can access this per job!! 
        Locate job by given id and change according to the job packet
    """
    try:
        with app.app_context():
            job = job.deserialize(request_json)
            db.session.commit()
            return True
    except Exception as e:
        print("qieru failed ", e)
        return False
   

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
    users = query_user_all()
    if users is None:
        userscount = 0
    else:
        userscount = len(users)
    samplesize = 50
    userdata= user_test_packet
    runningNumber_user = userdata["username"]
    jobdata= job_test_packet

    for i in range(userscount,userscount+samplesize):
        userdata["username"] = runningNumber_user+f'{datetime.datetime.now()}'
        print(" USERNAMES::"+userdata["username"])
        insertUser(userdata)

    users = query_user_all()
    if users is None:
            print("No users available, aborting job creation")
    else:
        for i in range(samplesize-25):
            randomUser= random.randrange(1,len(users))
            print(randomUser)
            jobdata["user_id"]= randomUser
            jobdata["job_name"] = "j_name:"+f'{datetime.datetime.now()}'
            insertJob(jobdata)
            
def main():
    """test for populating the database by running this module dircetly. """
    init()



if __name__ == '__main__':
    main()
else:
    init()
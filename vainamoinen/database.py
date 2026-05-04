'''
Database models and functions
'''

from datetime import datetime
import hashlib
import random
import secrets
import uuid
import click
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask.cli import with_appcontext

db = SQLAlchemy()

@event.listens_for(Engine, "connect")
def set_mysql_pragma(dbapi_connection, _):
    '''Enable foreign keys'''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


###############################################################
######### Database global for module use ######################
###############################################################


class GenericDatabaseModel(db.Model):
    '''
    Generic database model, you can make subclasses from this
    Subclasses inherit the database methods.
    '''
    __abstract__ = True

    @classmethod
    def query_all(cls, _filter_=None, public=False, include_jobs=False):
        '''
        Get all objects T from database,
        if _filter_ is set, gets all filtered objects.

        Parameters:
            _filter_ - for example a username, in format; {"username": "test-user-1"}
        Note: only set public to True if model has a public serializer
        '''
        obj_list = []
        query = cls.query

        if _filter_:
            print(_filter_)
            query = query.filter_by(**_filter_)

        objects = query.all()
        if public and include_jobs:
            for obj in objects:
                obj_list.append(obj.serialize_public(include_jobs))
            return obj_list
        
        if include_jobs:
            for obj in objects:
                obj_list.append(obj.serialize(include_jobs))
            return obj_list
        
        if public:
            for obj in objects:
                obj_list.append(obj.serialize_public())
            return obj_list
            
        for obj in objects:
            obj_list.append(obj.serialize())
        return obj_list
    

    @classmethod
    def insert(cls, request_json):
        '''
        Insert a new object T into database with request_json
        '''
        obj = cls()
        obj.deserialize(request_json) # type: ignore
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, request_json):
        '''
        Update an object T in database with request_json
        '''
        self.deserialize(request_json) # type: ignore
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        '''
        Delete an object T from database
        '''
        db.session.delete(self)
        db.session.commit()


class User(GenericDatabaseModel):
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
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    job = db.relationship("Job",cascade="all,delete-orphan", back_populates = "user")###relation
    api_key = db.relationship("ApiKey", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def serialize(self, include_jobs=False):
        '''
        Serializes all data, including sensitive information.
        ONLY TO BE USED WITH USER OR ADMIN AUTHENTICATION
        '''
        user = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
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
    
    def serialize_public(self, include_jobs=False):
        '''
        Omit sensitive user information, intended to be safe and accessible without any authorization
        # TODO: Do we include address and phone number here? omitting them for time being but might be changed in the future
        '''
        user = {
            "username": self.username,
            "email": self.email,
            "description": self.description,
            "created":self.created.isoformat()
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
        schema = {"type": "object",
            "required": ["username", "password","email","address","phone_number","description"]
        }
        props = schema["properties"] = {}
        props["username"] = {"description": "Users unique username", "type": "string"}
        props["password"] = {"description": "users pswd, to be hashed and salted","type": "string"}
        props["email"] =    {"description": "users unique email", "type": "string"}
        props["address"] =  {"description": "users address", "type": "string"}
        props["phone_number"] = {"description": "users phonenumber", "type": "string"}
        props["description"] =  {"description": "users description, bio", "type": "string"}
        return schema



class Job(GenericDatabaseModel):
    '''
    Job database model
    '''

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(32),db.ForeignKey(User.username,ondelete="CASCADE"),nullable=False)
    job_name = db.Column(db.String(63),unique=True, nullable=False)#lisätty kenttä resursseja varte
    job_description = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(63),nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    opening_hours = db.Column(db.String(63),nullable=False)
    category = db.Column(db.String(31),nullable=False)
    user = db.relationship("User",  back_populates = "job")###relation
    timetable = db.relationship("Timetable",cascade="all,delete-orphan", back_populates= "job")

    def serialize(self):
        '''
         serializes job object
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
            "user": self.user.serialize_public()
        }

    def deserialize(self, job):
        '''
        de-serializes job object
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
        schema = {"type": "object",
            "required":[
                "username","job_name","job_description",
                "location","opening_hours","category"
            ]
        }
        props = schema["properties"] = {}
        props["username"] =         {"description": "User's name", "type": "string"}
        props["job_name"] =         {"description": "Jobs unique name", "type": "string"}
        props["job_description"] =  {"description": "jobs description", "type": "string"}
        props["location"] =         {"description": "jobs location", "type": "string"}
        props["opening_hours"] =    {"description": "opening_hours", "type": "string"}
        props["category"] =         {"description": "category", "type": "string"}
        return schema



class Timetable(GenericDatabaseModel):
    '''
    Timetable database model
    '''
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(63), db.ForeignKey(Job.job_name,ondelete="CASCADE"),nullable=False)
    title= db.Column(db.String(63),unique=True, nullable=False)####lisätty kenttä resursseja varten
    start_time = db.Column(db.DateTime, nullable=True)##unix tms
    end_time = db.Column(db.DateTime, nullable=True)##unix tms
    is_booked = db.Column(db.Boolean,nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    job = db.relationship("Job",  back_populates = "timetable")###relation

    def serialize(self):
        '''
        serializes timetable object
        '''
        return {
            "id": self.id,
            "job_name": self.job_name,
            "title": self.title,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "is_booked": self.is_booked,
            "created": self.created.isoformat()
        }

    def deserialize(self, timetable):
        '''
        Start and end times are optional, both are not necessary (starting from time ->>)
        '''
        self.job_name = timetable["job_name"]
        self.title  = timetable["title"]
        self.is_booked = timetable["is_booked"]

        self.start_time = datetime.fromisoformat(timetable["start_time"]) if timetable.get("start_time") else None
        self.end_time = datetime.fromisoformat(timetable["end_time"]) if timetable.get("end_time") else None


    @staticmethod
    def json_schema():
        '''
        TODO: doc-string
        '''
        schema = {"type": "object",
            "required": ["title","is_booked"]
        }
        props = schema["properties"] = {}
        props["title"] =        {"description": "tt entry title","type": "string"}
        props["start_time"] =   {"description": "start time", "type": "string", "format": "date-time"}
        props["end_time"] =     {"description": "end time ", "type": "string", "format": "date-time"}
        props["is_booked"] =    {"description": "resrevation status","type": "boolean"}
        return schema

class ApiKey(db.Model):
    """
    Class for apikey handling. 
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    admin = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="api_key", uselist=False)

    @staticmethod
    def key_hash(key):
        '''
        Generates a hash for an API key
        '''
        return hashlib.sha256(key.encode()).digest()
    
    def __init__(self, key, admin=False, user_id=None, **kwargs):
        """
        Constructor so that pylance recognizes these parameters statically
        """
        super(ApiKey, self).__init__(**kwargs)
        self.key = key
        self.admin = admin
        self.user_id = user_id


###############################################################
######### Database functions ##################################
###############################################################

def init_db():
    ''' Initialize database '''
    db.create_all()

    # Database population based on if any users exist
    is_empty = db.session.query(User.id).first() is None
    if is_empty:
        populate_database()


@click.command("init-db")
@with_appcontext
def init_db_command():
    '''Cli callable function to initialize the database'''
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

    for i in range(samplesize):
        new_user_data = user_test_packet.copy()
        
        unique_suffix = str(uuid.uuid4())[:8]
        new_user_data["username"] = f"user_{unique_suffix}_{i}"
        new_user_data["email"] = f"email_{unique_suffix}@example.com"
        print(" USERNAMES::"+new_user_data["username"])
        User.insert(new_user_data)

    updated_users = User.query_all()
    if updated_users is None:
        print("No users available, aborting job creation. User creation likely failed")

    for i in range(samplesize - 25):
        new_job_data = job_test_packet.copy()
        
        random_user = random.choice(updated_users)
        
        new_job_data["username"] = random_user["username"]
        
        unique_id = str(uuid.uuid4())[:8]
        new_job_data["job_name"] = f"Job_{unique_id}_{i}"
        
        Job.insert(new_job_data)

        ###########################################
        ### FOR DEVELOPMENT AND TESTING ONLY    ###
        ### REMOVE AND IMPLEMENT ADMIN API KEY  ###
        ### ELSEWHERE FOR DEPLOYABLE VERSION    ###
        ###########################################
        # Add an admin API key if one does not exist, then display it in console

        api_key_exists = db.session.query(ApiKey.id).first() is not None
        if not api_key_exists:
            token = secrets.token_urlsafe()
            db_key = ApiKey(
                key = ApiKey.key_hash(token),
                admin = True
            )
            db.session.add(db_key)
            db.session.commit()
            print("DEVELOPMENT USE ONLY ADMIN API KEY: " + token)

def main():
    """test for populating the database by running this module dircetly. """
    #init()

if __name__ == '__main__':
    main()

import datetime
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy_utils import database_exists
import random 

from app import app

app.config["SQLALCHEMY_DATABASE_URI"]= f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique= False, nullable=False) ##set unique to false to test
    password= db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(63), unique= False, nullable=False) ##set unique to false to test
    address = db.Column(db.String(63), nullable=False)
    phoneNumber = db.Column(db.String(31), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    jobs = db.relationship("Job",cascade="all,delete-orphan", back_populates = "user")###relation

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"),  nullable=False)
    jobDescription = db.Column(db.String(255), nullable=False)
    timetable = db.Column(db.String(63), nullable=True)
    location = db.Column(db.String(63),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    opening_hours = db.Column(db.String(63),nullable=False)
    category = db.Column(db.String(31),nullable=False)
    user = db.relationship("User",  back_populates = "jobs")###relation

def init():
    createDatabase()


def createDatabase(): #tables actually, 
    with app.app_context():
        if database_exists(f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset=utf8mb4'):
            db.create_all()
        else:
            print("database does not exist")
    

def insertUser(user_packet):
    """"Gets dictionary of user values"""
    try:
        with app.app_context():
            user_record = User(
                username= user_packet["username"],  # type: ignore
                password= user_packet["password"], # type: ignore
                email= user_packet["email"], # type: ignore
                address= user_packet["address"], # type: ignore
                phoneNumber= user_packet["phoneNumber"], # type: ignore
                description= user_packet["description"] # type: ignore
                )
            db.session.add(user_record)
            db.session.commit()
            return True
    except Exception as e:
        print("failed to insert user", e)
        return False


def insertJob(job_packet):
    """"Gets dictionary of job values"""
    try: 
        with app.app_context():
            job_record = Job(
            userID = job_packet["userID"], # type: ignore
            jobDescription = job_packet["jobDescription"], # type: ignore
            timetable = job_packet["timetable"], # type: ignore
            location = job_packet["location"], # type: ignore
            created = job_packet["created"], # type: ignore
            opening_hours = job_packet["opening_hours"], # type: ignore
            category = job_packet["category"] # type: ignore
            ) 
            db.session.add(job_record)
            db.session.commit()
            return True
    except Exception as e:
        print("insert job failure", e)
        return False



def query_user(getRequest):
    """WIP get all users currently only"""
    try:
        with app.app_context(): 
            return User.query.all()
    except Exception as e:
        print("qieru failed ", e)
        return -1
    
def query_job(job_query):
    """Query all jobs currently"""
    try:
        with app.app_context():

            return Job.query.all()
    except Exception as e:
        print("qieru failed ", e)
        return -1

def delete_job(job_id):
    """Delete by id"""
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

def delete_user(user_id):
    """Delete user by id"""
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

def update_job(job_id, job_packet):    
    """ Kinda unsafe.
        Make sure only authorized users can access this per job!! 
        Locate job by given id and change according to the job packet
    """
    try:
        with app.app_context():
            temp_job = Job.query.filter_by(id=job_id)
            temp_job.userID = job_packet["userID"], # type: ignore
            temp_job.jobDescription = job_packet["jobDescription"], # type: ignore
            temp_job.timetable = job_packet["timetable"], # type: ignore
            temp_job.location = job_packet["location"], # type: ignore
            temp_job.opening_hours = job_packet["opening_hours"], # type: ignore
            temp_job.category = job_packet["category"] # type: ignore
            
            db.session.add(temp_job)
            db.session.commit()
            return True
    except Exception as e:
        print("qieru failed ", e)
        return False

def update_user(user_packet):
    """ Kinda unsafe.
        Make sure only authorized users can access this per user!! 
        Gets user data as json dict, locates user and makes changes according to the new packet,shitty
    """
    try:
        with app.app_context():
            temp_user = User.query.filter_by(username=user_packet["username"], password=user_packet["password"])
            temp_user.username= user_packet["username"],  # type: ignore
            temp_user.password= user_packet["password"], # type: ignore
            temp_user.email= user_packet["email"], # type: ignore
            temp_user.address= user_packet["address"], # type: ignore
            temp_user.phoneNumber= user_packet["phoneNumber"], # type: ignore
            temp_user.description= user_packet["description"] # type: ignore
            db.session.commit()
            return True
    except Exception as e:
        print("query failed ", e)
        return False




###chatGPT
user_test_packet = {
    "username": "testuser",
    "password": "securepassword123",  # hash this later if you haven't yet
    "email": "testuser@example.com",
    "address": "123 Main Street, Springfield",
    "phoneNumber": "555-123-4567",
    "description": "Test user account for database insertion"
}

job_test_packet = {
    "userID": 1,  # make sure this user ID exists in your User table
    "jobDescription": "Looking for a part-time barista for weekend shifts",
    "timetable": "Weekends 8am–2pm",
    "location": "Downtown Cafe, Springfield",
    "created": "2026-02-09",  # or datetime.utcnow() if your model expects a datetime
    "opening_hours": "08:00-14:00",
    "category": "Hospitality"
}
###chatGPT ends

def populate_database():
    """Function for populating the database users and jobs, change values on the size you want"""
    samplesize = 50
    userdata= user_test_packet
    runningNumber_user = userdata["username"]
    jobdata= job_test_packet
    for i in range(samplesize):
        userdata["username"] = runningNumber_user+f'": "+{i}'
        print(" UUUUSERNAMEEEESSS::        "+userdata["username"])
        insertUser(userdata)

    for i in range(samplesize-25):
        randomUser= random.randrange(1,samplesize-25)
        print(randomUser)
        jobdata["userID"]= randomUser
        insertJob(jobdata)

def main():
    """test for populating the database by running this module dircetly. """
    init()



if __name__ == '__main__':
    main()
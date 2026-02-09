import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy_utils import database_exists

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://root:Gambiinakiuas522@localhost:3306/pwp26?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique= False, nullable=False) ##set unique to false to test
    password= db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(63), unique= False, nullable=False) ##set unique to false to test
    address = db.Column(db.String(63), nullable=False)
    phoneNumber = db.Column(db.String(31), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    jobs = db.relationship("Job", back_populates = "user")###relation

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey(User.id),  nullable=False)
    jobDescription = db.Column(db.String(255), nullable=False)
    timetable = db.Column(db.String(63), nullable=True)
    location = db.Column(db.String(63),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    opening_hours = db.Column(db.String(63),nullable=False)
    category = db.Column(db.String(31),nullable=False)
    user = db.relationship("User", back_populates = "jobs")###relation

def init():
    createDatabase()


def createDatabase(): #tables actually, 
    with app.app_context():
        if database_exists("mysql+pymysql://root:Gambiinakiuas522@localhost:3306/pwp26?charset=utf8mb4"):
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


###chatGPT
user_test_packet = {
    "username": "testuser123",
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


def query_user(query_packet):
    try:
        with app.app_context():

            return True
    except Exception as e:
        print("qieru failed ", e)
        return False
    
def query_job():
    try:
        with app.app_context():

            return True
    except Exception as e:
        print("qieru failed ", e)
        return False

def delete_job(job_id):
    try:
        with app.app_context():
            job = Job.query.filter_by(id=job_id)
            db.session.delete(job)
            db.session.commit()
            return True
    except Exception as e:
        print("qieru failed ", e)
        return False

def delete_user(user_id):
    try:
        with app.app_context():
            user = User.query.filter_by(id=user_id)
            db.session.delete(user)
            db.session.commit()
            return True
    except Exception as e:
        print("deletion failed ", e)
        return False

def update_job(job_id):
    try:
        with app.app_context():

            return True
    except Exception as e:
        print("qieru failed ", e)
        return False

def update_user(user_id):
    try:
        with app.app_context():

            return True
    except Exception as e:
        print("qieru failed ", e)
        return False






def main():
    init()

    userdata= user_test_packet
    insertUser(userdata)

    jobdata= job_test_packet
    insertJob(jobdata)



if __name__ == '__main__':
    main()
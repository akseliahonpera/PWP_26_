from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= config.MYSQL_HOST
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password= db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phoneNumber = db.Column(db.String, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), nullable=False)
    jobDescription = db.Column(db.String(255), nullable=False)
    timetable = db.Column(db.String, nullable=True)
    location = db.Column(db.String,nullable=False)
    created = db.Column(db.DateTime,nullable=False)
    opening_hours = db.Column(db.String,nullable=False)
    category = db.Column(db.String,nullable=False)


def createUserTable():
    pass
def createJobsTable():
    pass

def createDatabase():
    pass
def databaseExists():
    pass

def insertUser():

    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ctx.pop()


def insertJob():
    pass



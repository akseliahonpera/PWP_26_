from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= config.MYSQL_HOST
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)





def createUserTable():

def createJobsTable():


def createDatabase():

def databaseExists():


def insertUser():

    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ctx.pop()


def insertJob():




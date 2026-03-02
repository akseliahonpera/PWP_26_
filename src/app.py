import datetime
from db_package import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)


def main():
    testfunction()
 
##For testing the database functions
def testfunction():
    job_test_packet2 = {'id': 4,}
    user_test_packet2 = {'id': 4,}
    Database.createDatabase()
    Database.populate_database()
    print("attempt deletion of job")
    Database.delete_job(3)
    print("attempt deletion of user")
    Database.delete_user(2)
    
    print("test query all ")
    jobs = Database.query_job_all()

    for job in jobs: # type: ignore
        print(job)
    
    print("test query by generic ")
    jobs = Database.query_job(job_test_packet2)

    for job in jobs: # type: ignore
        print(job)
    print("test query users by generic dict")
    users = Database.query_user(user_test_packet2)
    print("Print queryresults")
    for user in users: # type: ignore
        print(user)


if __name__ == "__main__":
    main()


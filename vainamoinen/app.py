import datetime
import os

from flask_caching import Cache
from flask_restful import Api
import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config["CACHE_TYPE"] = "FileSystemCache"
app.config["CACHE_DIR"] = os.path.join(app.instance_path, "cache")


##instantiate Database module after app.config is ready


def main():
    ##Initialize database module for use. 

    app.run(port=8001, debug=True)

    
    
    #testfunction()
 
##For testing the database functions
def testfunction():
    job_test_packet2 = {'id': 4,}
    user_test_packet2 = {'id': 4,}
    Database.instantiateDatabase()
    Database.populate_database()
    print("attempt deletion of job")
    Database.delete_job_by_id(3)
    print("attempt deletion of user")
    Database.delete_user_by_id(2)
   
    print("test query all ")
    jobs = Database.query_job_all()
    if jobs:
        for job in jobs: # type: ignore
            print(job)
    
    print("test query by generic ")
    jobs = Database.query_job(job_test_packet2)
    if jobs:
        for job in jobs: # type: ignore
            print(job)
    print("test query users by generic dict")
    users = Database.query_user(user_test_packet2)
    print("Print queryresults")
    if users:
        for user in users: # type: ignore
            print(user)

    """"""
if __name__ == "__main__":
    main()


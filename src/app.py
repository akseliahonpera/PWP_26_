import datetime
from db_package import database_ORM
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

job_test_packet2 = {'id': 4,}

user_test_packet2 = {'id': 4,}


##For testing the database
def main():
    database_ORM.createDatabase()
    #database_ORM.populate_database()
    #print("attempt deletion of job")
    #database_ORM.delete_job(3)
    #print("attempt deletion of user")
    #database_ORM.delete_user(2)
    
    print("test query all ")
   # jobs = database_ORM.query_job_all(None)

   # for job in jobs: # type: ignore
    #    print(job)
    
    print("test query by generic ")
    jobs = database_ORM.query_job(job_test_packet2)

    for job in jobs: # type: ignore
        print(job)
    print("test query users by generic dict")
    users = database_ORM.query_user(user_test_packet2)
    for user in users: # type: ignore
        print(user)




if __name__ == "__main__":
    main()


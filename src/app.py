import datetime
import database_ORM
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)





def main():
    database_ORM.createDatabase()
    database_ORM.populate_database()
    print("attempt deletion of job")
    database_ORM.delete_job(1)
    print("attempt deletion of user")
    database_ORM.delete_user(1)




if __name__ == "__main__":
    main()


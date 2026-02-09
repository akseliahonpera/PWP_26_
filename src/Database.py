from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re
import config
app = Flask(__name__)


app.secret_key = config.SECRET_KEY

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_PORT'] = config.MYSQL_PORT

mysqlInstance = MySQL(app)




def create_database(mysql):
    print("Creating database ")
    try:
        with app.app_context():
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('CREATE DATABASE IF NOT EXISTS '+config.MYSQL_DB)
            mysql.connection.commit()
            cursor.close()
            print("Database created")
            app.config['MYSQL_DB']= config.MYSQL_DB
            return True
    except Exception as e:
        print("db failed",e)
        return False



def checkIfDataBaseExists(mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    databases = cursor.execute("SHOW DATABASES")
    cursor.close()
    for database in databases:
        print(database)
    

def create_user_table(mysql):
    print("Creating user table ")
    try:
        with app.app_context():
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(50) NOT NULL UNIQUE,
                                password VARCHAR(100) NOT NULL,
                                email VARCHAR(100) NOT NULL UNIQUE,
                                address VARCHAR(255) NOT NULL,
                                phoneNumber VARCHAR(15) NOT NULL,
                                description VARCHAR(255)
                            )''')
            mysql.connection.commit()
            cursor.close()
            print("User table created")
            return True
    except Exception as e:
        print("user table failed",e )
        return False


def create_job_table(mysql):
    print("Creating job table")
    try:
        with app.app_context():
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        userID INT NOT NULL,
                        jobDescription VARCHAR(255) NOT NULL,
                        timetable INT,
                        location VARCHAR(127),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        opening_hours VARCHAR(127),
                        category VARCHAR(31) NOT NULL
                        )''')
            mysql.connection.commit()
            cursor.close()
            print("job table created")
            return True
    except Exception as e:
        print("job table failed",e)
        return False


def insert_to_user_table():
    NotImplementedError
def insert_to_job_table():
    NotImplementedError

def main():
    print("start main")
    #app.run()
    db_flag = create_database(mysqlInstance)
    user_table_flag = create_user_table(mysqlInstance)
    job_table_flag = create_job_table(mysqlInstance)
    print("end main")
    print(f"Db was created:{db_flag}, user table was created: {user_table_flag}, job table was created : {job_table_flag}")

if __name__ == '__main__':
    main()


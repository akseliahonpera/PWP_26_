# PWP SPRING 2026
# PROJECT NAME Väinämöinen
# Group information
* Student 1. Akseli Ahonpera aahonper20@student.oulu.fi
* Student 2. Tino Marttila tmarttil22@student.oulu.fi
* Student 3. Miro Sirviö msirvio22@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__


This software is requires following:

MYSQL server running on localhost
Create database to the MYSQL server through MYSQL shell by using CREATE DATABASE IF NOT EXISTS <yourdb>.

Populate the database by running the database_ORM.py directly or by using source <resource_path> for the dump file in test_dumpfiles_db folder.
 
- install following with pip
datetime
flask
flask_sqlalchemy
sqlalchemy_utils


Make yourself a config.py file to the src folder.

MYSQL_HOST = "localhost"    //- default
MYSQL_USER = "root"         //- default for MYSQL 8.0 atleast, if you have other profiles then use whatever you like
MYSQL_PASSWORD = ""         //- your mysql server password
MYSQL_PORT = "3306"         //- default MYSQL
MYSQL_DB = ""               //- your desired name for the database as in line 4 <yourdb>
SECRET_KEY = ""             //- irrelevant in this



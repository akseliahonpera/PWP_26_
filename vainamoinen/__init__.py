import os
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from . import config

db = SQLAlchemy()
cache = Cache()

"""
From course material
"""

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",           # test: "sqlite:///test.db"
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset=utf8mb4',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    print("db path:" + app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)
    cache.init_app(app)


    from . import Database
    with app.app_context():
        Database.init_db()

    
    from . import api
    from .utils import UserConverter, JobConverter#, TimeTableConverter

    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["job"] = JobConverter
    #app.url_map.converters["timetable"] = TimeTableConverter

    app.register_blueprint(api.api_bp)

    return app
"""
From course material
"""
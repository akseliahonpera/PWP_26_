'''
__init__.py -file
'''

import os
from flask import Flask
from flasgger import Swagger
#from flask_caching import Cache
from . import api
from .database import db
from flask_cors import CORS, cross_origin
#cache = Cache()


# From course material


def create_app(test_config=None):
    '''
    Create an app.

    Parameters:
        test_config...
    '''

    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*":{"origins":"http://localhost:3000"
        }
    })
    #this is also fine here (Probably)
    from .utils import UserConverter, JobConverter, TimeTableConverter # pylint: disable=import-outside-toplevel

    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["job"] = JobConverter
    app.url_map.converters["timetable"] = TimeTableConverter

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.config["SWAGGER"] = {
    "title": "Väinämöinen API",
    "openapi": "3.0.4",
    "uiversion": 3,
    }

    Swagger(app, template_file="doc/vainamoinen.yml")

    app.register_blueprint(api.api_bp)

    # This is also fine here (Probably)
    from . import database # pylint: disable=import-outside-toplevel
    app.cli.add_command(database.init_db_command)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    #cache.init_app(app)

    with app.app_context():
        database.init_db()

    # Uncomment to check db (should be the instance/development.db as for now)
    #print(app.config["SQLALCHEMY_DATABASE_URI"])

    return app

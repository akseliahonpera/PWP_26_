'''
__init__.py -file
'''

import os
from flask import Flask
#from flask_caching import Cache
from . import api
from .database import db

#cache = Cache()


# From course material


def create_app(test_config=None):
    '''
    Create an app.

    Parameters:
        test_config...
    '''

    app = Flask(__name__, instance_relative_config=True)

    from .utils import UserConverter, JobConverter, TimeTableConverter # pylint: disable=import-outside-toplevel, this is also fine here (Probably)

    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["job"] = JobConverter
    app.url_map.converters["timetable"] = TimeTableConverter

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.register_blueprint(api.api_bp)

    from . import database # pylint: disable=import-outside-toplevel, this is also fine here (Probably)
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

    return app

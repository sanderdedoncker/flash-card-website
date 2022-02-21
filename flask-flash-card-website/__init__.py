"""
Initialization and app factory for the Flask project
See https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # db set as global variable outside of the app -> makes library accessible anywhere
# TODO: configure SQLAlchemy database


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    # TODO: undo hardcoded config here
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flash-card-website.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # TODO: write external config file
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # TODO: from_mapping vs from_pyfile??
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
"""
Initialization and app factory for the Flask project
See https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
Also https://hackersandslackers.com/flask-application-factory/

Database also linked following the "Application factory" pattern
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
"""

from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # db set as global variable outside of the app -> makes library accessible anywhere
# TODO: configure SQLAlchemy database


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # Load the instance config when not testing
        config_dir = path.abspath(path.dirname(path.dirname(__file__)))  # Config is in this file's parent directory
        app.config.from_pyfile(path.join(config_dir, 'config.py'))
    else:
        # Load the test config if passed in
        # TODO: from_mapping vs from_pyfile??
        app.config.from_mapping(test_config)

    # Initialize SQLAlchemy database on the created app
    db.init_app(app)

    # Push the context for the app
    with app.app_context():

        db.create_all()

        # a simple page that says hello
        @app.route('/')
        def hello():
            return 'Hello, World!'

        return app


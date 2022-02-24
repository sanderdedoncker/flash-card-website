"""
Initialization and app factory for the Flask project, see
https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
https://hackersandslackers.com/flask-application-factory/

Explanation of blueprints and views see
https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
https://hackersandslackers.com/flask-blueprints/

Database also linked following the "Application factory" pattern
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/

Sander Dedoncker, 2022
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
        app.config.from_mapping(test_config)

    # Initialize SQLAlchemy database on the created app
    db.init_app(app)

    # Push the context for the app
    with app.app_context():

        # Import and register homepage blueprint
        from .home import views as home_views
        app.register_blueprint(home_views.bp)

        # Import and register authentication blueprint
        from .auth import views as auth_views
        app.register_blueprint(auth_views.bp)

        db.create_all()

        return app


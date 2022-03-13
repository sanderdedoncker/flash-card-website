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
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()  # db as variable outside of the app -> makes it accessible anywhere before app creation
# TODO: configure SQLAlchemy database
login = LoginManager()  # login as variable outside of app factory -> makes it accessible anywhere before app creation


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

    # Initialize Flask-Login login manager on the created app
    login.init_app(app)

    # Link the Flask-Bootstrap library to the created app
    Bootstrap(app)

    # Push the context for the app
    with app.app_context():

        # Import and register homepage blueprint
        from .home import views as home_views
        app.register_blueprint(home_views.bp)

        # Import and register authentication blueprint
        from .auth import views as auth_views
        app.register_blueprint(auth_views.bp)

        # Import and register cards blueprint
        from .cards import views as card_views
        app.register_blueprint(card_views.bp)

        # Import and register learn blueprint
        from .learn import views as learn_views
        app.register_blueprint(learn_views.bp)

        # TODO: User profile pages
        # TODO: Card game - JS?
        # TODO: Card overview/collections
        # TODO: Public and private cards/collections
        # TODO: Admin pages
        # TODO: API
        # TODO: Nicer styling

        db.create_all()

        return app


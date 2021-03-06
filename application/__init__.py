"""
Initialization and app factory for the Flask project, see
https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
https://hackersandslackers.com/flask-application-factory/

Explanation of blueprints and views see
https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
https://hackersandslackers.com/flask-blueprints/

Database also linked following the "Application factory" pattern
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/

For lots of general info and design guidelines, see M. Grinberg Flask Megatutorial
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Sander Dedoncker, 2022
"""

from os import path

from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate


# Constraint naming convention to ease migrations:
# https://stackoverflow.com/questions/62640576/flask-migrate-valueerror-constraint-must-have-a-name
# Attention: I added this later, so the SQLite constraints from before the first migration are still unnamed!
# If you need those removed, see also the SO topic
# db as variable outside of the app -> makes it accessible anywhere before app creation
db = SQLAlchemy(metadata=MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}))
migrate = Migrate()
login = LoginManager()  # login as variable outside of app factory -> makes it accessible anywhere before app creation
bootstrap = Bootstrap()


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

    # Initialize Flask-Migrate database migration tool on the created app and db
    migrate.init_app(app, db, render_as_batch=True)

    # Initialize Flask-Login login manager on the created app
    login.init_app(app)

    # Initialize Flask-Bootstrap instance to the created app
    bootstrap.init_app(app)

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

        # Import and register user blueprint
        from .user import views as user_views
        app.register_blueprint(user_views.bp)

        # Import and register api blueprint
        from .api import bp as api_bp
        app.register_blueprint(api_bp)

        # TODO: Card collections
        # TODO: Public and private cards/collections
        # TODO: Admin pages
        # TODO: Nicer styling

        return app


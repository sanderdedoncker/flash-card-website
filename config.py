""" Flask configuration """
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# TODO: use config (sub)classing
# App
TESTING = False if environ.get('FLASK_ENV') == "production" else True
EXPLAIN_TEMPLATE_LOADING = False
SECRET_KEY = environ.get('SECRET_KEY')

# Database
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL').replace(
        'postgres://', 'postgresql://') \
    if environ.get('FLASK_ENV') == "production" else environ.get('DEV_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False if environ.get('FLASK_ENV') == "production" else True

""" Flask configuration """
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# App
TESTING = True
SECRET_KEY = environ.get('SECRET_KEY')

# Database
SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
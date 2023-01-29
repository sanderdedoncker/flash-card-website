""" Flask configuration """
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# App
TESTING = False if environ.get('FLASK_ENV') == "production" else True
EXPLAIN_TEMPLATE_LOADING = False
SECRET_KEY = environ.get('SECRET_KEY')

# Database -- see azureproject/production.py at https://github.com/Azure-Samples/msdocs-flask-postgresql-sample-app
SQLALCHEMY_DATABASE_URI = DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=environ.get('DBUSER'),
    dbpass=environ.get('DBPASS'),
    dbhost=environ.get('DBHOST') + ".postgres.database.azure.com",
    dbname=environ.get('DBNAME')
) if environ.get('FLASK_ENV') == "production" else environ.get('DEV_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False if environ.get('FLASK_ENV') == "production" else True

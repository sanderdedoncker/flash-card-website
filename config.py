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
SQLALCHEMY_DATABASE_URI = "postgresql://zbjqeocxriauhb:a6ff7568c0439b1f771824b786ede334f6bccaf79eedbe7dc9c2b651b0883837@ec2-52-73-155-171.compute-1.amazonaws.com:5432/dem7lf9q4td77j"

# environ.get('DATABASE_URL').replace(
#         'postgres://', 'postgresql://') \
#     if environ.get('FLASK_ENV') == "production" else environ.get('DEV_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False if environ.get('FLASK_ENV') == "production" else True

from flask import Blueprint


bp = Blueprint(name='api', import_name=__name__, url_prefix='/api')

from application.api import cards, errors, auth, tokens

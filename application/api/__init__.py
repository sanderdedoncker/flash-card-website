from flask import Blueprint


API_DOCS_URL = "https://documenter.getpostman.com/view/21200551/Uz5CKxWk"

bp = Blueprint(name='api', import_name=__name__, url_prefix='/api')

from application.api import cards, errors, auth, tokens

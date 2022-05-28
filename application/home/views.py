from flask import Blueprint, render_template

from application.api import API_DOCS_URL


# # Blueprint configuration
bp = Blueprint(name="home", import_name=__name__, template_folder="templates", static_folder="static")

# # Views


# a simple page that says hello
@bp.route("/", methods=["GET"])
def home():
    return render_template("index.html", api_docs_url=API_DOCS_URL)

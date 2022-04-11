from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from application.models import User, Card, Score
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="user", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/user")


# # Views
@login_required
@bp.route("/", methods=["GET"])
def profile():
    user = User.query.get(current_user.id)
    if user:
        return render_template("user_profile.html", user=user)
    return abort(404)


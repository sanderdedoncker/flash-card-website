from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from application.models import User, Card
from application import db, login
import random
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="learn", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/learn")


@login_required
@bp.route("/", methods=["GET", "POST"])
def learn():
    all_user_cards = Card.query.filter_by(user_id=current_user.id).all()
    random_user_card = random.choice(all_user_cards)
    return render_template("learn.html", card=random_user_card)
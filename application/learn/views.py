from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from application.models import User, Card, Score
from application import db, login
import random
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="learn", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/learn")


# # Views
@login_required
@bp.route("/", methods=["GET"])
def learn():
    all_user_cards = Card.query.filter_by(user_id=current_user.id).all()
    if not all_user_cards:
        flash("You have no cards yet!")
        return redirect(url_for("cards.cards"))
    random_user_card = random.choice(all_user_cards)
    user_card_score = Score.query.filter_by(user_id=current_user.id, card_id=random_user_card.id).one_or_none()
    if not user_card_score:
        user_card_score = Score(
            user_id=current_user.id,
            card_id=random_user_card.id
        )
        db.session.add(user_card_score)
        db.session.commit()
    return render_template("learn.html", card=random_user_card, score=user_card_score)


@login_required
@bp.route("/<int:card_id>/level-up", methods=["GET"])
def level_up(card_id):
    user_card_score = Score.query.filter_by(user_id=current_user.id, card_id=card_id).one_or_none()
    if user_card_score:
        if user_card_score.score < 5:
            user_card_score.score += 1
        user_card_score.last_seen_on = datetime.now()
        db.session.commit()
        print(user_card_score.score)
    return redirect(url_for("learn.learn"))


@login_required
@bp.route("/<int:card_id>/level-down", methods=["GET"])
def level_down(card_id):
    user_card_score = Score.query.filter_by(user_id=current_user.id, card_id=card_id).one_or_none()
    if user_card_score:
        if user_card_score.score > 0:
            user_card_score.score -= 1
        user_card_score.last_seen_on = datetime.now()
        db.session.commit()
        print(user_card_score.score)
    return redirect(url_for("learn.learn"))

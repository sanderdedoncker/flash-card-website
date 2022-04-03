from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from application.models import User, Card, Score
from application import db, login
from .rules import is_reviewable, correct_recall, incorrect_recall
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="learn", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/learn")


# # Views
@login_required
@bp.route("/", methods=["GET"])
def learn():

    all_user_cards_scores = db.session.query(Card, Score). \
        outerjoin(Score). \
        filter(Card.user_id == current_user.id). \
        filter((Score.user_id == current_user.id) | (Score.user_id == None)). \
        all()

    if not all_user_cards_scores:
        flash("You have no cards yet!")
        return redirect(url_for("cards.cards"))

    for card, score in all_user_cards_scores:
        if score:
            if is_reviewable(score.score, score.last_seen_on):
                return render_template("learn.html", card=card, score=score)
        else:  # Unseen card -> always review, create new score for it
            score = Score(
                user_id=current_user.id,
                card_id=card.id
            )
            db.session.add(score)
            db.session.commit()
            return render_template("learn.html", card=card, score=score)

    return render_template("nothing_to_learn.html")


@login_required
@bp.route("/<int:card_id>/right", methods=["GET"])
def right(card_id):
    user_card_score = Score.query.filter_by(user_id=current_user.id, card_id=card_id).one_or_none()
    if user_card_score:
        user_card_score.score = correct_recall(user_card_score.score)
        user_card_score.last_seen_on = datetime.now()
        db.session.commit()
    return redirect(url_for("learn.learn"))


@login_required
@bp.route("/<int:card_id>/wrong", methods=["GET"])
def wrong(card_id):
    user_card_score = Score.query.filter_by(user_id=current_user.id, card_id=card_id).one_or_none()
    if user_card_score:
        user_card_score.score = incorrect_recall(user_card_score.score)
        user_card_score.last_seen_on = datetime.now()
        db.session.commit()
    return redirect(url_for("learn.learn"))

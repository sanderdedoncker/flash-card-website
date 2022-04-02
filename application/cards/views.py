from flask import Blueprint, render_template, redirect, url_for, flash, abort
from .forms import AddCardForm, EditCardForm, ResetCardForm, DeleteCardForm
from flask_login import current_user, login_required
from application.models import User, Card, Score
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="cards", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/cards")


# # Views
@login_required
@bp.route("/", methods=["GET"])
def cards():
    # TODO: Checking card content safety
    all_user_cards_scores = db.session.query(Card, Score).\
                            outerjoin(Score).\
                            filter(Card.user_id == current_user.id).\
                            filter((Score.user_id == current_user.id) | (Score.user_id == None)).\
                            all()
    return render_template("cards.html", cards_scores=all_user_cards_scores)


@login_required
@bp.route("/<int:card_id>", methods=["GET"])
def card_detail(card_id):
    # TODO: Maybe do edit and delete directly in this page
    # TODO: Checking card content safety
    card = Card.query.get(card_id)
    score = Score.query.filter_by(user_id=current_user.id, card_id=card.id).one_or_none()
    if card:
        if card.user.id == current_user.id:
            return render_template("card_detail.html", card=card, score=score)
        else:
            return abort(403)
    else:
        return abort(404)


@login_required
@bp.route("/add", methods=["GET", "POST"])
def add_card():
    add_card_form = AddCardForm()
    if add_card_form.validate_on_submit():
        new_card = Card(
            front=add_card_form.front.data,
            back=add_card_form.back.data,
            user_id=current_user.id,
            added_on=datetime.now()
        )
        db.session.add(new_card)
        db.session.commit()
        flash("New card added successfully.")
        return redirect(url_for("cards.cards"))
    return render_template("add_card.html", form=add_card_form)


@login_required
@bp.route("/<int:card_id>/edit", methods=["GET", "POST"])
def edit_card(card_id):
    card = Card.query.get(card_id)
    if card:
        edit_card_form = EditCardForm(front=card.front, back=card.back)
        if edit_card_form.validate_on_submit():
            card.front = edit_card_form.front.data
            card.back = edit_card_form.back.data
            db.session.commit()
            flash("Card edited successfully.")
            return redirect(url_for("cards.cards"))
        return render_template("edit_card.html", form=edit_card_form)
    else:
        return abort(404)


@login_required
@bp.route("/<int:card_id>/reset", methods=["GET", "POST"])
def reset_card(card_id):
    card = Card.query.get(card_id)
    score = Score.query.filter_by(user_id=current_user.id, card_id=card.id).one_or_none()
    if not score:
        return redirect(url_for("cards.card_detail", card_id=card_id))
    if card:
        reset_card_form = ResetCardForm()
        if reset_card_form.validate_on_submit():
            db.session.delete(score)
            db.session.commit()
            flash("Score reset successfully.")
            return redirect(url_for("cards.cards"))
        return render_template("reset_card.html", form=reset_card_form)
    else:
        return abort(404)


@login_required
@bp.route("/<int:card_id>/delete", methods=["GET", "POST"])
def delete_card(card_id):
    # TODO: Make this nicer with a confirmation popup before accessing the link, instead of form there
    # TODO: Accept "DELETE" requests?
    card = Card.query.get(card_id)
    if card:
        delete_card_form = DeleteCardForm()
        if delete_card_form.validate_on_submit():
            db.session.delete(card)
            db.session.commit()
            flash("Card deleted successfully.")
            return redirect(url_for("cards.cards"))
        return render_template("delete_card.html", form=delete_card_form)
    else:
        return abort(404)

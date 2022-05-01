from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from .forms import AddCardForm, EditCardForm, ResetCardForm, DeleteCardForm
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_args
from application.models import User, Card, Score
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="cards", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/cards")


# # Views
@bp.route("", methods=["GET"])
@login_required
def cards():
    # TODO: Checking card content
    user_cards_scores = current_user.query_cards_scores()

    query = request.args.get("query")
    if query:
        user_cards_scores = user_cards_scores.filter(Card.front.contains(query) | Card.back.contains(query))

    sort = request.args.get("sort")
    order = request.args.get("order")
    if sort == "added" and order == "up":
        user_cards_scores = user_cards_scores.order_by(Card.added_on.asc())
    if sort == "added" and order == "down":
        user_cards_scores = user_cards_scores.order_by(Card.added_on.desc())
    if sort == "level" and order == "up":
        user_cards_scores = user_cards_scores.order_by(Score.score.asc().nulls_first())
    if sort == "level" and order == "down":
        user_cards_scores = user_cards_scores.order_by(Score.score.desc().nulls_last())
    if sort == "seen" and order == "up":
        user_cards_scores = user_cards_scores.order_by(Score.last_seen_on.asc().nulls_first())
    if sort == "seen" and order == "down":
        user_cards_scores = user_cards_scores.order_by(Score.last_seen_on.desc().nulls_last())

    page, per_page, _ = get_page_args()
    user_cards_scores = user_cards_scores.paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, per_page=per_page, total=user_cards_scores.total,
                            inner_window=2, outer_window=0)

    return render_template("cards.html", cards_scores=user_cards_scores.items, pagination=pagination,
                           query=query, sort=sort, order=order, per_page=per_page)


@bp.route("/<int:card_id>", methods=["GET"])
@login_required
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


@bp.route("/add", methods=["GET", "POST"])
@login_required
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


@bp.route("/<int:card_id>/edit", methods=["GET", "POST"])
@login_required
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


@bp.route("/<int:card_id>/reset", methods=["GET", "POST"])
@login_required
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


@bp.route("/<int:card_id>/delete", methods=["GET", "POST"])
@login_required
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

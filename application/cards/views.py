from flask import Blueprint, render_template, redirect, url_for, flash, abort
from .forms import AddCardForm, EditCardForm, DeleteCardForm
from flask_login import current_user, login_required
from application.models import User, Card
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="cards", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/cards")


@login_required
@bp.route("/", methods=["GET"])
def cards():
    # TODO: Checking card content safety
    all_user_cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template("cards.html", cards=all_user_cards)


@login_required
@bp.route("/<int:card_id>", methods=["GET"])
def card_detail(card_id):
    # TODO: Maybe do edit and delete directly in this page
    # TODO: Checking card content safety
    card = Card.query.get(card_id)
    if card:
        if card.user.id == current_user.id:
            return render_template("card_detail.html", card=card)
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
@bp.route("/edit/<int:card_id>", methods=["GET", "POST"])
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
@bp.route("/delete/<int:card_id>", methods=["GET", "POST"])
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


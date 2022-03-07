from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import AddCardForm
from flask_login import current_user, login_required
from application.models import User, Card
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="cards", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/cards")


@login_required
@bp.route("/", methods=["GET"])
def cards():
    all_user_cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template("cards.html", cards=all_user_cards)


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
@bp.route("/edit/<int:card_id>", methods=["GET", "PUT"])
def edit_card(card_id):
    return f"Edit card {card_id} via form"


@login_required
@bp.route("/delete/<int:card_id>", methods=["GET", "DELETE"])
def delete_card(card_id):
    return f"Confirm deletion of card {card_id}"
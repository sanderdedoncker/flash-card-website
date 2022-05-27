from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user

from application import db
from application.models import User
from application.learn.rules import is_reviewable
from .forms import EditUserForm, ResetPasswordForm, DeleteUserForm

# # Blueprint configuration
bp = Blueprint(name="user", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/user")


# # Views
@bp.route("", methods=["GET"])
@login_required
def profile():

    all_user_cards_scores = current_user.query_cards_scores().all()
    unseen = 0
    score_stats = {}
    total_stat = {"reviewed": 0, "reviewable": 0}
    for card, score in all_user_cards_scores:
        if score:
            if score.score not in score_stats:
                score_stats[score.score] = {"reviewed": 0, "reviewable": 0}
            if is_reviewable(score.score, score.last_seen_on):
                score_stats[score.score]["reviewable"] += 1
                total_stat["reviewable"] += 1
            else:
                score_stats[score.score]["reviewed"] += 1
                total_stat["reviewed"] += 1
        else:
            unseen += 1
            total_stat["reviewable"] += 1

    score_stats = dict(sorted(score_stats.items()))
    total = total_stat["reviewable"] + total_stat["reviewed"]

    return render_template("user_profile.html", user=current_user, unseen=unseen, total=total,
                           score_stats=score_stats, total_stat=total_stat)


@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    edit_user_form = EditUserForm(username=current_user.username, email=current_user.email)
    if edit_user_form.validate_on_submit():
        if current_user.email != edit_user_form.email.data and User.query.filter_by(email=edit_user_form.email.data).first():
            flash("This email address is already registered by another user.")
            return redirect(url_for("user.edit_user"))
        current_user.username = edit_user_form.username.data
        current_user.email = edit_user_form.email.data
        db.session.commit()
        flash("User edited successfully.")
        return redirect(url_for("user.profile"))
    return render_template("edit_user.html", form=edit_user_form)


@bp.route("/reset_password", methods=["GET", "POST"])
@login_required
def reset_password():
    # TODO: Password reset via email
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():
        current_user.set_password(reset_password_form.password.data)
        db.session.commit()
        flash("Password changed successfully.")
        return redirect(url_for("user.profile"))
    return render_template("reset_password.html", form=reset_password_form)


@bp.route("/delete", methods=["GET", "POST"])
@login_required
def delete_user():
    # TODO: Make this nicer with a confirmation popup before accessing the link, instead of form there
    # TODO: Accept "DELETE" requests?
    delete_user_form = DeleteUserForm()
    if delete_user_form.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash("User deleted successfully.")
        return redirect(url_for("home.home"))
    return render_template("delete_user.html", form=delete_user_form)


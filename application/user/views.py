from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from application.models import User, Card, Score
from application.learn.rules import is_reviewable
from application import db, login
from datetime import datetime


# # Blueprint configuration
bp = Blueprint(name="user", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/user")


# # Views
@bp.route("/", methods=["GET"])
@login_required
def profile():

    all_user_cards_scores = current_user.get_cards_scores()
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


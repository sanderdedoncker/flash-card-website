from flask import Blueprint, render_template, redirect, url_for


# # Blueprint configuration
bp = Blueprint(name="auth", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/auth")


# # Views

@bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@bp.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("home.home"))

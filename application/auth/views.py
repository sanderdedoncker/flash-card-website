from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm


# # Blueprint configuration
bp = Blueprint(name="auth", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/auth")


# # Views

@bp.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        flash("Registration Successful!")
        return redirect(url_for("home.home"))
    return render_template("register.html", form=register_form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash("Login Successful!")
        return redirect(url_for("home.home"))
    return render_template("login.html", form=login_form)


@bp.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("home.home"))

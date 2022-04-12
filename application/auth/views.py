from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
from application import db, login


# # Blueprint configuration
bp = Blueprint(name="auth", import_name=__name__, template_folder="templates", static_folder="static", url_prefix="/auth")


# # Login manager setup
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# # Views
@bp.route("/register", methods=["GET", "POST"])
def register():
    # TODO: account activation via email
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("This email address is already registered.", category="error")  # TODO: Categorize flash messages
            return redirect(url_for("auth.register"))
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
        )
        new_user.set_password(register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for("home.home"))
    return render_template("register.html", form=register_form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  # TODO: Password reset
        flash("You are already logged in.")
        return redirect(url_for("home.home"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if not user or not user.check_password(login_form.password.data):
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))
        login_user(user)
        flash("Login successful!")
        return redirect(url_for("home.home"))
    return render_template("login.html", form=login_form)


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You are now logged out.")
    return redirect(url_for("home.home"))


@bp.route("/secret")
@login_required
def secret_route():
    return "You found the secret!"

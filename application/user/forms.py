from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo


class EditUserForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Password",
                                     validators=[DataRequired(), EqualTo("password", message='Passwords must match.')])
    submit = SubmitField(label="Submit")


class DeleteUserForm(FlaskForm):
    confirm_delete = SubmitField(label="Confirm user deletion")
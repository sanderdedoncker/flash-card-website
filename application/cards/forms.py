from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddCardForm(FlaskForm):
    front = StringField(label="Front text", validators=[DataRequired()])
    back = StringField(label="Back text", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class EditCardForm(FlaskForm):
    front = StringField(label="Front text", validators=[DataRequired()])
    back = StringField(label="Back text", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class DeleteCardForm(FlaskForm):
    confirm_delete = SubmitField(label="Confirm deletion")


class ResetCardForm(FlaskForm):
    confirm_reset = SubmitField(label="Confirm reset")

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddCardForm(FlaskForm):
    front = StringField(label="Front text", validators=[DataRequired()])
    back = StringField(label="Back text", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
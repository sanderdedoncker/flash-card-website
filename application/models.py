from . import db

from sqlalchemy.orm import relationship
from datetime import datetime


## Models
class User(db.Model):
    """User: contains data on website users."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    # User relates to Card via Score
    scores = relationship("Score", back_populates="user")


class Card(db.Model):
    """Card: contains data on the flash cards. For now, cards only support string content."""
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text, nullable=False)  # Text type has unlimited length
    back = db.Column(db.Text, nullable=False)

    # Card relates to User via Score
    scores = relationship("Score", back_populates="card")


class Score(db.Model):
    """Score: contains data on the score a User has for a Card."""
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.min)  # Default to earliest possible time.
    score = db.Column(db.Integer, nullable=False)

    # Score is the many-to-many association between User and Card
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="scores")

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"))
    card = relationship("Card", back_populates="scores")




from datetime import datetime, timedelta
import base64
import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from application import db


# # Models
class User(UserMixin, db.Model):
    """User: contains data on website users."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String(32), unique=True)
    token_expiration = db.Column(db.DateTime)

    # User relates to Card via Score
    scores = relationship("Score", back_populates="user", cascade="delete, all")

    # User relates to Card (one-to-many), being creator
    cards = relationship("Card", back_populates="user", cascade="delete, all")

    def set_password(self, password):
        #  https://security.stackexchange.com/questions/110084/parameters-for-pbkdf2-for-password-hashing/110106#110106
        # Werkzeug defaults seem to have built-in (adaptive?) number of iterations
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def query_cards_scores(self):
        cards_scores = db.session.query(Card, Score). \
            outerjoin(Score). \
            filter(Card.user_id == self.id). \
            filter((Score.user_id == self.id) | (Score.user_id == None))
        return cards_scores


class Card(db.Model):
    """Card: contains data on the flash cards. For now, cards only support string content."""
    # TODO: Markup of code and math
    # TODO: Card tags or collections
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.min)  # Default to earliest possible time.
    private = db.Column(db.Boolean, nullable=False, default=True)  # Default to private card
    front = db.Column(db.Text, nullable=False)  # Text type has unlimited length
    back = db.Column(db.Text, nullable=False)

    # Card relates to User via Score
    scores = relationship("Score", back_populates="card", cascade="delete, all")

    # Card relates to User (many-to-one) who is creator
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="cards")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "added_on": self.added_on.isoformat(),
            "private": self.private,
            "front": self.front,
            "back": self.back,
        }

    def from_dict(self, data):
        for field in ["front", "back", "private"]:
            if field in data:
                setattr(self, field, data[field])


class Score(db.Model):
    # TODO: refactor -> Level?
    """Score: contains data on the score a User has for a Card. Follows the SQLAlchemy 'Association Object' pattern."""
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    last_seen_on = db.Column(db.DateTime, nullable=False, default=datetime.now())  # Default to score creation time.
    score = db.Column(db.Integer, nullable=False, default=0)

    # Score is the many-to-many association between User and Card
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="scores")

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"))
    card = relationship("Card", back_populates="scores")

    def to_dict(self):
        return {
            "id": self.id,
            "card_id": self.card_id,
            "user_id": self.user_id,
            "last_seen_on": self.last_seen_on.isoformat(),
            "score": self.score,
        }

# TODO: Card collections?
# TODO: Score history?




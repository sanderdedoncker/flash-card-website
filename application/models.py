from application import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import relationship
from datetime import datetime


# # Models
class User(UserMixin, db.Model):
    """User: contains data on website users."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

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


class Card(db.Model):
    """Card: contains data on the flash cards. For now, cards only support string content."""
    # TODO: Markup of code and math
    # TODO: Card tags or collections
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.min)  # Default to earliest possible time.
    private = db.Column(db.Boolean, nullable=False, default=False)  # Default to public card
    front = db.Column(db.Text, nullable=False)  # Text type has unlimited length
    back = db.Column(db.Text, nullable=False)

    # Card relates to User via Score
    scores = relationship("Score", back_populates="card", cascade="delete, all")

    # Card relates to User (many-to-one) who is creator
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="cards")


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

# TODO: Card collections?
# TODO: Score history?




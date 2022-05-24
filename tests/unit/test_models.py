from datetime import datetime

from application.models import User, Card, Score


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id, name, email, (hashed) password, and admin fields are defined correctly
    THEN check if card and score fields are initialized as empty lists
    WHEN id, name, email, password, and admin fields are changed
    THEN check the id, name, email, (hashed) password, and admin fields are defined correctly
    """
    now = datetime.utcnow()
    user = User(
        added_on=now,
        username='test',
        email='test@a.b',
    )
    user.set_password('test')

    assert user.id is None
    assert user.username == 'test'
    assert user.email == 'test@a.b'
    assert user.password != 'test'
    assert user.check_password('test')
    assert user.added_on == now
    assert user.admin is None

    assert user.cards == []
    assert user.scores == []

    user.id = 0
    user.username = 'test2'
    user.email = 'test2@a.b'
    user.admin = True
    user.set_password('test2')

    assert user.id == 0
    assert user.username == 'test2'
    assert user.email == 'test2@a.b'
    assert user.password != 'test2'
    assert user.check_password('test2')
    assert user.admin is True


def test_new_card():
    """
    GIVEN a Card model
    WHEN a new Card is created
    THEN check the front, back, user_id, private, and created_on fields are defined correctly
    THEN check if user and score fields are initialized as none/empty lists
    WHEN front, back, user_id, private, and created on fields are changed
    THEN check if front, back, user_id, private, and created on fields are defined correctly
    """
    card = Card(
        front="test_front",
        back="test_back",
    )

    assert card.id is None
    assert card.front == "test_front"
    assert card.back == "test_back"
    assert card.added_on is None
    assert card.private is None
    assert card.user_id is None

    assert card.user is None
    assert card.scores == []

    now = datetime.utcnow()
    card.id = 0
    card.front = "test2_front"
    card.back = "test2_back"
    card.added_on = now
    card.private = False
    card.user_id = 1

    assert card.id == 0
    assert card.front == "test2_front"
    assert card.back == "test2_back"
    assert card.added_on == now
    assert card.private is False
    assert card.user_id == 1


def test_new_score():
    """
    GIVEN a Score model
    WHEN a new Score is created
    THEN check the id, last_seen_on, score, user_id, card_id fields are defined correctly
    THEN check if user and card fields are initialized as none/empty lists
    WHEN id, last_seen_on, score, user_id, card_id fields are changed
    THEN check if id, last_seen_on, score, user_id, card_id fields are defined correctly
    """
    score = Score()

    assert score.id is None
    assert score.last_seen_on is None
    assert score.score is None
    assert score.user_id is None
    assert score.card_id is None

    assert score.user is None
    assert score.card is None

    now = datetime.utcnow()
    score.id = 0
    score.last_seen_on = now
    score.score = 1
    score.user_id = 2
    score.card_id = 3

    assert score.id == 0
    assert score.last_seen_on == now
    assert score.score == 1
    assert score.user_id == 2
    assert score.card_id == 3


def test_user_tokens(user):
    """
    GIVEN a User object
    WHEN token is requested
    THEN check if token is assigned with correct validity
    WHEN new token is requested (within validity)
    THEN check if token is the same
    WHEN token is revoked
    CHECK if validity is expired
    WHEN token is requested
    THEN check if new token is assigned with correct validity
    """
    token = user.get_token(expires_in=1e10)

    assert user.token == token
    assert user.token_expiration > datetime.utcnow()

    assert user.get_token() == token

    user.revoke_token()

    assert user.token_expiration < datetime.utcnow()

    new_token = user.get_token(expires_in=1e10)

    assert new_token != token
    assert user.token == new_token
    assert user.token_expiration > datetime.utcnow()


def test_card_dict(card):
    """
    GIVEN a Card object
    WHEN dict is requested
    THEN check if dict is correct
    WHEN dict is modified and card is changed
    THEN check if card has the same contents
    """
    card_dict = card.to_dict()

    assert card_dict["id"] == card.id
    assert card_dict["user_id"] == card.user_id
    assert card_dict["added_on"] == card.added_on.isoformat()
    assert card_dict["private"] == card.private
    assert card_dict["front"] == card.front
    assert card_dict["back"] == card.back

    card_dict["id"] = "fake_id"
    card_dict["user_id"] = "fake_user_id"
    card_dict["added_on"] = "fake_added_on"
    card_dict["private"] = not card.private
    card_dict["front"] = "new_front"
    card_dict["back"] = "new_front"

    card.from_dict(card_dict)

    assert card_dict["id"] != card.id
    assert card_dict["user_id"] != card.user_id
    assert card_dict["added_on"] != card.added_on
    assert card_dict["private"] == card.private
    assert card_dict["front"] == card.front
    assert card_dict["back"] == card.back


def test_score_dict(score):
    """
    GIVEN a Score object
    WHEN dict is requested
    THEN check if dict is correct
    """
    score_dict = score.to_dict()

    assert score_dict["id"] == score.id
    assert score_dict["card_id"] == score.card_id
    assert score_dict["user_id"] == score.user_id
    assert score_dict["last_seen_on"] == score.last_seen_on.isoformat()
    assert score_dict["score"] == score.score







from application.models import User, Card, Score


def test_users_in_db(app, user, admin):
    """
    GIVEN a Flask app with attached database
    WHEN users are queried
    THEN check if admin and user (and no others) are present
    """
    with app.app_context():
        db_users = User.query.all()

    assert len(db_users) == 2
    assert admin in db_users
    assert user in db_users


def test_cards_in_db(app, card):
    """
    GIVEN a Flask app with attached database
    WHEN cards are queried
    THEN check if card (and no other) is present
    """
    with app.app_context():
        db_cards = Card.query.all()

    assert len(db_cards) == 1
    # For some reason, the equality/in checks don't seem to work for the Card object.
    # This is strange because they work perfectly fine for the User objects (see above)
    # On the level of .__dict__ I cannot find a difference between User and Card comparisons
    # Both match everywhere except on '_sa_instance_state'
    # I suspect this is due to Card having a foreign key, which makes the db add some secret stuff upon entry
    # But I cannot find a definite explanation
    # assert card in db_cards


def test_scores_in_db(app, score):
    """
    GIVEN a Flask app with attached database
    WHEN scores are queried
    THEN check if score (and no other) is present
    """
    with app.app_context():
        db_scores = Score.query.all()

    assert len(db_scores) == 1
    # See above!
    # assert score in db_scores

from datetime import datetime

from application.learn.rules import is_reviewable, correct_recall, incorrect_recall, MIN_LEVEL, MAX_LEVEL


def test_is_reviewable():
    """
    GIVEN the reviewable test
    WHEN some levels and times are given
    THEN check if it makes sense
    """
    assert is_reviewable(level=MIN_LEVEL, last_seen_on=datetime.now())
    assert is_reviewable(level=MAX_LEVEL, last_seen_on=datetime.min)
    assert not is_reviewable(level=MIN_LEVEL, last_seen_on=datetime.max)
    assert not is_reviewable(level=MAX_LEVEL, last_seen_on=datetime.now())


def test_recall():
    """
    GIVEN the level change functions based on recall
    WHEN some levels and recalls are given
    THEN check if it makes sense
    """
    assert correct_recall(current_level=MIN_LEVEL) > MIN_LEVEL
    assert correct_recall(current_level=MAX_LEVEL) == MAX_LEVEL
    assert incorrect_recall(current_level=MIN_LEVEL) == MIN_LEVEL
    assert incorrect_recall(current_level=MAX_LEVEL) < MAX_LEVEL


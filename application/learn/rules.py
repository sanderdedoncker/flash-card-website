"""
Learning rules based on the "spaced repetition" concept. See
https://en.wikipedia.org/wiki/Spaced_repetition
Learning with feedback (restudying after a failure) also improves performance.
For long-term retention, longer absolute spacing between tests is shown to improve performance, while relative spacing
has no significant effect:
Karpicke, J.D., Roediger, H.L. Is expanding retrieval a superior method for learning text materials?.
Memory & Cognition 38, 116–124 (2010).
Still, to avoid being overloaded with cards, the schedule here is based on the Leitner system. The repetition
period depends on a certain retention level, which is increased or decreased after a successful or
unsuccessful recall.
"""

from datetime import datetime, timedelta

MIN_LEVEL = 0
MAX_LEVEL = 5
LEVEL_TO_PERIOD = {
    0: 0,
    1: 1,
    2: 3,
    3: 7,
    4: 14,
    5: 28
}


def is_reviewable(level, last_seen_on):
    period = LEVEL_TO_PERIOD[level]
    return datetime.now().date() - timedelta(days=period) >= last_seen_on.date()


def correct_recall(current_level):
    if current_level >= MAX_LEVEL:
        return MAX_LEVEL
    else:
        return current_level + 1


def incorrect_recall(current_level):
    if current_level <= MIN_LEVEL:
        return MIN_LEVEL
    else:
        return current_level - 1


from datetime import datetime

from flask import jsonify, request, url_for, abort

from application import db
from application.api import bp
from application.models import Card, Score
from application.api.errors import bad_request, error_response
from application.api.auth import token_auth


# # Helper functions

def response_from_dict(response_dict):
    status_code = response_dict["status_code"]
    if status_code // 100 == 4:
        return error_response(status_code, response_dict["body"])
    response = jsonify(response_dict["body"])
    response.status_code = status_code
    if "location_header" in response_dict:
        response.headers["Location"] = response_dict["location_header"]
    return response


def create_card_helper(user, card_data):
    data = card_data
    if type(data) is not dict:
        return {"status_code": 400, "body": "Data must be a dict."}
    if "front" not in data or "back" not in data:
        return {"status_code": 400, "body": "Must include 'front' and 'back' fields."}
    if type(data["front"]) is not str:
        return {"status_code": 400, "body": "Field 'front' must be string."}
    if type(data["back"]) is not str:
        return {"status_code": 400, "body": "Field 'back' must be string."}
    if "private" in data and type(data["private"]) is not bool:
        return {"status_code": 400, "body": "Field 'private' must be boolean."}
    card = Card(user_id=user.id, added_on=datetime.now())
    card.from_dict(data)
    db.session.add(card)
    db.session.commit()
    return {"status_code": 201, "location_header": url_for("api.get_card", id=card.id), "body": card.to_dict()}


def update_card_helper(user, card_data):
    if type(card_data) is not dict:
        return {"status_code": 400, "body": "Card data must be a dict."}
    if "id" not in card_data or type(card_data["id"]) is not int:
        return {"status_code": 400, "body": "Field 'id' must be integer."}
    card = Card.query.get(card_data["id"])
    if card is None:
        return {"status_code": 404, "body": "Item not found."}
    if card.user.id != user.id:
        return {"status_code": 403, "body": "Unauthorized to edit this item."}
    if "data" not in card_data or type(card_data["data"]) is not dict:
        return {"status_code": 400, "body": "Data must be a dict."}
    data = card_data["data"]
    if "front" in data and type(data["front"]) is not str:
        return {"status_code": 400, "body": "Field 'front' must be string."}
    if "back" in data and type(data["back"]) is not str:
        return {"status_code": 400, "body": "Field 'back' must be string."}
    if "private" in data and type(data["private"]) is not bool:
        return {"status_code": 400, "body": "Field 'private' must be boolean."}
    card.from_dict(data)
    db.session.commit()
    return {"status_code": 200, "body": card.to_dict()}


def delete_card_helper(user, card_data):
    if type(card_data) is not dict:
        return {"status_code": 400, "body": "Card data must be a dict."}
    if "id" not in card_data or type(card_data["id"]) is not int:
        return {"status_code": 400, "body": "Field 'id' must be integer."}
    card = Card.query.get(card_data["id"])
    if card is None:
        return {"status_code": 404, "body": "Item not found."}
    if card.user.id != user.id:
        return {"status_code": 403, "body": "Unauthorized to delete this item."}
    db.session.delete(card)
    db.session.commit()
    return {"status_code": 204, "body": ""}


def batch_helper(user, data_list, function):
    if type(data_list) is not list:
        return bad_request("Batch data must be a list.")
    if len(data_list) > 100:
        return bad_request("Maximum batch items (100) exceeded.")
    response_list = []
    for data in data_list:
        response_list.append(function(user, data))
    response = jsonify(response_list)
    response.status_code = 200
    return response


# # Standard API routes

# Read
@bp.route('/cards/<int:id>', methods=['GET'])
@token_auth.login_required
def get_card(id):
    card = Card.query.get_or_404(id)
    user = token_auth.current_user()
    if card.user.id != user.id:
        return abort(403)
    data_dict = card.to_dict()
    score = Score.query.filter_by(user_id=user.id, card_id=card.id).one_or_none()
    data_dict["score"] = score.to_dict() if score else None
    return jsonify(data_dict)


# Read all
@bp.route('/cards', methods=['GET'])
@token_auth.login_required
def get_cards():
    user = token_auth.current_user()
    cards_scores = user.query_cards_scores()
    query = request.args.get("query")
    if query:
        cards_scores = cards_scores.filter(Card.front.contains(query) | Card.back.contains(query))
    sort = request.args.get("sort")
    order = request.args.get("order")
    if sort == "added" and order == "up":
        cards_scores = cards_scores.order_by(Card.added_on.asc())
    if sort == "added" and order == "down":
        cards_scores = cards_scores.order_by(Card.added_on.desc())
    if sort == "level" and order == "up":
        cards_scores = cards_scores.order_by(Score.score.asc())
    if sort == "level" and order == "down":
        cards_scores = cards_scores.order_by(Score.score.desc())
    if sort == "seen" and order == "up":
        cards_scores = cards_scores.order_by(Score.last_seen_on.asc().nulls_first())
    if sort == "seen" and order == "down":
        cards_scores = cards_scores.order_by(Score.last_seen_on.desc().nulls_last())
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    data_page = cards_scores.paginate(page=page, per_page=per_page, error_out=False)
    data_dict = {
        "items": [{
            **(card.to_dict()),
            "score": (score.to_dict() if score else None)
        } for card, score in data_page.items],
        "_meta": {
            "page": page,
            "per_page": per_page,
            "total_pages": data_page.pages,
            "total_items": data_page.total,
            "prev_page_num": data_page.prev_num if data_page.has_prev else None,
            "next_page_num": data_page.next_num if data_page.has_next else None
        }
    }
    return jsonify(data_dict)


# Create
@bp.route('/cards', methods=['POST'])
@token_auth.login_required
def create_card():
    user = token_auth.current_user()
    data = request.get_json() or {}
    response_dict = create_card_helper(user, data)
    return response_from_dict(response_dict)


# Update
@bp.route('/cards/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_card(id):
    user = token_auth.current_user()
    data = request.get_json() or {}
    response_dict = update_card_helper(user, {"id": id, "data": data})
    return response_from_dict(response_dict)


# Delete
@bp.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    user = token_auth.current_user()
    response_dict = delete_card_helper(user, {"id": id})
    return response_from_dict(response_dict)


# # Batch API routes

@bp.route('/create_cards', methods=['POST'])
@token_auth.login_required
def create_cards():
    user = token_auth.current_user()
    data_list = request.get_json() or []
    return batch_helper(user, data_list, create_card_helper)


@bp.route('/update_cards', methods=['POST'])
@token_auth.login_required
def update_cards():
    user = token_auth.current_user()
    data_list = request.get_json() or []
    return batch_helper(user, data_list, update_card_helper)


@bp.route('/delete_cards', methods=['POST'])
@token_auth.login_required
def delete_cards():
    user = token_auth.current_user()
    data_list = request.get_json() or []
    return batch_helper(user, data_list, delete_card_helper)

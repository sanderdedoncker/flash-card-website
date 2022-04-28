from datetime import datetime

from flask import jsonify, request, url_for, abort

from application import db
from application.api import bp
from application.models import Card, Score
from application.api.errors import bad_request
from application.api.auth import token_auth


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


@bp.route('/cards', methods=['GET'])
@token_auth.login_required
def get_cards():
    user = token_auth.current_user()
    cards_scores = user.query_cards_scores()
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


@bp.route('/cards', methods=['POST'])
@token_auth.login_required
def create_card():
    user = token_auth.current_user()
    data = request.get_json() or {}
    if "front" not in data or "back" not in data:
        return bad_request("Must include 'front' and 'back' fields.")
    if type(data["front"]) is not str:
        return bad_request("Field 'front' must be string.")
    if type(data["back"]) is not str:
        return bad_request("Field 'back' must be string.")
    if "private" in data and type(data["private"]) is not bool:
        return bad_request("Field 'private' must be boolean.")
    card = Card(
        user_id=user.id,
        added_on=datetime.now()
    )
    card.from_dict(data)
    db.session.add(card)
    db.session.commit()
    response = jsonify(card.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_card", id=card.id)
    return response


@bp.route('/cards/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_card(id):
    card = Card.query.get_or_404(id)
    user = token_auth.current_user()
    if card.user.id != user.id:
        return abort(403)
    data = request.get_json() or {}
    if "front" in data and type(data["front"]) is not str:
        return bad_request("Field 'front' must be string.")
    if "back" in data and type(data["back"]) is not str:
        return bad_request("Field 'back' must be string.")
    if "private" in data and type(data["private"]) is not bool:
        return bad_request("Field 'private' must be boolean.")
    card.from_dict(data)
    db.session.commit()
    return jsonify(card.to_dict())


@bp.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return '', 204

# TODO: refactor, moving db manipulations to other module to import in this and card views script
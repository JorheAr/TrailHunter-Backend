from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import follow_user, unfollow_user, get_follow_stats

@jwt_required()
def follow():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    target_user_id = data.get("user_id")
    return follow_user(current_user_id, target_user_id)

@jwt_required()
def unfollow():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    target_user_id = data.get("user_id")
    return unfollow_user(current_user_id, target_user_id)

@jwt_required()
def follow_stats():
    current_user_id = get_jwt_identity()
    return get_follow_stats(current_user_id)

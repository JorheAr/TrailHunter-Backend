from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import follow_user, unfollow_user, get_follow_stats, request_verification_email, \
    get_usuario_actual, verify_email_token, get_all_users, get_usuario_by_id, get_seguidores, get_seguidos


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

@jwt_required()
def follow_stats_by_id(user_id):
    return get_follow_stats(user_id)

@jwt_required()
def obtener_usuario_actual():
    user_id = get_jwt_identity()
    return get_usuario_actual(user_id)


@jwt_required()
def send_verification_request():
    user_id = get_jwt_identity()
    return request_verification_email(user_id)

def verify_email():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return {"message": "Token no proporcionado"}, 400

    return verify_email_token(token)

@jwt_required()
def obtener_usuarios():
    current_user_id = get_jwt_identity()
    return get_all_users(current_user_id)

@jwt_required()
def obtener_usuario_por_id(user_id):
    current_user_id = get_jwt_identity()
    return get_usuario_by_id(user_id, current_user_id)

@jwt_required()
def obtener_seguidores():
    current_user_id = get_jwt_identity()
    return get_seguidores(current_user_id)

@jwt_required()
def obtener_seguidos():
    current_user_id = get_jwt_identity()
    return get_seguidos(current_user_id)

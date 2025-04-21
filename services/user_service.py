from models import db, Usuario

def follow_user(current_user_id, target_user_id):
    current_user = Usuario.query.get(current_user_id)
    target_user = Usuario.query.get(target_user_id)

    if not current_user or not target_user:
        return {"message": "Usuario no encontrado"}, 404

    if current_user.id == target_user.id:
        return {"message": "No puedes seguirte a ti mismo"}, 400

    if current_user.is_following(target_user):
        return {"message": "Ya estás siguiendo a este usuario"}, 400

    current_user.follow(target_user)
    db.session.commit()
    return {"message": f"Ahora sigues a {target_user.username}"}, 200

def unfollow_user(current_user_id, target_user_id):
    current_user = Usuario.query.get(current_user_id)
    target_user = Usuario.query.get(target_user_id)

    if not current_user or not target_user:
        return {"message": "Usuario no encontrado"}, 404

    if not current_user.is_following(target_user):
        return {"message": "No estás siguiendo a este usuario"}, 400

    current_user.unfollow(target_user)
    db.session.commit()
    return {"message": f"Has dejado de seguir a {target_user.username}"}, 200

def get_follow_stats(current_user_id):
    user = Usuario.query.get(current_user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    followers_count = user.followers.count()
    following_count = user.followed.count()

    return {
        "seguidores": followers_count,
        "seguidos": following_count
    }, 200
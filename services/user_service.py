from models import db, Usuario, Cliente
from utils.token_utils import generate_verification_token, confirm_verification_token
from services.email_service import send_verification_email

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

def request_verification_email(user_id):
    user = Usuario.query.get(user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    if getattr(user, "verificado", False):
        return {"message": "La cuenta ya está verificada"}, 400

    token = generate_verification_token(user.email)
    send_verification_email(user.email, token)

    return {"message": "Correo de verificación enviado"}, 200

def verify_email_token(token):
    email = confirm_verification_token(token)
    if not email:
        return {"message": "Token inválido o expirado"}, 400

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return {"message": "Usuario no encontrado"}, 404

    if user.verificado:
        return {"message": "La cuenta ya estaba verificada"}, 200

    user.verificado = True
    db.session.commit()
    return {"message": "Cuenta verificada correctamente"}, 200

def get_usuario_actual(user_id):
    user = Usuario.query.get(user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    # Serializar datos básicos
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "verificado": user.verificado,
        "rol": user.rol,
        "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None,
    }

    # Añadir info de cliente si existe
    if user.cliente:
        user_data["cliente"] = {
            "nombre": user.cliente.nombre,
            "apellidos": user.cliente.apellidos,
            "fecha_nacimiento": user.cliente.fecha_nacimiento.isoformat()
        }
    else:
        user_data["cliente"] = None

    return user_data, 200

def get_all_users(current_user_id=None):
    users = Usuario.query.all()

    if not users:
        return {"message": "No se encontraron usuarios"}, 404

    current_user = Usuario.query.get(current_user_id) if current_user_id else None
    users_data = []

    for user in users:
        if current_user and user.id == current_user.id:
            continue

        is_following = current_user.is_following(user) if current_user else False

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "verificado": user.verificado,
            "rol": user.rol,
            "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None,
            "is_following": is_following
        }

        if user.cliente:
            user_data["cliente"] = {
                "nombre": user.cliente.nombre,
                "apellidos": user.cliente.apellidos,
                "fecha_nacimiento": user.cliente.fecha_nacimiento.isoformat()
            }
        else:
            user_data["cliente"] = None

        users_data.append(user_data)

    return {"usuarios": users_data}, 200

def get_usuario_by_id(user_id, current_user_id=None):
    user = Usuario.query.get(user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    is_following = False
    if current_user_id and current_user_id != user.id:
        current_user = Usuario.query.get(current_user_id)
        if current_user:
            is_following = current_user.is_following(user)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "verificado": user.verificado,
        "rol": user.rol,
        "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None,
        "is_following": is_following
    }

    if user.cliente:
        user_data["cliente"] = {
            "nombre": user.cliente.nombre,
            "apellidos": user.cliente.apellidos,
            "fecha_nacimiento": user.cliente.fecha_nacimiento.isoformat()
        }
    else:
        user_data["cliente"] = None

    return user_data, 200

def get_seguidores(current_user_id):
    user = Usuario.query.get(current_user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    # Obtener los seguidores del usuario
    seguidores = user.followers.all()

    # Serializar la información de los seguidores
    seguidores_data = []
    for follower in seguidores:
        seguidores_data.append({
            "id": follower.id,
            "username": follower.username,
            "email": follower.email,
            "verificado": follower.verificado,
            "rol": follower.rol,
            "fecha_registro": follower.fecha_registro.isoformat() if follower.fecha_registro else None,
            "cliente": {
                "nombre": follower.cliente.nombre if follower.cliente else None,
                "apellidos": follower.cliente.apellidos if follower.cliente else None,
                "fecha_nacimiento": follower.cliente.fecha_nacimiento.isoformat() if follower.cliente else None
            }
        })

    return {"seguidores": seguidores_data}, 200

def get_seguidos(current_user_id):
    user = Usuario.query.get(current_user_id)

    if not user:
        return {"message": "Usuario no encontrado"}, 404

    # Obtener los seguidos por el usuario
    seguidos = user.followed.all()

    # Serializar la información de los seguidos
    seguidos_data = []
    for followed in seguidos:
        seguidos_data.append({
            "id": followed.id,
            "username": followed.username,
            "email": followed.email,
            "verificado": followed.verificado,
            "rol": followed.rol,
            "fecha_registro": followed.fecha_registro.isoformat() if followed.fecha_registro else None,
            "cliente": {
                "nombre": followed.cliente.nombre if followed.cliente else None,
                "apellidos": followed.cliente.apellidos if followed.cliente else None,
                "fecha_nacimiento": followed.cliente.fecha_nacimiento.isoformat() if followed.cliente else None
            }
        })

    return {"seguidos": seguidos_data}, 200

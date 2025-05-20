from flask import request, jsonify
from services.contacto_service import guardar_mensaje_contacto, marcar_mensaje_como_leido
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.contacto_service import obtener_mensajes_contacto
from models import Usuario, MensajeContacto


def enviar_mensaje_contacto():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    mensaje = data.get('mensaje')

    if not nombre or not correo or not mensaje:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    guardar_mensaje_contacto(nombre, correo, mensaje)
    return jsonify({"mensaje": "Mensaje enviado con éxito"}), 201

@jwt_required()
def listar_mensajes_contacto():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario or usuario.rol != 'admin':
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403

    leido_param = request.args.get('leido')
    query = MensajeContacto.query

    if leido_param is not None:
        if leido_param.lower() == 'true':
            query = query.filter_by(leido=True)
        elif leido_param.lower() == 'false':
            query = query.filter_by(leido=False)

    mensajes = query.all()

    resultado = [{
        "id": m.id,
        "nombre": m.nombre,
        "correo": m.correo,
        "mensaje": m.mensaje,
        "fecha_envio": m.fecha_envio.isoformat(),
        "leido": m.leido
    } for m in mensajes]

    return jsonify(resultado), 200

@jwt_required()
def marcar_leido():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario or usuario.rol != 'admin':
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403

    data = request.get_json()
    mensaje_id = data.get('mensaje_id')

    mensaje = marcar_mensaje_como_leido(mensaje_id)
    if not mensaje:
        return jsonify({"error": "Mensaje no encontrado"}), 404

    return jsonify({"mensaje": "Mensaje marcado como leído"}), 200
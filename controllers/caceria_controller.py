from flask import request, jsonify
from models import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.caceria_service import inscribirse_actividad, valorar_actividad, \
    obtener_todas_actividades, obtener_actividades_de_usuario, eliminar_inscripcion, crear_actividad_db, \
    obtener_comentarios_actividad, agregar_comentario


@jwt_required()
def inscribirse():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    try:
        inscripcion = inscribirse_actividad(usuario_id, data["actividad_id"])
        return jsonify({"message": "Inscripción exitosa"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@jwt_required()
def quitar_inscripcion():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    try:
        eliminar_inscripcion(usuario_id, data["actividad_id"])
        return jsonify({"message": "Inscripción eliminada"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@jwt_required()
def valorar():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    try:
        valoracion = valorar_actividad(
            usuario_id,
            data["actividad_id"],
            data["puntuacion"],
            data.get("comentario", "")
        )
        return jsonify({"message": "Valoración registrada"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@jwt_required()
def crear_actividad():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if usuario.rol != "admin":
        return jsonify({"error": "No autorizado"}), 403

    try:
        actividad = crear_actividad_db(
            data["titulo"],
            data["descripcion"],
            data["fecha"],
            data["lugar"],
            data["cupo_maximo"],
            usuario_id,
            data.get("imagen_url")
        )
        return jsonify({"message": "Actividad creada", "id": actividad.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@jwt_required(optional=True)
def listar_actividades():
    actividades = obtener_todas_actividades()
    resultado = [
        {
            "id": a.id,
            "titulo": a.titulo,
            "descripcion": a.descripcion,
            "fecha": a.fecha.isoformat(),
            "cupo_maximo": a.cupo_maximo,
            "lugar": a.lugar,
            "inscritos": len(a.inscripciones),
            "imagen_url": a.imagen_url
        }
        for a in actividades
    ]
    return jsonify(resultado), 200

@jwt_required()
def listar_actividades_usuario():
    usuario_id = get_jwt_identity()
    actividades = obtener_actividades_de_usuario(usuario_id)

    resultado = [
        {
            "id": a.id,
            "titulo": a.titulo,
            "descripcion": a.descripcion,
            "fecha": a.fecha.isoformat(),
            "valoracion": next(
                (v.puntuacion for v in a.valoraciones if v.usuario_id == usuario_id), None
            ),
            "imagen_url": a.imagen_url
        }
        for a in actividades
    ]
    return jsonify(resultado), 200

def crear_comentario(actividad_id, data, usuario_actual):
    texto = data.get('texto')
    if not texto:
        return {'error': 'Texto requerido'}, 400

    comentario = agregar_comentario(actividad_id, usuario_actual.id, texto)
    return {
        'id': comentario.id,
        'texto': comentario.texto,
        'fecha_creacion': comentario.fecha_creacion.isoformat(),
        'autor': usuario_actual.username
    }, 201


def listar_comentarios(actividad_id):
    comentarios = obtener_comentarios_actividad(actividad_id)
    return [{
        'id': c.id,
        'texto': c.texto,
        'fecha_creacion': c.fecha_creacion.isoformat(),
        'autor': c.usuario.username
    } for c in comentarios]

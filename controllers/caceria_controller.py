from flask import request, jsonify
from models import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.caceria_service import inscribirse_actividad, valorar_actividad, \
    obtener_todas_actividades, obtener_actividades_de_usuario, eliminar_inscripcion, crear_actividad_db


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

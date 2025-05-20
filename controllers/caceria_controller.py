from flask import request, jsonify
from models import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.caceria_service import inscribirse_actividad, quitar_inscripcion, valorar_actividad, \
    obtener_todas_actividades, obtener_actividades_de_usuario


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
        quitar_inscripcion(usuario_id, data["actividad_id"])
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
        actividad = crear_actividad(
            data["nombre"],
            data["descripcion"],
            data["fecha"],
            data["limite_participantes"]
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
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "fecha": a.fecha.isoformat(),
            "limite_participantes": a.limite_participantes,
            "inscritos": len(a.inscripciones)
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
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "fecha": a.fecha.isoformat(),
            "valoracion": next((i.valoracion for i in a.inscripciones if i.usuario_id == usuario_id), None)
        }
        for a in actividades
    ]
    return jsonify(resultado), 200
from flask import Blueprint
from controllers.caceria_controller import (
    inscribirse, quitar_inscripcion, valorar, crear_actividad,
    listar_actividades, listar_actividades_usuario,
    crear_comentario, listar_comentarios
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Usuario
from flask import request, jsonify

caceria_bp = Blueprint('caceria', __name__)

caceria_bp.post("/inscribirse")(inscribirse)
caceria_bp.post("/desinscribirse")(quitar_inscripcion)
caceria_bp.post("/valorar")(valorar)
caceria_bp.post("/crear")(crear_actividad)
caceria_bp.get("/todas")(listar_actividades)
caceria_bp.get("/mis")(listar_actividades_usuario)

# Comentarios
@caceria_bp.post("/actividades/<int:actividad_id>/comentarios")
@jwt_required()
def route_crear_comentario(actividad_id):
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(usuario_id)
    return crear_comentario(actividad_id, request.json, usuario)

@caceria_bp.get("/actividades/<int:actividad_id>/comentarios")
def route_listar_comentarios(actividad_id):
    return jsonify(listar_comentarios(actividad_id))

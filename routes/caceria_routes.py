from flask import Blueprint
from controllers.caceria_controller import (inscribirse,quitar_inscripcion,valorar, crear_actividad,
                                            listar_actividades, listar_actividades_usuario)

caceria_bp = Blueprint('caceria', __name__)

caceria_bp.post("/inscribirse")(inscribirse)
caceria_bp.post("/desinscribirse")(quitar_inscripcion)
caceria_bp.post("/valorar")(valorar)
caceria_bp.post("/crear")(crear_actividad)
caceria_bp.get("/todas")(listar_actividades)
caceria_bp.get("/mis")(listar_actividades_usuario)


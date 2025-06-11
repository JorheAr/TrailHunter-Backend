from flask import jsonify
from services.stats_service import (
    usuarios_registrados_ultima_semana,
    inscripciones_ultima_semana,
    total_usuarios,
    total_actividades
)

def obtener_estadisticas_dashboard():
    return jsonify({
        "usuarios_ultima_semana": usuarios_registrados_ultima_semana(),
        "inscripciones_ultima_semana": inscripciones_ultima_semana(),
        "total_usuarios": total_usuarios(),
        "total_actividades": total_actividades()
    })

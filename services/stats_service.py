from models import db, Usuario, ActividadCaceria, InscripcionActividad
from datetime import datetime, timedelta

def usuarios_registrados_ultima_semana():
    desde = datetime.utcnow() - timedelta(days=7)
    return Usuario.query.filter(Usuario.fecha_registro >= desde).count()

def inscripciones_ultima_semana():
    desde = datetime.utcnow() - timedelta(days=7)
    return InscripcionActividad.query.filter(InscripcionActividad.actividad.has(ActividadCaceria.fecha >= desde)).count()

def total_usuarios():
    return Usuario.query.count()

def total_actividades():
    return ActividadCaceria.query.count()

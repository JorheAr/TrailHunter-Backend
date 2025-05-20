from models import db, ActividadCaceria, InscripcionActividad, ValoracionActividad
from datetime import datetime


def inscribirse_actividad(usuario_id, actividad_id):
    actividad = ActividadCaceria.query.get(actividad_id)
    if not actividad:
        raise ValueError("Actividad no encontrada")

    if datetime.utcnow() > actividad.fecha:
        raise ValueError("La actividad ya ha ocurrido")

    if len(actividad.participantes) >= actividad.limite_participantes:
        raise ValueError("La actividad ya está llena")

    ya_inscrito = InscripcionActividad.query.filter_by(usuario_id=usuario_id, actividad_id=actividad_id).first()
    if ya_inscrito:
        raise ValueError("Ya estás inscrito")

    inscripcion = InscripcionActividad(usuario_id=usuario_id, actividad_id=actividad_id)
    db.session.add(inscripcion)
    db.session.commit()
    return inscripcion


def quitar_inscripcion(usuario_id, actividad_id):
    inscripcion = InscripcionActividad.query.filter_by(usuario_id=usuario_id, actividad_id=actividad_id).first()
    if not inscripcion:
        raise ValueError("No estás inscrito")

    db.session.delete(inscripcion)
    db.session.commit()


def valorar_actividad(usuario_id, actividad_id, puntuacion, comentario):
    actividad = ActividadCaceria.query.get(actividad_id)
    if not actividad or datetime.utcnow() < actividad.fecha:
        raise ValueError("No puedes valorar esta actividad todavía")

    inscripcion = InscripcionActividad.query.filter_by(usuario_id=usuario_id, actividad_id=actividad_id).first()
    if not inscripcion:
        raise ValueError("No participaste en esta actividad")

    ya_valorada = ValoracionActividad.query.filter_by(usuario_id=usuario_id, actividad_id=actividad_id).first()
    if ya_valorada:
        raise ValueError("Ya valoraste esta actividad")

    valoracion = ValoracionActividad(usuario_id=usuario_id, actividad_id=actividad_id,
                                   puntuacion=puntuacion, comentario=comentario)
    db.session.add(valoracion)
    db.session.commit()
    return valoracion

def crear_actividad(nombre, descripcion, fecha, limite_participantes):
    nueva_actividad = ActividadCaceria(
        nombre=nombre,
        descripcion=descripcion,
        fecha=fecha,
        limite_participantes=limite_participantes
    )
    db.session.add(nueva_actividad)
    db.session.commit()
    return nueva_actividad

def obtener_todas_actividades():
    return ActividadCaceria.query.all()

def obtener_actividades_de_usuario(usuario_id):
    return ActividadCaceria.query.join(InscripcionActividad).filter(InscripcionActividad.usuario_id == usuario_id).all()


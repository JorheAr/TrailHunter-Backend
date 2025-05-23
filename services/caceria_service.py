from models import db, ActividadCaceria, InscripcionActividad, ValoracionActividad
from datetime import datetime


def inscribirse_actividad(usuario_id, actividad_id):
    actividad = ActividadCaceria.query.get(actividad_id)
    if actividad is None:
        raise Exception("Actividad no encontrada")

    # Aquí está la clave: cambiar participantes por inscripciones
    if len(actividad.inscripciones) >= actividad.cupo_maximo:
        raise Exception("Límite de participantes alcanzado")

    ya_inscrito = InscripcionActividad.query.filter_by(usuario_id=usuario_id, actividad_id=actividad_id).first()
    if ya_inscrito:
        raise Exception("Usuario ya inscrito en esta actividad")

    nueva_inscripcion = InscripcionActividad(usuario_id=usuario_id, actividad_id=actividad_id)
    db.session.add(nueva_inscripcion)
    db.session.commit()

    return nueva_inscripcion

def eliminar_inscripcion(usuario_id, actividad_id):
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

def crear_actividad_db(titulo, descripcion, fecha, cupo_maximo, creador_id, imagen_url=None):
    nueva_actividad = ActividadCaceria(
        titulo=titulo,
        descripcion=descripcion,
        fecha=fecha,
        cupo_maximo=cupo_maximo,
        imagen_url=imagen_url,
        creador_id=creador_id
    )
    db.session.add(nueva_actividad)
    db.session.commit()
    return nueva_actividad


def obtener_todas_actividades():
    return ActividadCaceria.query.all()

def obtener_actividades_de_usuario(usuario_id):
    return ActividadCaceria.query.join(InscripcionActividad).filter(InscripcionActividad.usuario_id == usuario_id).all()


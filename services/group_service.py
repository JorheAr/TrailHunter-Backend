from models import db, Grupo, MiembroGrupo, PublicacionGrupo, LikePublicacionGrupo, Usuario, ComentarioPublicacionGrupo
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def crear_grupo(nombre, descripcion, creador_id):
    grupo = Grupo(nombre=nombre, descripcion=descripcion)
    db.session.add(grupo)
    db.session.flush()  # Para obtener id

    miembro_admin = MiembroGrupo(usuario_id=creador_id, grupo_id=grupo.id, rol='admin')
    db.session.add(miembro_admin)

    db.session.commit()
    return grupo

def borrar_grupo(grupo_id, usuario_id):
    grupo = Grupo.query.get(grupo_id)
    if not grupo:
        raise Exception("Grupo no encontrado")

    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    if not miembro or miembro.rol != 'admin':
        raise Exception("No tienes permiso para borrar este grupo")

    db.session.delete(grupo)
    db.session.commit()

def unir_a_grupo(grupo_id, usuario_id):
    grupo = Grupo.query.get(grupo_id)
    if not grupo:
        raise Exception("Grupo no encontrado")

    miembro_existente = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    if miembro_existente:
        return miembro_existente  # Ya es miembro

    miembro = MiembroGrupo(grupo_id=grupo_id, usuario_id=usuario_id, rol='miembro')
    db.session.add(miembro)
    db.session.commit()
    return miembro

def salir_de_grupo(grupo_id, usuario_id):
    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    if not miembro:
        raise Exception("No eres miembro de este grupo")

    db.session.delete(miembro)
    db.session.commit()

def es_miembro_de_grupo(grupo_id, usuario_id):
    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    return miembro is not None


def expulsar_miembro(grupo_id, usuario_admin_id, usuario_a_expulsar_id):
    miembro_admin = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_admin_id).first()
    if not miembro_admin or miembro_admin.rol != 'admin':
        raise Exception("No tienes permiso para expulsar miembros")

    miembro_expulsar = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_a_expulsar_id).first()
    if not miembro_expulsar:
        raise Exception("Usuario a expulsar no es miembro del grupo")

    db.session.delete(miembro_expulsar)
    db.session.commit()

def crear_publicacion(grupo_id, autor_id, titulo, contenido, imagen_url=None):
    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=autor_id).first()
    if not miembro:
        raise Exception("No eres miembro de este grupo")

    publicacion = PublicacionGrupo(
        grupo_id=grupo_id,
        autor_id=autor_id,
        titulo=titulo,
        contenido=contenido,
        imagen=imagen_url
    )
    db.session.add(publicacion)
    db.session.commit()
    return publicacion

def borrar_publicacion(publicacion_id, usuario_id):
    publicacion = PublicacionGrupo.query.get(publicacion_id)
    if not publicacion:
        raise Exception("Publicación no encontrada")

    if publicacion.autor_id != usuario_id:
        miembro = MiembroGrupo.query.filter_by(grupo_id=publicacion.grupo_id, usuario_id=usuario_id).first()
        if not miembro or miembro.rol != 'admin':
            raise Exception("No tienes permiso para borrar esta publicación")

    db.session.delete(publicacion)
    db.session.commit()

def dar_like_publicacion(publicacion_id, usuario_id):
    publicacion = PublicacionGrupo.query.get(publicacion_id)
    if not publicacion:
        raise Exception("Publicación no encontrada")

    miembro = MiembroGrupo.query.filter_by(grupo_id=publicacion.grupo_id, usuario_id=usuario_id).first()
    if not miembro:
        raise Exception("No eres miembro del grupo")

    like_existente = LikePublicacionGrupo.query.filter_by(publicacion_id=publicacion_id, usuario_id=usuario_id).first()
    if like_existente:
        db.session.delete(like_existente)
        db.session.commit()
        return False  # Like quitado
    else:
        like = LikePublicacionGrupo(publicacion_id=publicacion_id, usuario_id=usuario_id)
        db.session.add(like)
        db.session.commit()
        return True  # Like añadido

def obtener_grupo(grupo_id):
    grupo = Grupo.query.get(grupo_id)
    if not grupo:
        raise Exception("Grupo no encontrado")
    return grupo

def crear_comentario_publicacion_grupo(autor_id: int, publicacion_id: int, texto: str) -> ComentarioPublicacionGrupo:
    comentario = ComentarioPublicacionGrupo(
        autor_id=autor_id,
        publicacion_id=publicacion_id,
        texto=texto,
        fecha_creacion=datetime.utcnow()
    )
    db.session.add(comentario)
    db.session.commit()

    # Forzar la carga de la relación autor
    comentario.autor = Usuario.query.get(autor_id)

    return comentario


def obtener_comentarios_publicacion_grupo(publicacion_id: int):
    return ComentarioPublicacionGrupo.query.filter_by(publicacion_id=publicacion_id).order_by(ComentarioPublicacionGrupo.fecha_creacion.asc()).all()

def listar_grupos():
    return Grupo.query.all()

def listar_publicaciones(grupo_id):
    return PublicacionGrupo.query.filter_by(grupo_id=grupo_id).order_by(PublicacionGrupo.fecha_creacion.desc()).all()

def listar_miembros(grupo_id):
    return MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()

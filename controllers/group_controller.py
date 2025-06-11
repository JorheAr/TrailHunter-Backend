from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import LikePublicacionGrupo, PublicacionGrupo
from services.group_service import (
    crear_grupo, borrar_grupo, unir_a_grupo, salir_de_grupo, expulsar_miembro,
    crear_publicacion, borrar_publicacion, dar_like_publicacion,
    obtener_grupo, listar_publicaciones, listar_miembros, listar_grupos, es_miembro_de_grupo,
    crear_comentario_publicacion_grupo, obtener_comentarios_publicacion_grupo
)


@jwt_required()
def crear():
    user_id = get_jwt_identity()
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    if not nombre:
        return jsonify({"message": "El nombre es obligatorio"}), 400
    try:
        grupo = crear_grupo(nombre, descripcion, user_id)
        return jsonify({"id": grupo.id, "nombre": grupo.nombre, "descripcion": grupo.descripcion}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@jwt_required()
def borrar(grupo_id):
    user_id = get_jwt_identity()
    try:
        borrar_grupo(grupo_id, user_id)
        return jsonify({"message": "Grupo borrado correctamente"})
    except Exception as e:
        return jsonify({"message": str(e)}), 403


@jwt_required()
def unirse(grupo_id):
    user_id = get_jwt_identity()
    try:
        miembro = unir_a_grupo(grupo_id, user_id)
        return jsonify({"grupo_id": miembro.grupo_id, "usuario_id": miembro.usuario_id, "rol": miembro.rol})
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@jwt_required()
def salir(grupo_id):
    user_id = get_jwt_identity()
    try:
        salir_de_grupo(grupo_id, user_id)
        return jsonify({"message": "Has salido del grupo"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@jwt_required()
def comprobar_membresia(grupo_id):
    user_id = get_jwt_identity()
    es_miembro = es_miembro_de_grupo(grupo_id, user_id)
    return jsonify({"es_miembro": es_miembro})

@jwt_required()
def expulsar(grupo_id):
    user_admin_id = get_jwt_identity()
    data = request.get_json()
    usuario_a_expulsar_id = data.get("usuario_id")
    if not usuario_a_expulsar_id:
        return jsonify({"message": "Debe proporcionar usuario_id para expulsar"}), 400
    try:
        expulsar_miembro(grupo_id, user_admin_id, usuario_a_expulsar_id)
        return jsonify({"message": "Usuario expulsado correctamente"})
    except Exception as e:
        return jsonify({"message": str(e)}), 403


@jwt_required()
def crear_post(grupo_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    titulo = data.get("titulo")
    contenido = data.get("contenido")
    imagen_url = data.get("imagen_url")
    if not contenido:
        return jsonify({"message": "El contenido es obligatorio"}), 400
    try:
        post = crear_publicacion(grupo_id, user_id, titulo, contenido, imagen_url)
        return jsonify({
            "id": post.id,
            "titulo": post.titulo,
            "contenido": post.contenido,
            "imagen": post.imagen,
            "autor_id": post.autor_id,
            "autor_nombre": post.autor.username,
            "fecha_creacion": post.fecha_creacion.isoformat()
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@jwt_required()
def borrar_post(publicacion_id):
    user_id = get_jwt_identity()
    try:
        borrar_publicacion(publicacion_id, user_id)
        return jsonify({"message": "Publicación borrada correctamente"})
    except Exception as e:
        return jsonify({"message": str(e)}), 403


@jwt_required()
def like_post(publicacion_id):
    user_id = get_jwt_identity()
    try:
        liked = dar_like_publicacion(publicacion_id, user_id)
        return jsonify({"liked": liked})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@jwt_required()
def obtener_grupos():
    try:
        grupos = listar_grupos()
        result = []
        for g in grupos:
            result.append({
                "id": g.id,
                "nombre": g.nombre,
                "descripcion": g.descripcion,
                "fecha_creacion": g.fecha_creacion.isoformat(),
                "imagen_url": g.imagen_url
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@jwt_required()
def detalle_grupo(grupo_id):
    try:
        grupo = obtener_grupo(grupo_id)
        return jsonify({
            "id": grupo.id,
            "nombre": grupo.nombre,
            "descripcion": grupo.descripcion,
            "fecha_creacion": grupo.fecha_creacion.isoformat()
        })
    except Exception as e:
        return jsonify({"message": str(e)}), 404


@jwt_required()
def publicaciones(grupo_id):
    try:
        user_id = get_jwt_identity()
        publicaciones = listar_publicaciones(grupo_id)
        result = []
        for pub in publicaciones:
            ya_votado = LikePublicacionGrupo.query.filter_by(
                publicacion_id=pub.id, usuario_id=user_id
            ).first() is not None

            cantidad_likes = LikePublicacionGrupo.query.filter_by(
                publicacion_id=pub.id
            ).count()

            result.append({
                "id": pub.id,
                "titulo": pub.titulo,
                "contenido": pub.contenido,
                "imagen": pub.imagen,
                "autor_id": pub.autor_id,
                "autor_nombre": pub.autor.username,
                "fecha_creacion": pub.fecha_creacion.isoformat(),
                "ya_votado": ya_votado,
                "cantidad_likes": cantidad_likes
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": str(e)}), 404


@jwt_required()
def miembros(grupo_id):
    try:
        miembros = listar_miembros(grupo_id)
        result = []
        for m in miembros:
            result.append({
                "usuario_id": m.usuario_id,
                "rol": m.rol
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@jwt_required()
def api_crear_comentario_publicacion_grupo(publicacion_id):
    data = request.get_json()
    texto = data.get('texto')
    if not texto or texto.strip() == '':
        return jsonify({'error': 'El texto del comentario es obligatorio'}), 400

    usuario_id = get_jwt_identity()
    # Opcional: Validar que la publicación existe
    publicacion = PublicacionGrupo.query.get(publicacion_id)
    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404

    comentario = crear_comentario_publicacion_grupo(usuario_id, publicacion_id, texto)
    return jsonify({
        'id': comentario.id,
        'texto': comentario.texto,
        'fecha_creacion': comentario.fecha_creacion.isoformat(),
        'autor': {
            'id': comentario.autor.id,
            'nombre': comentario.autor.username
        }
    }), 201

@jwt_required(optional=True)
def api_obtener_comentarios_publicacion_grupo(publicacion_id):
    comentarios = obtener_comentarios_publicacion_grupo(publicacion_id)
    lista = []
    for c in comentarios:
        lista.append({
            'id': c.id,
            'texto': c.texto,
            'fecha_creacion': c.fecha_creacion.isoformat(),
            'autor': {
                'id': c.autor.id,
                'nombre': c.autor.username
            }
        })
    return jsonify(lista)
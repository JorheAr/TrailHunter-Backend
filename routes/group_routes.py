from flask import Blueprint
from controllers.group_controller import (
    crear, borrar, unirse, salir, expulsar,
    crear_post, borrar_post, like_post,
    detalle_grupo, publicaciones, miembros, obtener_grupos, comprobar_membresia, api_crear_comentario_publicacion_grupo,
    api_obtener_comentarios_publicacion_grupo
)

group_bp = Blueprint('group', __name__)

group_bp.route('/crear', methods=['POST'])(crear)
group_bp.route('/todos', methods=['GET'])(obtener_grupos)
group_bp.route('/<int:grupo_id>', methods=['DELETE'])(borrar)
group_bp.route('/<int:grupo_id>/unirse', methods=['POST'])(unirse)
group_bp.route('/<int:grupo_id>/salir', methods=['POST'])(salir)
group_bp.route("/<int:grupo_id>/es_miembro", methods=["GET"])(comprobar_membresia)
group_bp.route('/<int:grupo_id>/expulsar', methods=['POST'])(expulsar)

group_bp.route('/<int:grupo_id>/publicacion', methods=['POST'])(crear_post)
group_bp.route('/publicaciones/<int:publicacion_id>', methods=['DELETE'])(borrar_post)
group_bp.route('/publicaciones/<int:publicacion_id>/like', methods=['POST'])(like_post)

group_bp.route('/<int:grupo_id>', methods=['GET'])(detalle_grupo)
group_bp.route('/<int:grupo_id>/publicaciones', methods=['GET'])(publicaciones)
group_bp.route('/publicaciones/<int:publicacion_id>/comentarios', methods=['POST'])(api_crear_comentario_publicacion_grupo)
group_bp.route('/publicaciones/<int:publicacion_id>/comentarios', methods=['GET'])(api_obtener_comentarios_publicacion_grupo)
group_bp.route('/<int:grupo_id>/miembros', methods=['GET'])(miembros)

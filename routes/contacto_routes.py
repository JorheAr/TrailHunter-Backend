from flask import Blueprint
from controllers.contacto_controller import enviar_mensaje_contacto, listar_mensajes_contacto, marcar_leido

contacto_bp = Blueprint('contacto', __name__)

contacto_bp.route('', methods=['POST'])(enviar_mensaje_contacto)  # antes '/contacto'
contacto_bp.route('/mensajes', methods=['GET'])(listar_mensajes_contacto)
contacto_bp.route('/mensajes/marcar-leido', methods=['POST'])(marcar_leido)

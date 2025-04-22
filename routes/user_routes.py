from flask import Blueprint
from controllers.user_controller import follow, unfollow, follow_stats, send_verification_request, \
    obtener_usuario_actual, verify_email

user_bp = Blueprint("user", __name__)

user_bp.route("/follow", methods=["POST"])(follow)
user_bp.route("/unfollow", methods=["POST"])(unfollow)
user_bp.route("/follow-stats", methods=["GET"])(follow_stats)
user_bp.route("/send-verification-email", methods=["POST"])(send_verification_request)
user_bp.route("/me", methods=["GET"])(obtener_usuario_actual)
user_bp.route("/verify-email", methods=["POST"])(verify_email)


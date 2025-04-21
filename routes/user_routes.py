from flask import Blueprint
from controllers.user_controller import follow, unfollow, follow_stats

user_bp = Blueprint("user", __name__)

user_bp.route("/follow", methods=["POST"])(follow)
user_bp.route("/unfollow", methods=["POST"])(unfollow)
user_bp.route("/follow-stats", methods=["GET"])(follow_stats)

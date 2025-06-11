from flask import Blueprint
from controllers.stats_controller import obtener_estadisticas_dashboard

stats_bp = Blueprint("stats", __name__)
stats_bp.route("/dashboard", methods=["GET"])(obtener_estadisticas_dashboard)

from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.caceria_routes import caceria_bp
from routes.contacto_routes import contacto_bp
from config import Config
from models import db
from routes.auth_routes import auth_bp
from flask_cors import CORS

from routes.group_routes import group_bp
from routes.stats_routes import stats_bp
from routes.user_routes import user_bp


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# Registrar rutas
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/usuarios")
app.register_blueprint(caceria_bp, url_prefix="/caceria")
app.register_blueprint(contacto_bp, url_prefix="/contacto")
app.register_blueprint(stats_bp, url_prefix="/stats")
app.register_blueprint(group_bp, url_prefix="/group")


if __name__ == "__main__":
    app.run(debug=True)

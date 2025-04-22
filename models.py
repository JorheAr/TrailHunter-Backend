from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Tabla intermedia para la relación de "seguidores"
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('usuarios.id'))
)

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    verificado = db.Column(db.Boolean, default=False)

    rol = db.Column(db.String(20), nullable=False, default='usuario')

    # Relación uno a uno con Cliente
    cliente = db.relationship("Cliente", backref="usuario", uselist=False)

    # Relación muchos-a-muchos: usuarios que este usuario sigue
    followed = db.relationship(
        'Usuario', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    # Métodos de autenticación
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Métodos para seguir/seguir
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def is_followed_by(self, user):
        return self.followers.filter(followers.c.follower_id == user.id).count() > 0


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)

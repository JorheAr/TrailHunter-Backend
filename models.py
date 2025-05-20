from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('usuarios.id'))
)

bloqueos = db.Table(
    'bloqueos',
    db.Column('bloqueador_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('bloqueado_id', db.Integer, db.ForeignKey('usuarios.id'))
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

    cliente = db.relationship("Cliente", backref="usuario", uselist=False)

    followed = db.relationship(
        'Usuario', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    bloqueados = db.relationship(
        'Usuario', secondary=bloqueos,
        primaryjoin=(bloqueos.c.bloqueador_id == id),
        secondaryjoin=(bloqueos.c.bloqueado_id == id),
        backref=db.backref('bloqueadores', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    def block(self, user):
        if not self.has_blocked(user):
            self.unfollow(user)
            user.unfollow(self)
            self.bloqueados.append(user)

    def unblock(self, user):
        if self.has_blocked(user):
            self.bloqueados.remove(user)

    def has_blocked(self, user):
        return self.bloqueados.filter(bloqueos.c.bloqueado_id == user.id).count() > 0

    def is_blocked_by(self, user):
        return self.bloqueadores.filter(bloqueos.c.bloqueador_id == user.id).count() > 0

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)

class ActividadCaceria(db.Model):
    __tablename__ = 'actividades_caceria'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(200))
    cupo_maximo = db.Column(db.Integer, nullable=False)

    creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    creador = db.relationship('Usuario', backref='actividades_creadas')


class InscripcionActividad(db.Model):
    __tablename__ = 'inscripciones_actividad'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades_caceria.id'), nullable=False)

    usuario = db.relationship('Usuario', backref='inscripciones')
    actividad = db.relationship('ActividadCaceria', backref='inscripciones')

    __table_args__ = (db.UniqueConstraint('usuario_id', 'actividad_id', name='_usuario_actividad_uc'),)


class ValoracionActividad(db.Model):
    __tablename__ = 'valoraciones_actividad'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades_caceria.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)  # Por ejemplo, de 1 a 5
    comentario = db.Column(db.Text)

    usuario = db.relationship('Usuario', backref='valoraciones')
    actividad = db.relationship('ActividadCaceria', backref='valoraciones')

    __table_args__ = (db.UniqueConstraint('usuario_id', 'actividad_id', name='_usuario_valoracion_uc'),)

class MensajeContacto(db.Model):
    __tablename__ = 'mensajes_contacto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=db.func.current_timestamp())
    leido = db.Column(db.Boolean, default=False)

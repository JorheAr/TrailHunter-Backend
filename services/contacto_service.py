from models import db, MensajeContacto

def guardar_mensaje_contacto(nombre, correo, mensaje):
    nuevo_mensaje = MensajeContacto(nombre=nombre, correo=correo, mensaje=mensaje)
    db.session.add(nuevo_mensaje)
    db.session.commit()
    return nuevo_mensaje

def obtener_mensajes_contacto():
    return MensajeContacto.query.order_by(MensajeContacto.fecha_envio.desc()).all()

def marcar_mensaje_como_leido(mensaje_id):
    mensaje = MensajeContacto.query.get(mensaje_id)
    if mensaje:
        mensaje.leido = True
        db.session.commit()
        return mensaje
    return None
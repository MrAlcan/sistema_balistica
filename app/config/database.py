from app.models.usuario import Usuario
from app.config.extensiones import db

def iniciar_datos():
    administradores = Usuario.query.all()

    if not administradores:
        nuevo_administrador = Usuario('administrador', 'administrador', 'administrador', 'administrador', '10000000', 'administrador@correo.com', 'administrador', 'administrador', 1)
        db.session.add(nuevo_administrador)
        db.session.commit()

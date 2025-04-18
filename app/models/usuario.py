from app.config.extensiones import db, bcrypt
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key = True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena= db.Column(db.String(200), nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    carnet = db.Column(db.String(15), unique=True, nullable=False)
    correo = db.Column(db.String(40), nullable=True)
    rol = db.Column(db.String(20))
    grado = db.Column(db.String(50))
    activo = db.Column(db.Integer, default=1)

    id_usuario_creado = db.Column(db.Integer, nullable=False)
    id_usuario_modificado = db.Column(db.Integer, nullable=False)
    fecha_creado = db.Column(db.DateTime)
    fecha_modificado = db.Column(db.DateTime)

    def __init__(self, nombre_usuario, contrasena, nombres, apellidos, carnet, correo, rol, grado, id_usuario_creado):
        self.nombre_usuario = nombre_usuario
        contrasena_segura = bcrypt.generate_password_hash(contrasena).decode('utf-8')
        self.contrasena = contrasena_segura
        self.nombres = nombres
        self.apellidos = apellidos
        self.carnet = carnet
        self.correo = correo
        self.rol = rol
        self.grado = grado
        self.id_usuario_creado = id_usuario_creado
        self.id_usuario_modificado = id_usuario_creado
        self.fecha_creado = datetime.now()
        self.fecha_modificado = datetime.now()
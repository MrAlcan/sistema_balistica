from app.config.extensiones import db
from datetime import datetime

class Casquillo(db.Model):
    __tablename__ = 'casquillos'

    id_casquillo = db.Column(db.Integer, primary_key=True)
    id_caso = db.Column(db.Integer, db.ForeignKey('casos.id_caso'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagen_original = db.Column(db.Text, nullable=True)
    imagen_procesada = db.Column(db.Text)
    imagen_contorno = db.Column(db.Text)
    csv = db.Column(db.Text, nullable=True)
    angulo_rotacion = db.Column(db.String(20), default='0.0')
    centro_contorno = db.Column(db.String(100), default='[0, 0]')
    activo = db.Column(db.Integer, default=1)

    id_usuario_creado = db.Column(db.Integer, nullable=False)
    id_usuario_modificado = db.Column(db.Integer, nullable=False)
    fecha_creado = db.Column(db.DateTime)
    fecha_modificado = db.Column(db.DateTime)

    def __init__(self, id_caso, tipo, img_original, img_procesada, img_contorno, csv, angulo, centro, id_creado):
        self.id_caso = id_caso
        self.tipo = tipo
        self.imagen_original = img_original
        self.imagen_procesada = img_procesada
        self.imagen_contorno = img_contorno
        self.csv = csv
        self.angulo_rotacion = angulo
        self.centro_contorno = centro
        self.id_usuario_creado = id_creado
        self.id_usuario_modificado = id_creado
        self.fecha_creado = datetime.now()
        self.fecha_modificado = datetime.now()


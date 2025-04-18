from app.config.extensiones import db
from datetime import datetime

class Caso(db.Model):
    __tablename__ = 'casos'
    
    id_caso = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    rup = db.Column(db.String(50), nullable=False)
    id_experto = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    activo = db.Column(db.Integer, default=1)

    id_usuario_creado = db.Column(db.Integer, nullable=False)
    id_usuario_modificado = db.Column(db.Integer, nullable=False)
    fecha_creado = db.Column(db.DateTime)
    fecha_modificado = db.Column(db.DateTime)


    def __init__(self, descripcion, departamento, rup, id_experto, id_creado):
        self.descripcion = descripcion
        self.departamento = departamento
        self.rup = rup
        self.id_experto = id_experto
        self.id_usuario_creado = id_creado
        self.id_usuario_modificado = id_creado
        self.fecha_creado = datetime.now()
        self.fecha_modificado = datetime.now()
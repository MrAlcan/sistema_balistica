from app.models.caso import Caso
from app.models.usuario import Usuario
from app.config.extensiones import db
from app.serializer.serializadorUniversal import SerializadorUniversal
from datetime import datetime

class ServiciosCaso():
    def crear(descripcion, departamento, rup, id_experto, id_creado):
        nuevo_caso = Caso(descripcion, departamento, rup, id_experto, id_creado)
        db.session.add(nuevo_caso)
        db.session.commit()
        return {'status': 'success'}
    
    def modificar(id_caso, id_modificado, descripcion=None, departamento=None, rup=None, id_experto=None):
        caso = Caso.query.get(id_caso)
        if not caso:
            return {'error': 'caso no encontrado'}


        if descripcion:
            caso.descripcion = descripcion
        if departamento:
            caso.departamento = departamento
        if rup:
            caso.rup = rup
        if id_experto:
            caso.id_experto = id_experto

        caso.id_usuario_modificado = id_modificado
        caso.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}
    
    def eliminar(id_caso, id_usuario):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso == id_caso).first()
        if not caso:
            return {'error': 'Caso no encontrado'}
        caso.activo = 0
        caso.id_usuario_modificado = id_usuario
        caso.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}
    
    def obtener_por_id(id_caso):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso==id_caso).first()
        if not caso:
            return None
        
        id_experto = caso.id_experto
        experto = Usuario.query.get(id_experto)

        nombres_perito = experto.nombres + " " + experto.apellidos
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto']
        respuesta = SerializadorUniversal.serializar_unico(caso, datos_requeridos)
        respuesta['perito'] = nombres_perito
        return respuesta
    
    def obtener_por_id_y_experto(id_caso, id_experto):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso==id_caso, Caso.id_experto==id_experto).first()
        if not caso:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto']
        respuesta = SerializadorUniversal.serializar_unico(caso, datos_requeridos)
        return respuesta
    
    def obtener_todos():
        casos = Caso.query.filter(Caso.activo==1).all()
        if not casos:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto']
        respuesta = SerializadorUniversal.serializar_lista(casos, datos_requeridos)
        for resp in respuesta:
            id_experto = resp['id_experto']
            experto = Usuario.query.get(id_experto)
            nombres_perito = experto.nombres + " " + experto.apellidos
            resp['perito'] = nombres_perito

        return respuesta
    
    def obtener_por_experto(id_experto):
        casos = Caso.query.filter(Caso.activo==1, Caso.id_experto==id_experto).all()
        if not casos:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto']
        respuesta = SerializadorUniversal.serializar_lista(casos, datos_requeridos)
        return respuesta


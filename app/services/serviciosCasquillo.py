from app.models.caso import Caso
from app.models.usuario import Usuario
from app.models.casquillo import Casquillo
from app.config.extensiones import db
from app.serializer.serializadorUniversal import SerializadorUniversal
from datetime import datetime
from flask import current_app
import os

class ServiciosCasquillo():
    def modificar_existentes(id_caso, ids_casquillos):

        casquillos = Casquillo.query.filter(Casquillo.activo==1, Casquillo.id_caso==id_caso).all()

        if ids_casquillos:
            if casquillos:
                for casquillo in casquillos:
                    if int(casquillo.id_casquillo) not in ids_casquillos:
                        casquillo.activo = 0
                        
                        
                        ruta_casquillo = os.path.join('app/static', str(casquillo.imagen_original))
                        filename = str(casquillo.imagen_original).split('/')[-1]
                        carpeta = str(casquillo.imagen_original).split('/')[-2]
                        carpeta_caso = str(casquillo.imagen_original).split('/')[-3]
                        ruta_casquillos = os.path.join('app', 'static', 'casos', carpeta_caso, carpeta, filename)
                        print(ruta_casquillos)
                        os.remove(ruta_casquillos)
                db.session.commit()
                    
                    
        return True
    

    def crear(id_caso, img_original, img_procesada, img_contorno, contornos, centro, id_creado, tipo):
        #casquillo = Casquillo(id_caso, tipo, img_original, img_procesada, img_contorno, csv, angulo, centro, id_creado)

        direccion_img_original = str(img_original).split('static')[1]
        direccion_img_procesada = str(img_procesada).split('static')[1]#+".png"
        direccion_img_contorno = str(img_contorno).split('static')[1]#+".png"
        direccion_contornos = str(contornos).split('static')[1]
        direccion_img_original = direccion_img_original.replace('\\', '/')
        direccion_img_procesada = direccion_img_procesada.replace('\\', '/')
        direccion_img_contorno = direccion_img_contorno.replace('\\', '/')
        direccion_contornos = direccion_contornos.replace('\\', '/')

        nuevo_casquillo = Casquillo(id_caso, tipo, direccion_img_original, direccion_img_procesada, direccion_img_contorno, direccion_contornos, 0, centro, id_creado)
        db.session.add(nuevo_casquillo)
        db.session.commit()
        return True
    
    def obtener_cantidad(id_caso):
        casquillos = Casquillo.query.filter(Casquillo.id_caso==id_caso).all()

        contador = 0
        if casquillos:
            for casquillo in casquillos:
                contador = contador + 1
        
        return contador

    def obtener_todos():
        casquillos = Casquillo.query.filter(Casquillo.activo==1).all()
        datos_requeridos = ['id_casquillo', 'id_caso', 'tipo', 'imagen_original', 'imagen_procesada', 'imagen_contorno', 'csv', 'angulo_rotacion', 'centro_contorno']

        respuesta = SerializadorUniversal.serializar_lista(casquillos, datos_requeridos)

        return respuesta
    
    def obtener_por_caso(id_caso):
        casquillos = Casquillo.query.filter(Casquillo.activo==1, Casquillo.id_caso==id_caso).all()
        if not casquillos:
            return None
        datos_requeridos = ['id_casquillo', 'id_caso', 'tipo', 'imagen_original', 'imagen_procesada', 'imagen_contorno', 'csv', 'angulo_rotacion', 'centro_contorno']

        respuesta = SerializadorUniversal.serializar_lista(casquillos, datos_requeridos)

        return respuesta
    
    def obtener_por_id(id_casquillo):
        casquillo = Casquillo.query.filter(Casquillo.activo==1, Casquillo.id_casquillo==id_casquillo).first()
        if not casquillo:
            return None
        datos_requeridos = ['id_casquillo', 'id_caso', 'tipo', 'imagen_original', 'imagen_procesada', 'imagen_contorno', 'csv', 'angulo_rotacion', 'centro_contorno']

        respuesta = SerializadorUniversal.serializar_unico(casquillo, datos_requeridos)

        return respuesta
    
    def actualizar_angulos(id_casquillo, angulo):
        casquillo = Casquillo.query.filter(Casquillo.activo==1, Casquillo.id_casquillo==id_casquillo).first()
        if not casquillo:
            return None
        
        casquillo.angulo_rotacion = str(angulo)
        db.session.commit()
        return True
        
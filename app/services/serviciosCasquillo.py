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
                        casquillo.activo == 0
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], casquillo.img_original))
                    
                    db.session.commit()
        return True
    

    def crear(id_caso, img_original, img_procesada, img_contorno, contornos, centro, id_creado):
        #casquillo = Casquillo(id_caso, tipo, img_original, img_procesada, img_contorno, csv, angulo, centro, id_creado)

        direccion_img_original = str(img_original).split('static')[1]
        direccion_img_procesada = str(img_procesada).split('static')[1]+".png"
        direccion_img_contorno = str(img_contorno).split('static')[1]+".png"
        direccion_contornos = str(contornos).split('static')[1]
        direccion_img_original = direccion_img_original.replace('\\', '/')
        direccion_img_procesada = direccion_img_procesada.replace('\\', '/')
        direccion_img_contorno = direccion_img_contorno.replace('\\', '/')
        direccion_contornos = direccion_contornos.replace('\\', '/')

        nuevo_casquillo = Casquillo(id_caso, 's/n', direccion_img_original, direccion_img_procesada, direccion_img_contorno, direccion_contornos, 0, centro, id_creado)
        db.session.add(nuevo_casquillo)
        db.session.commit()
        return True

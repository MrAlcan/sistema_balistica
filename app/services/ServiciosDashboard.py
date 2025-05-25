from app.models.usuario import Usuario
from app.models.caso import Caso
from app.models.casquillo import Casquillo

from app.config.extensiones import db, bcrypt

from app.serializer.serializadorUniversal import SerializadorUniversal

from flask import current_app
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import random
import string
from sqlalchemy import func

DICCIONARIO_MESES = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}

DICCIONARIO_DIAS = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

class ServiciosDashboard():

    def obtener_cantidad_peritos_administradores():

        roles = db.session.query(Usuario.rol, func.count(Usuario.id_usuario)).group_by(Usuario.rol).all()
        conteo_roles = dict(roles)
        admin_count = conteo_roles.get('administrador', 0)
        perito_count = conteo_roles.get('perito', 0)

        respuesta = {'administradores': admin_count,
                     'peritos': perito_count}
        
        return respuesta
    
    def obtener_cantidad_usuarios():
        usuarios = db.session.query(func.count(Usuario.id_usuario)).scalar()
        
        return usuarios
    
    def obtener_cantidad_casos():
        casos = db.session.query(func.count(Caso.id_caso)).scalar()
        return casos

    def obtener_cantidad_casquillos():
        casquillos = db.session.query(func.count(Casquillo.id_casquillo)).scalar()
        return casquillos
    
    def obtener_cantidad_usuarios_registrados_ultimos_meses():
        fecha_actual = datetime.now()

        
        cantidad_usuarios = ['0']*6
        nombre_meses = ['a']*6

        contador = 6

        while (contador>0):
            contador = contador -1
 
            fecha_inicio = fecha_actual.replace(day=1)
            fecha_final = fecha_actual + relativedelta(months=1)
            fecha_final = fecha_final.replace(day=1)
            mes_string_l = fecha_inicio.strftime('%B')
            mes_espanol = DICCIONARIO_MESES[mes_string_l]
            usuarios_nuevos = Usuario.query.filter(Usuario.fecha_creado>=fecha_inicio, Usuario.fecha_creado<fecha_final).count()

            cantidad_usuarios[contador] = usuarios_nuevos
            nombre_meses[contador] = mes_espanol

            fecha_actual = fecha_actual - relativedelta(months=1)

        respuesta = {
            'cantidad': cantidad_usuarios,
            'mes': nombre_meses
        }

        return respuesta
    
    def obtener_cantidad_casos_registrados_ultimos_meses():
        fecha_actual = datetime.now()

        
        cantidad_casos = ['0']*6
        nombre_meses = ['a']*6

        contador = 6

        while (contador>0):
            contador = contador -1
 
            fecha_inicio = fecha_actual.replace(day=1)
            fecha_final = fecha_actual + relativedelta(months=1)
            fecha_final = fecha_final.replace(day=1)
            mes_string_l = fecha_inicio.strftime('%B')
            mes_espanol = DICCIONARIO_MESES[mes_string_l]
            casos_nuevos = Caso.query.filter(Caso.activo==1, Caso.fecha_creado>=fecha_inicio, Caso.fecha_creado<fecha_final).count()

            cantidad_casos[contador] = casos_nuevos
            nombre_meses[contador] = mes_espanol

            fecha_actual = fecha_actual - relativedelta(months=1)

        respuesta = {
            'cantidad': cantidad_casos,
            'mes': nombre_meses
        }

        return respuesta
    
    def obtener_cantidad_casquillos_registrados_ultimos_meses():
        fecha_actual = datetime.now()

        
        cantidad_casquillos = ['0']*6
        nombre_meses = ['a']*6

        contador = 6

        while (contador>0):
            contador = contador -1
 
            fecha_inicio = fecha_actual.replace(day=1)
            fecha_final = fecha_actual + relativedelta(months=1)
            fecha_final = fecha_final.replace(day=1)
            mes_string_l = fecha_inicio.strftime('%B')
            mes_espanol = DICCIONARIO_MESES[mes_string_l]
            casquillos_nuevos = Casquillo.query.filter(Casquillo.activo==1, Casquillo.fecha_creado>=fecha_inicio, Casquillo.fecha_creado<fecha_final).count()

            cantidad_casquillos[contador] = casquillos_nuevos
            nombre_meses[contador] = mes_espanol

            fecha_actual = fecha_actual - relativedelta(months=1)

        respuesta = {
            'cantidad': cantidad_casquillos,
            'mes': nombre_meses
        }

        return respuesta
    
    def obtener_cantidad_casos_por_departamento():

        roles = db.session.query(Caso.departamento, func.count(Caso.id_caso)).group_by(Caso.departamento).all()
        conteo_roles = dict(roles)

        respuesta = {
            'La Paz': conteo_roles.get('La Paz', 0),
            'Cochabamba': conteo_roles.get('Cochabamba', 0),
            'Santa Cruz': conteo_roles.get('Santa Cruz', 0),
            'Potosi': conteo_roles.get('Potosi', 0),
            'Oruro': conteo_roles.get('Oruro', 0),
            'Tarija': conteo_roles.get('Tarija', 0),
            'Chuquisaca': conteo_roles.get('Chuquisaca', 0),
            'Beni': conteo_roles.get('Beni', 0),
            'Pando': conteo_roles.get('Pando', 0),
        }

        return respuesta
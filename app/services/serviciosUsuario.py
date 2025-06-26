from app.models.usuario import Usuario

from app.config.extensiones import db, bcrypt

from app.serializer.serializadorUniversal import SerializadorUniversal
from flask_mail import Mail, Message
from flask import current_app
from .. import mail
from datetime import datetime, date, timedelta
from app.services.templateEmail import generar_email
import random
import string

def generar_contrasena():

    lowercase = random.sample(string.ascii_lowercase, 2)
    uppercase = random.sample(string.ascii_uppercase, 2)
    digits = random.sample(string.digits, 2)
    symbols = random.sample('*-@+!¡', 2)

    password_chars = lowercase + uppercase + digits + symbols

    random.shuffle(password_chars)

    return ''.join(password_chars)

def generar_numero_seis_digitos():

    return random.randint(100000, 999999)

def enviar_credenciales(recipient: str, username: str, password: str) -> None:
    subject = 'Tus credenciales de acceso'
    body = (
        f"Hola,\n\n"
        f"Aquí tienes tus credenciales de acceso:\n"
        f"Usuario: {username}\n"
        f"Contraseña: {password}\n\n"
        "Saludos."
    )
    body = generar_email(nombre_usuario=username, username=username, password=password, pagina='https://kipka.sistema-web.com/inicio/ingresar')
    msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = body

    mail.send(msg)


def enviar_codigo_numerico(recipient: str, code: int) -> None:

    subject = 'Código de verificación'
    body = (
        f"Hola,\n\n"
        f"Tu código de verificación es: {code}\n\n"
        "No compartas este código con nadie."
    )
    msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = body

    mail.send(msg)

class ServiciosUsuario():

    def crear(nombres, apellidos, carnet, correo, rol, grado, id_usuario_creado):

        nombre_usuario = str(nombres).split(' ')[0] + "." + str(apellidos).split(' ')[0]
        usuarios = Usuario.query.filter(Usuario.nombre_usuario==nombre_usuario).all()
        if usuarios:
            usuario_existente = True
            contador = 0
            while usuario_existente:
                contador = contador + 1
                nombre_usuario_nuevo = nombre_usuario + "." + str(contador)
                usuario_mod = Usuario.query.filter(Usuario.nombre_usuario==nombre_usuario_nuevo).all()
                if not usuario_mod:
                    usuario_existente = False
                    nombre_usuario = nombre_usuario_nuevo
                    break
        
        #contrasena = random()
        #contrasena = 'AS465esrf654@*' # generar contraseña random
        contrasena = generar_contrasena()
        
        nuevo_usuario = Usuario(nombre_usuario, contrasena, nombres, apellidos, carnet, correo, rol, grado, id_usuario_creado)
        db.session.add(nuevo_usuario)
        db.session.commit()
        if nuevo_usuario:
            enviar_credenciales(correo, nombre_usuario, contrasena)
        return {'status': 'success'}
    
    def modificar(id_usuario, id_usuario_modificado, contrasena=None, nombres=None, apellidos=None, carnet=None, correo=None, rol=None, grado=None):

        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {'status': 'Usuario no encontrado'}
        
        if contrasena:
            usuario.contrasena = contrasena
        if nombres:
            usuario.nombres = nombres
        if apellidos:
            usuario.apellidos = apellidos
        if carnet:
            usuario.carnet = carnet
        if correo:
            usuario.correo = correo
        if rol:
            usuario.rol = rol
        if grado:
            usuario.grado = grado

        usuario.id_usuario_modificado = id_usuario_modificado
        usuario.fecha_modificado = datetime.now()

        db.session.commit()

        return {'status': 'success'}
    
    def modificar_contrasena(id_usuario, contrasena_antigua, contrasena_nueva):
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return {'status': 'Usuario no encontrado'}
        
        if bcrypt.check_password_hash(usuario.contrasena, contrasena_antigua):
            usuario.contrasena = bcrypt.generate_password_hash(contrasena_nueva)
            db.session.commit()
            return {'status': 'success'}
        else:
            return {'status': 'contrasena erronea'}
    
    def eliminar(id_usuario, id_usuario_modifico):
        usuario = Usuario.query.filter(Usuario.activo==1, Usuario.id_usuario == id_usuario).first()

        if not usuario:
            return {'error': 'usuario no encontrado'}
        
        usuario.activo = 0
        usuario.id_usuario_modificado = id_usuario_modifico
        usuario.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}

    def habilitar(id_usuario, id_usuario_modifico):
        usuario = Usuario.query.filter(Usuario.activo==0, Usuario.id_usuario == id_usuario).first()

        if not usuario:
            return {'error': 'usuario no encontrado'}
        
        usuario.activo = 1
        usuario.id_usuario_modificado = id_usuario_modifico
        usuario.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}
    
    def obtener_activos():
        usuarios = Usuario.query.filter(Usuario.activo==1).all()

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado']
        
        respuesta = SerializadorUniversal.serializar_lista(usuarios, datos_requeridos)

        return respuesta
    
    def obtener_todos():
        usuarios = Usuario.query.all()

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo']
        
        respuesta = SerializadorUniversal.serializar_lista(usuarios, datos_requeridos)

        return respuesta
    
    def obtener_administradores():
        usuarios = Usuario.query.filter(Usuario.activo==1, Usuario.rol=='Administrador').all()

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo']
        
        respuesta = SerializadorUniversal.serializar_lista(usuarios, datos_requeridos)

        return respuesta

    def obtener_peritos():
        usuarios = Usuario.query.filter(Usuario.activo==1, Usuario.rol=='Perito').all()

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo']
        
        respuesta = SerializadorUniversal.serializar_lista(usuarios, datos_requeridos)

        return respuesta
    
    def obtener_por_id(id_usuario):
        usuario = Usuario.query.get(id_usuario)

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo', 'user_img', 'ultima_conexion']
        
        respuesta = SerializadorUniversal.serializar_unico(usuario, datos_requeridos)

        if not respuesta['user_img']:
            respuesta['user_img'] = '/dist/img/user2-160x160.jpg'

        return respuesta
    
    def subir_imagen(id_usuario, direccion):
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return None
        
        usuario.user_img = direccion
        db.session.commit()

        return True
    
    def verificacion_doble(id_usuario):
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None
        
        codigo_numerico = generar_numero_seis_digitos()

        usuario.codigo_numerico = codigo_numerico
        db.session.commit()

        enviar_codigo_numerico(str(usuario.correo), codigo_numerico)

        return True
    
    def validar_codigo_numerico(id_usuario, codigo):
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return None
        
        codigo_numerico_db = str(usuario.codigo_numerico)
        codigo_numerico_cliente = str(codigo)

        if codigo_numerico_db == codigo_numerico_cliente:
            return str(usuario.rol)
        else:
            return None
        
        #return str(usuario.codigo_numerico)

    def obtener_por_correo(correo):
        usuario = Usuario.query.filter(Usuario.correo==correo).first()

        if not usuario:
            return None
        
        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo', 'user_img']
        
        respuesta = SerializadorUniversal.serializar_unico(usuario, datos_requeridos)

        return respuesta
    
    def obtener_por_nombre_usuario(nombre_usuario):
        usuario = Usuario.query.filter(Usuario.nombre_usuario==nombre_usuario).first()

        if not usuario:
            return None
        
        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo', 'user_img']
        
        respuesta = SerializadorUniversal.serializar_unico(usuario, datos_requeridos)

        return respuesta
    
    def actualizar_ultima_conexion(id_usuario):
        return None
        '''usuario = Usuario.query.filter(Usuario.activo==1, Usuario.id_usuario==id_usuario).first()

        if not usuario:
            return None
        
        usuario.ultima_conexion = datetime.now()
        db.session.commit()
        return True'''
    
    def actualizar_ultima_conexion_inicio_cerrar(id_usuario):
        usuario = Usuario.query.filter(Usuario.activo==1, Usuario.id_usuario==id_usuario).first()

        if not usuario:
            return None
        
        usuario.ultima_conexion = datetime.now()
        db.session.commit()
        return True
        

        
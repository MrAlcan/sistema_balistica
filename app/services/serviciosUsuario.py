from app.models.usuario import Usuario

from app.config.extensiones import db, bcrypt

from app.serializer.serializadorUniversal import SerializadorUniversal

from datetime import datetime, date, timedelta
import random

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
        contrasena = 'AS465esrf654@*' # generar contraseña random
        
        nuevo_usuario = Usuario(nombre_usuario, contrasena, nombres, apellidos, carnet, correo, rol, grado, id_usuario_creado)
        db.session.add(nuevo_usuario)
        db.session.commit()
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
    
    def eliminar(id_usuario):
        usuario = Usuario.query.filter(Usuario.activo==1, Usuario.id_usuario == id_usuario).first()

        if not usuario:
            return {'error': 'usuario no encontrado'}
        
        usuario.activo = 0
        db.session.commit()
        return {'status': 'success'}

    def habilitar(id_usuario):
        usuario = Usuario.query.filter(Usuario.activo==0, Usuario.id_usuario == id_usuario).first()

        if not usuario:
            return {'error': 'usuario no encontrado'}
        
        usuario.activo = 1
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

        datos_requeridos = ['id_usuario', 'nombre_usuario', 'nombres', 'apellidos', 'carnet', 'correo', 'rol', 'grado', 'activo', 'user_img']
        
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

        
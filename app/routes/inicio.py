from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies, get_jwt
from app.services.serviciosAutenticacion import ServiciosAutenticacion, no_iniciar_sesion, token_requerido
import os
from app.services.serviciosUsuario import ServiciosUsuario

inicio_bp = Blueprint('inicio_bp', __name__)

@inicio_bp.route('/ingresar', methods=['GET', 'POST'])
@no_iniciar_sesion
def vista_ingresar():
    if request.method == 'POST':
        datos = request.form
        nombre_usuario = datos['nombre_usuario']
        contrasena = datos['contrasena']

        respuesta_usuario, dato_usuario = ServiciosAutenticacion.autenticar_nombre_usuario(nombre_usuario)

        if not respuesta_usuario:
            return render_template('ingresar.html', usuario_mensaje = dato_usuario, nombre_usuario = nombre_usuario, contrasena = contrasena)
        
        respuesta_contrasena, dato_contrasena = ServiciosAutenticacion.autenticar_contrasena(dato_usuario, contrasena)

        if not respuesta_contrasena:
            return render_template('ingresar.html', contrasena_mensaje = dato_contrasena, nombre_usuario = nombre_usuario, contrasena = contrasena)
        
        print(f"bienvenido {dato_contrasena}")

        usuario = ServiciosUsuario.obtener_por_nombre_usuario(nombre_usuario)
        id_usuario = usuario['id_usuario']

        envio_codigo = ServiciosUsuario.verificacion_doble(id_usuario)

        return redirect(url_for('inicio_bp.vista_verificacion', id=id_usuario))



        token = ServiciosAutenticacion.generar_token(dato_usuario)
        token = str(token)
        print(token)
        
        if str(dato_contrasena)=='administrador':
            resp = make_response(redirect(url_for('administrador_bp.vista_inicio')))

        elif str(dato_contrasena)=='perito':
            resp = make_response(redirect(url_for('perito_bp.vista_inicio')))
        
        set_access_cookies(resp, token)
        return resp
    

    return render_template('ingresar.html')

@inicio_bp.route('/verificacion/<id>', methods=['GET', 'POST'])
def vista_verificacion(id):
    #envio_codigo = ServiciosUsuario.verificacion_doble(id)
    if request.method=='POST':
        datos = request.form
        codigo_verificacion = str(datos['codigo'])
        verificar_codigo = ServiciosUsuario.validar_codigo_numerico(id, codigo_verificacion)
        if verificar_codigo:
            token = ServiciosAutenticacion.generar_token(id)
            token = str(token)
            #print(token)
            #ServiciosUsuario.actualizar_ultima_conexion_inicio_cerrar(id)
            
            if str(verificar_codigo)=='administrador':
                resp = make_response(redirect(url_for('administrador_bp.vista_inicio')))

            elif str(verificar_codigo)=='perito':
                resp = make_response(redirect(url_for('perito_bp.vista_inicio')))
            
            set_access_cookies(resp, token)
            return resp
        else:
            return render_template('verificacion.html', usuario_mensaje = 'Codigo Erroneo', codigo = codigo_verificacion)


    return render_template('verificacion.html')


@inicio_bp.route('/cerrar_sesion', methods=['GET'])
@jwt_required()
def cerrar_sesion():
    claims = get_jwt()
    id_usuario = claims.get('id_usuario')
    ServiciosUsuario.actualizar_ultima_conexion_inicio_cerrar(id_usuario)
    resp = make_response(redirect(url_for('inicio_bp.vista_ingresar')))
    unset_jwt_cookies(resp)
    return resp
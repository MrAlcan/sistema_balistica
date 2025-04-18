from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from app.services.serviciosAutenticacion import token_requerido
from app.services.serviciosUsuario import ServiciosUsuario
import os

administrador_bp = Blueprint('administrador_bp', __name__)

@administrador_bp.route('/inicio', methods=['GET'])
@token_requerido
def vista_inicio(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]


    return render_template('administrador/inicio.html', datos=datos)

@administrador_bp.route('/usuarios/totales', methods=['GET'])
@token_requerido
def vista_usuarios_totales(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    usuarios = ServiciosUsuario.obtener_todos()

    return render_template('administrador/usuarios.html', datos=datos, usuarios=usuarios)

@administrador_bp.route('/usuarios/agregar', methods=['POST'])
@token_requerido
def agregar_usuario(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    formulario = request.form

    nuevo_usuario = ServiciosUsuario.crear(formulario['nombres'],
                                           formulario['apellidos'],
                                           formulario['carnet'],
                                           formulario['correo'],
                                           formulario['rol'],
                                           formulario['grado'],
                                           id_usuario)
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_usuarios_totales'))
    
@administrador_bp.route('/usuarios/editar/<id>', methods=['POST'])
@token_requerido
def editar_usuario(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    formulario = request.form

    usuario_editado = ServiciosUsuario.modificar(id_usuario=id,
                                               id_usuario_modificado=id_usuario,
                                               nombres=formulario['nombres'],
                                               apellidos=formulario['apellidos'],
                                               carnet=formulario['carnet'],
                                               correo=formulario['correo'],
                                               rol=formulario['rol'],
                                               grado=formulario['grado'])
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_usuarios_totales'))

@administrador_bp.route('/usuarios/eliminar/<id>', methods=['GET'])
@token_requerido
def eliminar_usuario(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    usuario_eliminado = ServiciosUsuario.eliminar(id, id_usuario)

    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_usuarios_totales'))

@administrador_bp.route('/usuarios/habilitar/<id>', methods=['GET'])
@token_requerido
def habilitar_usuario(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    usuario_eliminado = ServiciosUsuario.habilitar(id, id_usuario)

    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_usuarios_totales'))

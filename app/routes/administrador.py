from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from app.services.serviciosAutenticacion import token_requerido
from app.services.serviciosUsuario import ServiciosUsuario
import os

administrador_bp = Blueprint('administrador_bp', __name__)

@administrador_bp.route('/inicio', methods=['GET'])
@token_requerido
def vista_inicio(datos_usuario):
    primer_nombre = datos_usuario['primer_nombre']
    primer_apellido = datos_usuario['primer_apellido']
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    user_img = datos['user_img']


    return render_template('administrador/inicio.html', nombre = primer_nombre, apellido = primer_apellido, datos=datos, user_img=user_img)
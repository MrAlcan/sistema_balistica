from flask import Blueprint, jsonify, render_template, request, redirect, url_for, send_from_directory, current_app

from app.services.serviciosUsuario import ServiciosUsuario

from datetime import datetime



from app.services.serviciosAutenticacion import ServiciosAutenticacion, token_requerido


import os
import time
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_HOMEWORK = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp3', 'wav', 'ogg'}

def allowed_file_homework(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_HOMEWORK

# Función para verificar si la extensión de la imagen es válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para cambiar el tamaño de la imagen antes de guardarla
def resize_image(image, max_size=(800, 800)):
    image.thumbnail(max_size)
    return image

# Función para convertir a formato JPG
def convert_to_jpg(image):
    if image.format != 'JPEG':
        img = image.convert('RGB')
        return img
    return image


perfil_bp = Blueprint('perfil_bp', __name__)


@perfil_bp.route('/configurar', methods=['POST'])
@token_requerido
def configurar_perfil(datos_usuario):

    id_usuario = datos_usuario['id_usuario']

    datos = request.form

    nombres = datos['nombres']
    apellidos = datos['apellidos']
    correo = datos['correo']


    respuesta = ServiciosUsuario.modificar(id_usuario=id_usuario,
                                           id_usuario_modificado=id_usuario,
                                           nombres=nombres,
                                           apellidos=apellidos,
                                           correo=correo)

    

    referer = request.referrer

    if 'image' not in request.files:
        if referer:
            return redirect(referer)
        else:
            # Si no hay referencia, rediriges a una página predeterminada
            return redirect(url_for('inicio_bp.vista_ingresar'))

    file = request.files['image']
    
    # Verificar si se seleccionó un archivo
    if file.filename == '':
        if referer:
            return redirect(referer)
        else:
            # Si no hay referencia, rediriges a una página predeterminada
            return redirect(url_for('inicio_bp.vista_ingresar'))

    # Verificar si el archivo tiene una extensión permitida
    if file and allowed_file(file.filename):
        # Renombrar el archivo usando el id de sesión y la fecha actual para evitar colisiones
        session_id = str(id_usuario)  # Aquí se debe usar el ID de sesión o cualquier identificador único
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{session_id}_{timestamp}.jpg"

        # Asegurarse de que el nombre del archivo sea seguro
        filename = secure_filename(filename)

        # Crear el directorio si no existe
        if not os.path.exists(current_app.config['UPLOAD_FOLDER_PERFIL']):
            os.makedirs(current_app.config['UPLOAD_FOLDER_PERFIL'])

        # Guardar la imagen temporalmente
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PERFIL'], filename)

        # Abrir la imagen con Pillow
        image = Image.open(file)

        # Redimensionar y convertir la imagen
        image = resize_image(image)
        image = convert_to_jpg(image)

        # Guardar la imagen final en el directorio
        image.save(file_path, 'JPEG')

        # Devolver la URL de la imagen guardada
        imagen_url = f'/perfil/{filename}'

        sub_img = ServiciosUsuario.subir_imagen(id_usuario, imagen_url)



        if referer:
            return redirect(referer)
        else:
            # Si no hay referencia, rediriges a una página predeterminada
            return redirect(url_for('inicio_bp.vista_ingresar'))

    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('inicio_bp.vista_ingresar'))


    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('inicio_bp.vista_ingresar'))

@perfil_bp.route('/contrasena', methods=['POST'])
@token_requerido
def configurar_contrasena(datos_usuario):
    id_usuario = datos_usuario['id_usuario']

    datos = request.form

    contrasena_ant = datos['contrasena_ant']
    contrasena_nueva = datos['contrasena_nueva']

    ServiciosUsuario.modificar_contrasena(id_usuario, contrasena_ant, contrasena_nueva)

    referer = request.referrer

    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('inicio_bp.vista_ingresar'))
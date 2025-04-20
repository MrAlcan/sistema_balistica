from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from app.services.serviciosAutenticacion import token_requerido
from app.services.serviciosUsuario import ServiciosUsuario
from app.services.serviciosCaso import ServiciosCaso
from app.services.serviciosCasquillo import ServiciosCasquillo
from app.controllers.ProcesarBala import ProcesarBala
import os
from werkzeug.utils import secure_filename

perito_bp = Blueprint('perito_bp', __name__)

@perito_bp.route('/inicio', methods=['GET'])
@token_requerido
def vista_inicio(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]


    return render_template('perito/inicio.html', datos=datos)



# ----------------------------- VISTAS CASOS ------------------------------------

@perito_bp.route('/casos', methods=['GET'])
@token_requerido
def vista_casos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    casos = ServiciosCaso.obtener_por_experto(id_usuario)

    return render_template('perito/casos.html', datos=datos, casos=casos)

@perito_bp.route('/casos/ver/<id>', methods=['GET'])
@token_requerido
def vista_caso_id(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    caso = ServiciosCaso.obtener_por_id_y_experto(id, id_usuario)

    if not caso:

        referer = request.referrer
        if referer:
            return redirect(referer)
        else:
            # Si no hay referencia, rediriges a una página predeterminada
            return redirect(url_for('perito_bp.vista_casos'))
    
    casquillos = ServiciosCasquillo.obtener_por_caso(id)

    return render_template('perito/ver_caso.html', datos=datos, caso=caso, casquillos=casquillos)




# ----------------------------- FIN VISTAS CASOS ------------------------------------
# ------------------------------- FUNCIONES CASOS ------------------------------------

@perito_bp.route('/casos/agregar', methods=['POST'])
@token_requerido
def agregar_caso(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    formulario = request.form

    nuevo_caso = ServiciosCaso.crear(formulario['descripcion'],
                                     formulario['departamento'],
                                     formulario['rup'],
                                     id_usuario,
                                     id_usuario)
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('perito_bp.vista_casos'))

@perito_bp.route('/casos/editar/<id>', methods=['POST'])
@token_requerido
def editar_caso(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    formulario = request.form

    nuevo_caso = ServiciosCaso.modificar(id,
                                         id_usuario,
                                         formulario['descripcion'],
                                         formulario['departamento'],
                                         formulario['rup'],
                                         id_usuario)
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('perito_bp.vista_casos'))
    
@perito_bp.route('/casos/eliminar/<id>', methods=['GET'])
@token_requerido
def eliminar_caso(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]

    caso_eliminado = ServiciosCaso.eliminar(id, id_usuario)

    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('perito_bp.vista_casos'))

# ------------------------------- FIN FUNCIONES CASOS ------------------------------------

# ------------------------------------- FUNCIONES CASQUILLOS -----------------------------------------------------------------------------

@perito_bp.route('/casquillos/agregar/<id>', methods=['POST'])
@token_requerido
def agregar_casquillos(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]


    # 1) Recogemos datos
    existing = request.form.getlist('existing_paths[]')  # rutas que siguen
    new_files = request.files.getlist('casquillos_images[]')

    carpeta_caso = 'caso_'+str(id)
    '''if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso)):
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso))
        except OSError:
            pass'''
    direccion_carpeta_casos_fold = os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'])
    if not os.path.exists(direccion_carpeta_casos_fold):
        os.mkdir(direccion_carpeta_casos_fold)
    
    direccion_carpeta_caso = os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso)
    if not os.path.exists(direccion_carpeta_caso):
        os.mkdir(direccion_carpeta_caso)

    direccion_carpeta_originales = os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso, 'original')
    direccion_carpeta_mascaras = os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso, 'mascara')
    direccion_carpeta_procesados = os.path.join(current_app.config['UPLOAD_FOLDER_CASOS'], carpeta_caso, 'procesado')

    if not os.path.exists(direccion_carpeta_originales):
        os.mkdir(direccion_carpeta_originales)
    if not os.path.exists(direccion_carpeta_mascaras):
        os.mkdir(direccion_carpeta_mascaras)
    if not os.path.exists(direccion_carpeta_procesados):
        os.mkdir(direccion_carpeta_procesados)

    contador = ServiciosCasquillo.obtener_cantidad(id)
    
    if existing:
        ids_casquillos = []
        for id_casquillo in existing:
            ids_casquillos.append(int(id_casquillo))
        casquillos_existentes = ServiciosCasquillo.modificar_existentes(id, ids_casquillos)



    # 4) Guardar los nuevos
    procesar_bala = ProcesarBala()
    for f in new_files:
        if f and f.filename:
            filename = secure_filename(f.filename)
            filename = str(filename).split('-')[0]
            filename = filename + "-" + str(contador)+".png"
            filename = secure_filename(filename)
            contador = contador + 1
            nombre_contorno = str(filename).split('.')[0]+".txt"
            save_path = os.path.join(direccion_carpeta_originales, filename)
            direccion_img_procesada = os.path.join(direccion_carpeta_procesados, filename)
            direccion_img_contornos = os.path.join(direccion_carpeta_mascaras, filename)
            direccion_contornos = os.path.join(direccion_carpeta_mascaras, nombre_contorno)
            f.save(save_path)

            res, centro = procesar_bala.procesar(save_path, direccion_img_procesada, direccion_img_contornos, direccion_contornos)
            # almacena la ruta relativa (p.ej. 'uploads/'+filename)
            casquillo_nuevo = ServiciosCasquillo.crear(id,
                                                       save_path,
                                                       direccion_img_procesada,
                                                       direccion_img_contornos,
                                                       direccion_contornos,
                                                       centro,
                                                       id_usuario)
        

    return redirect(url_for('perito_bp.vista_casos'))
            
    





# ------------------------------------- FIN FUNCIONES CASQUILLOS -----------------------------------------------------------------------------
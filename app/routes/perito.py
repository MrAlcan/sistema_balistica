from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from app.services.serviciosAutenticacion import token_requerido
from app.services.serviciosUsuario import ServiciosUsuario
from app.services.serviciosCaso import ServiciosCaso
from app.services.serviciosCasquillo import ServiciosCasquillo
from app.controllers.ProcesarBala import ProcesarBala
from app.services.ServiciosDashboard import ServiciosDashboard
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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    cantidad_roles = ServiciosDashboard.obtener_cantidad_peritos_administradores()
    cantidad_usuarios = ServiciosDashboard.obtener_cantidad_usuarios()
    cantidad_casos = ServiciosDashboard.obtener_cantidad_casos()
    cantidad_casquillos = ServiciosDashboard.obtener_cantidad_casquillos()
    usuarios_nuevos = ServiciosDashboard.obtener_cantidad_usuarios_registrados_ultimos_meses()
    casquillos_nuevos = ServiciosDashboard.obtener_cantidad_casquillos_registrados_ultimos_meses()
    casos_nuevos = ServiciosDashboard.obtener_cantidad_casos_registrados_ultimos_meses()
    casos_departamento = ServiciosDashboard.obtener_cantidad_casos_por_departamento()

    datos_dashboard = {
        'cantidad_roles': cantidad_roles,
        'cantidad_usuarios': cantidad_usuarios,
        'cantidad_casos': cantidad_casos,
        'cantidad_casquillos': cantidad_casquillos,
        'usuarios_nuevos': usuarios_nuevos,
        'casquillos_nuevos': casquillos_nuevos,
        'casos_nuevos': casos_nuevos,
        'casos_departamento': casos_departamento
    }


    return render_template('perito/inicio.html', datos=datos, datos_dashboard=datos_dashboard)



# ----------------------------- VISTAS CASOS ------------------------------------

@perito_bp.route('/casos', methods=['GET'])
@token_requerido
def vista_casos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    casos = ServiciosCaso.obtener_por_experto(id_usuario)

    return render_template('perito/casos.html', datos=datos, casos=casos)

@perito_bp.route('/casos/ver/<id>', methods=['GET'])
@token_requerido
def vista_caso_id(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    formulario = request.form

    nuevo_caso = ServiciosCaso.crear(formulario['descripcion'],
                                     formulario['departamento'],
                                     formulario['rup'],
                                     id_usuario,
                                     id_usuario)
    
    referer = request.referrer
    return jsonify({'success': True}), 200
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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    formulario = request.form

    nuevo_caso = ServiciosCaso.modificar(id,
                                         id_usuario,
                                         formulario['descripcion'],
                                         formulario['departamento'],
                                         formulario['rup'],
                                         id_usuario)
    
    referer = request.referrer
    return jsonify({'success': True}), 200
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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)


    # 1) Recogemos datos
    existing = request.form.getlist('existing_paths[]')  # rutas que siguen
    new_files = request.files.getlist('casquillos_images[]')
    tipos = request.form.getlist('casquillos_tipos[]')
    print(tipos)
    for tip in tipos:
        print(tip)

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
    contador_lista = 0
    for f in new_files:
        if f and f.filename:
            tipo_casquillo = tipos[contador_lista]
            contador_lista = contador_lista + 1
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
                                                       id_usuario,
                                                       tipo_casquillo)
        

    return jsonify({'success': True}), 200
    return redirect(url_for('perito_bp.vista_casos'))
            
    
@perito_bp.route('/casquillos/angulos/procesar', methods=['POST'])
@token_requerido
def procesar_angulos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    def factorial(numero):
        fact = 1
        for i in range(1,numero+1,1):
            fact = fact * i
        return fact
    
    def combinatoria(numero):
        result = factorial(numero) / (factorial(numero-2) * 2)
        return result


    angulos = []
    direcciones = []
    ids_balas = []

    data = request.get_json(force=True)
    rots = data.get('rotations', [])
    print(data)
    print(len(rots))
    cantidad_casquillos = int(len(rots))
    cantidad_comparaciones = combinatoria(cantidad_casquillos)
    #results = {}
    for item in rots:
        cid = item.get('id')
        angle = item.get('angle')
        casquillo_proc = ServiciosCasquillo.obtener_por_id(cid)
        #direccion_contorno = "app/static"+str(casquillo_proc['csv'])
        direccion_contorno = "/var/www/sistema_balistica/app/static"+str(casquillo_proc['csv'])
        angulos.append(angle)
        direcciones.append(direccion_contorno)
        ids_balas.append(cid)
        # aquí podrías, por ejemplo, rotar las imágenes en disco con Pillow…
        #results[cid] = {
        #    'angle_received': angle,
        #    'status': 'ok'
        #}
    #return jsonify(results), 200

    #data = request.json
    #angulos = data.get('angulos', [])
    #direcciones = data.get('direcciones', [])
    #ids_balas = data.get('ids', [])
    print(angulos)
    print(direcciones)

    cantidad_armas = 1

    if len(direcciones) < 2:
        print('pocas direcciones')
        cuerpo = {
            'textos' : ['solo hay un arma'],
            'similitudes' : []
        }
        return jsonify(cuerpo)
    else:
        print('hacer')

        obj_bala = ProcesarBala()

        similitudes = []
        comparaciones_dir = []
        cantidad_pixeles_iguales = []
        cantidad_pixeles_totales = []
        diferencia_centros_lista = []
        porcentaje_diferencia_centros_list = []

        comparaciones = len(direcciones)

        cantidad_armas = [0] * len(direcciones)
        cantidad_armas[0] = 1

        auxiliar = 1

        distancias_centro = ['0']*comparaciones
        texto_centros = ['0']*comparaciones

        image_size = (640, 640)
        height = 640
        width = 640
        center = (image_size[0] // 2, image_size[1] // 2)

        media_comparaciones = 0





        for i in range(0, comparaciones-1, 1):
            
            for j in range(i+1, comparaciones, 1):
                print(i, " ", j)
                texto_comparacion = f"Comparacion de la imagen {ids_balas[i]} con la imagen {ids_balas[j]}"
                comparaciones_dir.append(texto_comparacion)

                
                

                ang_1 = int(angulos[i])
                ang_2 = int(angulos[j])

                ang_1 = -ang_1
                ang_2 = -ang_2

                bala_act = ServiciosCasquillo.actualizar_angulos(ids_balas[i], ang_1)
                bala_act_2 = ServiciosCasquillo.actualizar_angulos(ids_balas[j], ang_2)

                similitud, pixeles_iguales, total_pixeles, centro, centro_c_1, centro_c_2, diferencia_centros, porcentaje_dif = obj_bala.obtener_similitud(direcciones[i], direcciones[j], ang_1, ang_2)

                texto_centro_1 = f"Distancia al Centro del Casquillo de ID: {ids_balas[i]}"
                texto_centro_2 = f"Distancia al Centro del Casquillo de ID: {ids_balas[j]}"
                texto_centros[i] = texto_centro_1
                texto_centros[j] = texto_centro_2

                distancias_centro[i] = str(obj_bala.obtener_distancia_centro(centro, centro_c_1))
                distancias_centro[j] = str(obj_bala.obtener_distancia_centro(centro, centro_c_2))

                diferencia_centros_lista.append(str(diferencia_centros))
                porcentaje_diferencia_centros_list.append(porcentaje_dif)

                media_comparaciones = media_comparaciones + similitud
                



                similitud = str(similitud).split('.')[0] + '.' + str(similitud).split('.')[1][0:2] + ' %'

                similitudes.append(similitud)
                cantidad_pixeles_iguales.append(str(pixeles_iguales))
                cantidad_pixeles_totales.append(str(total_pixeles))
            
        
        media_comparaciones = media_comparaciones / cantidad_comparaciones
        
        cuerpo = {
            'textos' : comparaciones_dir,
            'similitudes' : similitudes,
            'pixeles_iguales' : cantidad_pixeles_iguales,
            'pixeles_totales' : cantidad_pixeles_totales,
            'diferencias_centros' : diferencia_centros_lista,
            'textos_dis_centros' : texto_centros,
            'distancias_centros' : distancias_centro,
            'porcentaje_dif_list' : porcentaje_diferencia_centros_list,
            'cantidad_comparaciones': cantidad_comparaciones,
            'media_comparaciones': str(media_comparaciones).split('.')[0] + '.' + str(media_comparaciones).split('.')[1][0:2] + ' %'
        }
        print("imprimiendo cuerpo")
        print("-*"*100)
        print(cuerpo)
        return jsonify(cuerpo), 200




# ------------------------------------- FIN FUNCIONES CASQUILLOS -----------------------------------------------------------------------------


# ------------------PDF'S

@perito_bp.route('/generar/pdf/caso/<id>', methods=['GET'])
@token_requerido
def generar_pdf(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    #balas_mostrar = ServiciosBala.obtener_todos()
    balas_caso = ServiciosCasquillo.obtener_por_caso(id)
    cantidad_indice = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cont=0
    print("dato_bala")
    print("helloda")
    #print(balas_mostrar)
    #for bala in balas_mostrar:
    #    print(bala['id_caso'])
    #    id_bala_g = int(bala['id_caso'])
    #    cont = cont + 1
    #    if id_bala_g==int(id):
    #        print(bala)
    #        print(id)
    #        balas_caso.append(bala)

    #datos_caso = ServiciosCaso.obtener_id(id)
    datos_caso = ServiciosCaso.obtener_por_id(id)
    id_experto = datos_caso['id_experto']
    #datos_experto = ServiciosExperto.obtener_id(id_experto)
    datos_experto = ServiciosUsuario.obtener_por_id(id_experto)
    id_usuario_experto = datos_experto['id_usuario']
    datos_usuario_experto = ServiciosUsuario.obtener_por_id(id_usuario_experto)
    datos_usuario_solicitante = ServiciosUsuario.obtener_por_id(id_usuario)

    respuesta = ServiciosCaso.generar_horizontal_pdf(datos_usuario_solicitante, datos_usuario_experto, datos_experto, datos_caso, balas_caso)
    print('-'*50)
    print('DEBUG')
    print(respuesta)
    print(len(respuesta.getvalue()))

    response = make_response(respuesta.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="informe_caso_{id}.pdf"'

    return response

from datetime import datetime

@perito_bp.route('/descargar/pdf/caso/<id>', methods=['GET'])
@token_requerido
def descargar_pdf(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    #balas_mostrar = ServiciosBala.obtener_todos()
    balas_caso = ServiciosCasquillo.obtener_por_caso(id)
    cantidad_indice = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cont=0
    print("dato_bala")
    print("helloda")
    #print(balas_mostrar)
    #for bala in balas_mostrar:
    #    print(bala['id_caso'])
    #    id_bala_g = int(bala['id_caso'])
    #    cont = cont + 1
    #    if id_bala_g==int(id):
    #        print(bala)
    #        print(id)
    #        balas_caso.append(bala)

    #datos_caso = ServiciosCaso.obtener_id(id)
    datos_caso = ServiciosCaso.obtener_por_id(id)
    id_experto = datos_caso['id_experto']
    #datos_experto = ServiciosExperto.obtener_id(id_experto)
    datos_experto = ServiciosUsuario.obtener_por_id(id_experto)
    id_usuario_experto = datos_experto['id_usuario']
    datos_usuario_experto = ServiciosUsuario.obtener_por_id(id_usuario_experto)
    datos_usuario_solicitante = ServiciosUsuario.obtener_por_id(id_usuario)

    respuesta = ServiciosCaso.generar_horizontal_pdf(datos_usuario_solicitante, datos_usuario_experto, datos_experto, datos_caso, balas_caso)
    print('-'*50)
    print('DEBUG')
    print(respuesta)
    print(len(respuesta.getvalue()))

    response = make_response(respuesta.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    filename_pdf = f"CASO_{datos_caso['rup']}_{fecha_actual}.pdf"
    response.headers['Content-Disposition'] = f'attachment; filename={filename_pdf}'

    return response


# ------------------------------------- VSITAS CASQUILLSO 

@perito_bp.route('/casquillos', methods=['GET'])
@token_requerido
def vista_casquillos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    casquillos = ServiciosCasquillo.obtener_por_experto(id_usuario)

    return render_template('perito/casquillos.html', datos=datos, casquillos=casquillos)
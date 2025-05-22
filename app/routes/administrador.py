from flask import Blueprint, request, jsonify, current_app, send_from_directory, send_file, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from app.services.serviciosAutenticacion import token_requerido
from app.services.serviciosUsuario import ServiciosUsuario
from app.services.serviciosCaso import ServiciosCaso
from app.services.serviciosCasquillo import ServiciosCasquillo
from app.services.ServiciosDashboard import ServiciosDashboard
import os

administrador_bp = Blueprint('administrador_bp', __name__)

@administrador_bp.route('/inicio', methods=['GET'])
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


    return render_template('administrador/inicio.html', datos=datos, datos_dashboard=datos_dashboard)

# -------------------------- LOGICA USUARIOS -------------------------------

@administrador_bp.route('/usuarios/agregar', methods=['POST'])
@token_requerido
def agregar_usuario(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

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
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    usuario_eliminado = ServiciosUsuario.habilitar(id, id_usuario)

    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_usuarios_totales'))
    
# ------------------------ FIN LOGICA USUARIOS ----------------------------

# ------------------- VISTAS USUARIOS ----------------------------------

@administrador_bp.route('/usuarios/totales', methods=['GET'])
@token_requerido
def vista_usuarios_totales(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    usuarios = ServiciosUsuario.obtener_todos()

    return render_template('administrador/usuarios.html', datos=datos, usuarios=usuarios)

@administrador_bp.route('/usuarios/administradores', methods=['GET'])
@token_requerido
def vista_usuarios_administradores(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    usuarios = ServiciosUsuario.obtener_administradores()

    return render_template('administrador/administradores.html', datos=datos, usuarios=usuarios)

@administrador_bp.route('/usuarios/peritos', methods=['GET'])
@token_requerido
def vista_usuarios_peritos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    usuarios = ServiciosUsuario.obtener_peritos()

    return render_template('administrador/peritos.html', datos=datos, usuarios=usuarios)


# ------------------- FIN VISTAS USUARIOS ----------------------------------

# ----------------------------- VISTAS CASOS ------------------------------------

@administrador_bp.route('/casos', methods=['GET'])
@token_requerido
def vista_casos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    peritos = ServiciosUsuario.obtener_peritos()
    casos = ServiciosCaso.obtener_todos()

    return render_template('administrador/casos.html', datos=datos, casos=casos, peritos=peritos)

@administrador_bp.route('/casos/ver/<id>', methods=['GET'])
@token_requerido
def vista_caso_id(datos_usuario, id):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    caso = ServiciosCaso.obtener_por_id(id)

    if not caso:

        referer = request.referrer
        if referer:
            return redirect(referer)
        else:
            # Si no hay referencia, rediriges a una página predeterminada
            return redirect(url_for('administrador_bp.vista_casos'))
    
    casquillos = ServiciosCasquillo.obtener_por_caso(id)

    return render_template('administrador/ver_caso.html', datos=datos, caso=caso, casquillos=casquillos)




# ----------------------------- FIN VISTAS CASOS ------------------------------------

# ------------------------------- FUNCIONES CASOS ------------------------------------

@administrador_bp.route('/casos/agregar', methods=['POST'])
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
                                     formulario['perito'],
                                     id_usuario)
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_casos'))

@administrador_bp.route('/casos/editar/<id>', methods=['POST'])
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
                                         formulario['perito'])
    
    referer = request.referrer
    if referer:
        return redirect(referer)
    else:
        # Si no hay referencia, rediriges a una página predeterminada
        return redirect(url_for('administrador_bp.vista_casos'))
    
@administrador_bp.route('/casos/eliminar/<id>', methods=['GET'])
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
        return redirect(url_for('administrador_bp.vista_casos'))

# ------------------------------- FIN FUNCIONES CASOS ------------------------------------



@administrador_bp.route('/generar/pdf/caso/<id>', methods=['GET'])
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



# ----------------- vista casquillso -----------------------------


@administrador_bp.route('/casquillos', methods=['GET'])
@token_requerido
def vista_casquillos(datos_usuario):
    id_usuario = datos_usuario['id_usuario']
    datos = ServiciosUsuario.obtener_por_id(id_usuario)
    datos['nombre'] = str(datos['nombres']).split(' ')[0]
    datos['apellido'] = str(datos['apellidos']).split(' ')[0]
    ServiciosUsuario.actualizar_ultima_conexion(id_usuario)

    casquillos = ServiciosCasquillo.obtener_todos()

    return render_template('administrador/casquillos.html', datos=datos, casquillos=casquillos)
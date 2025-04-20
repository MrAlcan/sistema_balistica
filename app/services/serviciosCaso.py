from app.models.caso import Caso
from app.models.usuario import Usuario
from app.models.casquillo import Casquillo
from app.config.extensiones import db
from app.serializer.serializadorUniversal import SerializadorUniversal

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import queue
from io import BytesIO
import os
from app.controllers.ProcesarBala import ProcesarBala

class ServiciosCaso():
    def crear(descripcion, departamento, rup, id_experto, id_creado):
        nuevo_caso = Caso(descripcion, departamento, rup, id_experto, id_creado)
        db.session.add(nuevo_caso)
        db.session.commit()
        return {'status': 'success'}
    
    def modificar(id_caso, id_modificado, descripcion=None, departamento=None, rup=None, id_experto=None):
        caso = Caso.query.get(id_caso)
        if not caso:
            return {'error': 'caso no encontrado'}


        if descripcion:
            caso.descripcion = descripcion
        if departamento:
            caso.departamento = departamento
        if rup:
            caso.rup = rup
        if id_experto:
            caso.id_experto = id_experto

        caso.id_usuario_modificado = id_modificado
        caso.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}
    
    def eliminar(id_caso, id_usuario):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso == id_caso).first()
        if not caso:
            return {'error': 'Caso no encontrado'}
        caso.activo = 0
        caso.id_usuario_modificado = id_usuario
        caso.fecha_modificado = datetime.now()
        db.session.commit()
        return {'status': 'success'}
    
    def obtener_por_id(id_caso):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso==id_caso).first()
        if not caso:
            return None
        
        id_experto = caso.id_experto
        experto = Usuario.query.get(id_experto)

        nombres_perito = experto.nombres + " " + experto.apellidos
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto', 'fecha_creado']
        respuesta = SerializadorUniversal.serializar_unico(caso, datos_requeridos)
        respuesta['perito'] = nombres_perito
        return respuesta
    
    def obtener_por_id_y_experto(id_caso, id_experto):
        caso = Caso.query.filter(Caso.activo==1, Caso.id_caso==id_caso, Caso.id_experto==id_experto).first()
        if not caso:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto', 'fecha_creado']
        respuesta = SerializadorUniversal.serializar_unico(caso, datos_requeridos)
        return respuesta
    
    def obtener_todos():
        casos = Caso.query.filter(Caso.activo==1).all()
        if not casos:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto', 'fecha_creado']
        respuesta = SerializadorUniversal.serializar_lista(casos, datos_requeridos)
        for resp in respuesta:
            id_experto = resp['id_experto']
            experto = Usuario.query.get(id_experto)
            nombres_perito = experto.nombres + " " + experto.apellidos
            resp['perito'] = nombres_perito

        return respuesta
    
    def obtener_por_experto(id_experto):
        casos = Caso.query.filter(Caso.activo==1, Caso.id_experto==id_experto).all()
        if not casos:
            return None
        
        datos_requeridos = ['id_caso', 'descripcion', 'departamento', 'rup', 'id_experto', 'fecha_creado']
        respuesta = SerializadorUniversal.serializar_lista(casos, datos_requeridos)

        for caso in respuesta:
            casquillos_dir = []

            casquillos = Casquillo.query.filter(Casquillo.activo==1, Casquillo.id_caso==caso['id_caso']).all()
            if casquillos:
                for casquillo in casquillos:
                    diccionario = {'id_casquillo': int(casquillo.id_casquillo),
                                   'direccion_imagen': str(casquillo.imagen_original)}
                    casquillos_dir.append(diccionario)
            
            caso['casquillos'] = casquillos_dir

        return respuesta
    
    def generar_horizontal_pdf(usuario_solicitante, usuario_experto, datos_experto, datos_caso, balas):

        nombre_usuario = str(usuario_solicitante['nombres'] + ' ' + usuario_solicitante['apellidos'])

        margin_left = 1.6 * inch
        margin_right = 1.4 * inch
        margin_top = 1.6 * inch  # Deja espacio para el carimbo
        margin_bottom = 1 * inch
        buffer = BytesIO()

        #pdf = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        pdf = SimpleDocTemplate(buffer, pagesize=landscape(letter), 
                            leftMargin=margin_left,
                            rightMargin=margin_right,
                            topMargin=margin_top,
                            bottomMargin=margin_bottom)
        #pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle('Titulo', fontSize=18, alignment=1, fontName="Helvetica-Bold", underline=True)
        estilo_subtitulo = ParagraphStyle('Subtitulo', fontSize=10, alignment=0)
        estilo_tabla_paragrah = ParagraphStyle('Normala', fontSize=12, alignment=1)
        estilo_datos = estilos['Normal']

        logo_direccion = os.path.join(os.getcwd(),'app', 'static', 'assets', 'images', 'logo.png')
        print(logo_direccion)

        imagen_logo = Image(logo_direccion, 1 * inch, 1 * inch)  # Ajustar el tamaño del logo



        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generado_por = Paragraph(f"<b>Generado por:</b> {nombre_usuario}<br/><b>Fecha de generación:</b> {fecha_actual}", estilo_subtitulo)

        datos_caso_experto = Table([[Paragraph(f"<b>RUP:</b> {datos_caso['rup']}", estilo_datos), Paragraph(f"<b>Operador:</b> {usuario_experto['nombres']} {usuario_experto['apellidos']}", estilo_datos)],
                                [Paragraph(f"<b>Descripcion del Caso:</b> {datos_caso['descripcion']}", estilo_datos), Paragraph(f"<b>Fecha:</b> {datos_caso['fecha_creado']}", estilo_datos)]], colWidths=[3.5*inch, 3.5*inch])

        '''datos_caso_experto.setStyle(TableStyle([('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                                            ('SPAN',(0,0),(2,0)),
                                            ('SPAN',(0,3),(2,3)),]))'''
        datos_caso_experto.setStyle(TableStyle([('ALIGNMENT', (0, 0), (-1, -1), 'LEFT')]))

        titulo = Paragraph("<u>KIPKA</u>", estilo_titulo)
        
        def add_header(canvas, doc):
            width, height = letter

            x = 0.2 * inch
            y = width - (0.2 * inch) - (1.2 * inch)
            radio_esquinas = 5

            canvas.setStrokeColorRGB(66/255, 70/255, 50/255)  # Color de borde (Azul)
            canvas.setFillColorRGB(66/255, 70/255, 50/255)  # Color de relleno (Verde)
            #canvas.rect(x, y, 1.2 * inch, 1.2 * inch, fill=1)
            canvas.roundRect(x, y, 1.2 * inch, 1.2 * inch, radio_esquinas, fill=1)

            x = 1.6 * inch
            y = width - (0.2*inch) - (0.3 * inch)

            canvas.roundRect(x, y, 9.2 * inch, 0.3 * inch, radio_esquinas, fill=1)

            '''x = 1.6 * inch
            y = width - (0.2*inch) - (0.3 * inch)
            canvas.setStrokeColorRGB(1, 1, 1)  # Color de borde (Azul)
            canvas.setFillColorRGB(1, 1, 1)  # Color de relleno (Verde)
            canvas.roundRect(x, y, 9.2 * inch, 0.3 * inch, radio_esquinas, fill=1)'''



            imagen_logo.drawOn(canvas, (0.3*inch), width - (0.3*inch) - imagen_logo.drawHeight)
           
            posicion_texto_x = (0.3*inch)
            posicion_texto_y = (0.3*inch)
            generado_por.wrapOn(canvas, width, height)
            generado_por.drawOn(canvas, posicion_texto_x, posicion_texto_y)

            posicion_texto_x = (1.2*inch)
            posicion_texto_y = width - (0.7*inch)
            titulo.wrapOn(canvas, width, height)
            titulo.drawOn(canvas, posicion_texto_x, posicion_texto_y)

            posicion_texto_x = (1.6*inch)
            posicion_texto_y = width - (1.5*inch)
            datos_caso_experto.wrapOn(canvas, width, height)
            datos_caso_experto.drawOn(canvas, posicion_texto_x, posicion_texto_y)




        obj_bala = ProcesarBala()
        # 1 pulgada = 72 puntos
        anchos_columnas = [72 * 0.5, 72 * 0.5, 72 * 1.25, 72 * 1.25, 72 * 1.25, 72 * 3]

        cabecera_balistica = [Paragraph("<b>INDUBITADA</b>", estilo_tabla_paragrah),Paragraph("<b>DUBITADA</b>", estilo_tabla_paragrah)]


        if balas:
            for bala in balas:
                
                #------------ obtener similitudes basado en angulos -------------------

            

                id_bala_actual = bala['id_casquillo']
                ang_1 = int(bala['angulo_rotacion'])
                centro_1 = str(bala['centro_contorno'])[1:-1]
                centro_1_x = int(centro_1.split(', ')[0])
                centro_1_y = int(centro_1.split(', ')[1])
                direccion_1 = "app/static"+str(bala['csv'])
                comparaciones_str = 'Comparacion Similituds \n Angulo Casquillo Actual: '+ str(ang_1)
                for bala_c in balas:
                    

                    id_bala_comparacion = bala_c['id_casquillo']
                    if str(id_bala_actual) != str(id_bala_comparacion):
                        
                        tabla_balistica = []
                        tabla_balistica.append(cabecera_balistica)

                        direccion_imagen_procesada = "app/static"+str(bala['imagen_procesada'])#os.path.join(os.getcwd(), str(bala['imagen_procesada']))
                        direccion_imagen_procesada_c = "app/static"+str(bala_c['imagen_procesada'])#os.path.join(os.getcwd(), str(bala_c['imagen_procesada']))

                        imagen_procesada = Image(direccion_imagen_procesada, 3.5 * inch, 3.5* inch)
                        imagen_procesada_c = Image(direccion_imagen_procesada_c, 3.5 * inch, 3.5* inch)

                        tabla_balistica.append([imagen_procesada, imagen_procesada_c])

                        
                        ang_2 = int(bala_c['angulo_rotacion'])
                        centro_2 = str(bala_c['centro_contorno'])[1:-1]
                        centro_2_x = int(centro_2.split(', ')[0])
                        centro_2_y = int(centro_2.split(', ')[1])
                        direccion_2 = "app/static"+str(bala_c['csv'])
                        similitud, pixeles_iguales, total_pixeles, centro, centro_c_1, centro_c_2, diferencia_centros, porcentaje_dif = obj_bala.obtener_similitud(direccion_1, direccion_2, ang_1, ang_2)

                        tabla_balistica.append([Paragraph(f"<b>Similitud de Forma: </b>{str(similitud).split('.')[0]}.{str(similitud).split('.')[1][0:2]} %<br /><b>Similitud Basada en los Centros de los Golpes: </b>{str(porcentaje_dif)}", estilo_tabla_paragrah),''])

                        tabla_final_balas = Table(tabla_balistica)

                        estilo_tabla_balas = TableStyle([

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('SPAN', (0, 2), (1, 2)),
                        ])

                        tabla_final_balas.setStyle(estilo_tabla_balas)

                        elementos.append(tabla_final_balas)
                        elementos.append(Spacer(1, 90))

                        

                        #comparaciones_str = comparaciones_str + f'\n----------------------------------------------------------\nComparación con Casquillo con ID: {str(id_bala_comparacion)}\nAngulo Casquillo ' + str(id_bala_comparacion) +': ' +str(ang_2) + '\nSimilitud: ' + str(similitud).split('.')[0]+'.'+str(similitud).split('.')[1][0:2]+'%\nSimilitud Basada en los Centros de los Golpes:\n' + str(porcentaje_dif)


                
                




        

        # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer


import cv2
import numpy as np
from ultralytics import YOLO
#import matplotlib.pyplot as plt
import os


class ProcesarBala():
    def __init__(self):
        self.valor = None
        ruta_modelo = os.path.join(os.getcwd(), 'app', 'controllers', 'best.pt')
        self.model = YOLO(ruta_modelo)
    
    '''def guardarContornos(self, contornos, ruta_contornos):
        with open(ruta_contornos, 'w') as f:
            for cnt in contornos:
                f.write(f"{cnt.flatten().tolist()}\n")'''

    '''def guardarContornos(self, contornos, ruta_contornos):
        with open(ruta_contornos, 'w') as f:
            for cnt in contornos:
                for point in cnt:
                    # Escribir los puntos como "x y" en cada línea
                    f.write(f"{point[0]} {point[1]}\n")
                f.write("\n")  # Línea en blanco para separar contornos'''

    def guardarContornos(self, contornos, ruta_contornos):
        with open(ruta_contornos, 'w') as f:
            for cnt in contornos:
                for point in cnt:
                    x, y = point[0]  # Acceder al punto (x, y)
                    f.write(f"{x} {y}\n")
                f.write("\n")  # Línea en blanco para separar contornos
    
    def obtenerContornos(self, ruta_contornos):
        contornos = []

        with open(ruta_contornos, 'r') as f:
            for linea in f:
                puntos = eval(linea.strip())
                contornos.append(np.array(puntos, dtype=np.int32).reshape((-1, 1, 2)))
        
        return contornos
    
    def procesar(self, ruta_imagen, ruta_imagen_destino, ruta_imagen_contornos, ruta_contornos):

        results = self.model.predict(ruta_imagen, imgsz=640, conf=0.8)
        annotated_img = results[0].plot()
        #cv2.imwrite(ruta_imagen_destino, annotated_img) # ORIGINAL DE LA FEHCA 27/02/2025




        img = cv2.imread(ruta_imagen)

        h, w = img.shape[:2]

        resultados = self.model(img)

        mask = np.zeros((h, w), dtype=np.uint8)

        clase_objetivo = 0
        umbral_confianza = 0.8

        for resultado in resultados:
            segmentaciones = resultado.masks
            detecciones = resultado.boxes

            for i, segmentacion in enumerate(segmentaciones):
                clase = int(detecciones.cls[i])
                confianza = detecciones.conf[i]

                if clase == clase_objetivo and confianza > umbral_confianza:
                    mask_segmentada = segmentaciones.data[i].cpu().numpy().astype(np.uint8)
                    mask_segmentada = cv2.resize(mask_segmentada, (w, h), interpolation=cv2.INTER_NEAREST)
                    mask = np.maximum(mask, mask_segmentada)

        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_img = np.zeros((h, w), dtype=np.uint8)

        #-------- BUSCANDO CENTRO CONTORNO --------------------
        momentos = cv2.moments(contornos[0])
    
        # Calcular el centroide (cx, cy) utilizando los momentos
        cx = int(momentos['m10'] / momentos['m00'])
        cy = int(momentos['m01'] / momentos['m00'])
        cv2.putText(contorno_img, "Centroide", (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
        cv2.circle(contorno_img, (cx, cy), 5, (255), -1)  # Dibuja un círculo verde en el centro
        centro = str([cx, cy])
        #-------- FIN BUSCANDO CENTRO CONTORNO --------------------

        cv2.drawContours(contorno_img, contornos, -1, (255), thickness=2)  # Color blanco, grosor 2
        cv2.imwrite(ruta_imagen_contornos, contorno_img)

        self.guardarContornos(contornos, ruta_contornos)

        # ---------------------- GUARDADO DE IMAGENES CON CONTORNO ROJO RELLENO VERDE CENTRO AZUL ---------------------------
        
        img_2 = cv2.imread(ruta_imagen)
        relleno_verde = np.zeros_like(img_2)
        cv2.drawContours(relleno_verde, contornos, -1, (0, 255, 0, 75), thickness=cv2.FILLED) 

        img_2 = cv2.add(img_2, relleno_verde)
        #cv2.drawContours(img_2, contornos, -1, (0, 255, 0), thickness=cv2.FILLED)
        cv2.drawContours(img_2, contornos, -1, (0, 0, 255), thickness=5)
        cv2.putText(img_2, "Centroide", (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.circle(img_2, (cx, cy), 5, (255, 0, 0), -1)
        cv2.imwrite(ruta_imagen_destino, img_2)

        # ---------------------- FIN GUARDADO DE IMAGENES CON CONTORNO ROJO RELLENO VERDE CENTRO AZUL ---------------------------

        return 200, centro
    

    '''def load_contours_from_txt(self, file_path):
        with open(file_path, 'r') as file:
            points = [tuple(map(float, line.strip().split())) for line in file]
        return np.array(points, dtype=np.float32)'''
    
    def load_contours_from_txt(self, file_path):
        contours = []
        current_contour = []

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        point = tuple(map(float, line.split()))
                        if len(point) == 2:  # Asegurarse de que sea un punto (x, y)
                            current_contour.append(point)
                    except ValueError:
                        print(f"Error parsing line: {line}")
                else:
                    if current_contour:  # Si hay puntos en el contorno actual
                        contours.append(np.array(current_contour, dtype=np.float32))
                        current_contour = []

            # Añadir el último contorno si existe
            if current_contour:
                contours.append(np.array(current_contour, dtype=np.float32))

        return contours

    def rotate_contour(self, contour, angle, center):
        #angle_rad = np.deg2rad(angle)

        '''if contour.shape[1] != 1:
            contour = contour[:, np.newaxis, :]'''
        if isinstance(contour, list):
            contour = np.array(contour, dtype=np.float32)
        
        # Asegurarse de que el contorno tenga la forma (N, 1, 2)
        if contour.ndim == 2:
            contour = contour[:, np.newaxis, :]
    
        # Rotar el contorno
        #rotated_contour = cv2.transform(contour, rotation_matrix)

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        #rotated_contour = cv2.transform(np.array([contour]), rotation_matrix) # ORIGINAL
        rotated_contour = cv2.transform(contour, rotation_matrix)
        return rotated_contour[0]

    def calculate_max_distance_from_center(self, contour, center):
        distances = np.linalg.norm(contour - np.array(center), axis=1)
        return np.max(distances)

    def create_circle_mask(self, image_size, radius):
        mask = np.zeros(image_size, dtype=np.uint8)
        center = (image_size[0] // 2, image_size[1] // 2)
        cv2.circle(mask, center, int(radius), 255, thickness=cv2.FILLED)
        return mask
    
    # Calculate similarity
    def calculate_similarity(self, image1, image2, mask, mask_cir):



        '''image1_masked = cv2.bitwise_and(image1, image1, mask=mask)
        image2_masked = cv2.bitwise_and(image2, image2, mask=mask)

        cv2.imwrite('image_mask_1.png', image1_masked)
        cv2.imwrite('image_mask_2.png', image2_masked)

        image1_masked = image1_masked[mask_cir]
        image2_masked = image2_masked[mask_cir]

        
        
        matching_pixels = np.sum(image1_masked == image2_masked)
        print('pixeles iguales, ', matching_pixels)
        total_pixels_in_circle = np.sum(mask == 255) # original
        #total_pixels_in_circle = np.sum(image1 == 255)
        #total_pixels_in_circle = 640*640
        print(' total_ pixeles en cirucli', total_pixels_in_circle)

        similarity_percentage = (matching_pixels / total_pixels_in_circle) * 100
        return similarity_percentage'''

        image1_masked = cv2.bitwise_and(image1, image1, mask=mask)
        image2_masked = cv2.bitwise_and(image2, image2, mask=mask)

        cv2.imwrite('image_mask_1.png', image1_masked)
        cv2.imwrite('image_mask_2.png', image2_masked)

        image1_masked = image1_masked[mask_cir]
        image2_masked = image2_masked[mask_cir]

        
        
        #matching_pixels = np.sum(image1_masked == image2_masked == 255)
        matching_pixels = np.sum((image1_masked == image2_masked) & (image1_masked == 255)) * 2
        print('pixeles iguales, ', matching_pixels)
        total_pixels_in_circle = np.sum(image1_masked == 255) + np.sum(image2_masked == 255) # original
        print(' total_ pixeles en cirucli', total_pixels_in_circle)

        similarity_percentage = (matching_pixels / total_pixels_in_circle) * 100
        return similarity_percentage, matching_pixels, total_pixels_in_circle
    
    def obtener_similitud(self, ruta_contorno_1, ruta_contorno_2, angulo_1, angulo_2):

        # Load and rotate contours
        contour1 = self.load_contours_from_txt(ruta_contorno_1)
        contour2 = self.load_contours_from_txt(ruta_contorno_2)
        #print(contour1)
        #print("forma del contorno --- -- -- -- --", contour1.shape)
        #print("forma del contorno --- -- -- -- --", contour2.shape)

        image_size = (640, 640)
        height = 640
        width = 640
        center = (image_size[0] // 2, image_size[1] // 2)

        angle1 = angulo_1  # Replace with the actual angle received from Flask
        angle2 = angulo_2  # Replace with the actual angle received from Flask

        rotated_contour1 = self.rotate_contour(contour1, angle1, center)
        rotated_contour2 = self.rotate_contour(contour2, angle2, center)

        # Calculate the radius of the circle based on the furthest point from the center
        radius1 = self.calculate_max_distance_from_center(rotated_contour1, center)
        radius2 = self.calculate_max_distance_from_center(rotated_contour2, center)
        circle_radius = max(radius1, radius2)

        momentos_1 = cv2.moments(rotated_contour1)
        # Calcular el centroide (cx, cy) utilizando los momentos
        cx_1 = int(momentos_1['m10'] / momentos_1['m00'])
        cy_1 = int(momentos_1['m01'] / momentos_1['m00'])
        centro_c_1 = (cx_1, cy_1)

        momentos_2 = cv2.moments(rotated_contour2)
        # Calcular el centroide (cx, cy) utilizando los momentos
        cx_2 = int(momentos_2['m10'] / momentos_2['m00'])
        cy_2 = int(momentos_2['m01'] / momentos_2['m00'])
        centro_c_2 = (cx_2, cy_2)

        print("circulo radio, ", circle_radius)

        Y, X = np.ogrid[:height, :width]
        center_y, center_x = height // 2, width // 2
        mask_cir = (X - center_x) ** 2 + (Y - center_y) ** 2 <= circle_radius ** 2  # Máscara circular

        # Create the mask using the calculated radius
        mask = self.create_circle_mask(image_size, circle_radius)

        # Create binary images of the rotated contours
        binary_image1 = np.zeros(image_size, dtype=np.uint8)
        binary_image2 = np.zeros(image_size, dtype=np.uint8)
        cv2.drawContours(binary_image1, [rotated_contour1.astype(np.int32)], -1, 255, thickness=cv2.FILLED)
        cv2.drawContours(binary_image2, [rotated_contour2.astype(np.int32)], -1, 255, thickness=cv2.FILLED)

        cv2.imwrite('jajas_1.png', binary_image1)
        cv2.imwrite('jajas_2.png', binary_image2)
        cv2.imwrite('mask.png', mask)

        diferencia_centros, porcentaje_distancia = self.obtener_similitud_centro_contorno_imagen(center, centro_c_1, centro_c_2)

        

        

        similarity_percentage, matching_pixels, total_pixels_in_circle = self.calculate_similarity(binary_image1, binary_image2, mask, mask_cir)
        print(f'Similarity: {similarity_percentage:.2f}%')
        return similarity_percentage, matching_pixels, total_pixels_in_circle, center, centro_c_1, centro_c_2, diferencia_centros, porcentaje_distancia
    
    def obtener_distancia_centro(self, centro, centro_contorno):
        return np.linalg.norm(np.array(centro) - np.array(centro_contorno))
    
    def obtener_similitud_centro_contorno_imagen(self, centro, centro_c_1, centro_c_2):

        distancia_1 = self.obtener_distancia_centro(centro, centro_c_1)
        distancia_2 = self.obtener_distancia_centro(centro, centro_c_2)

        distancia_contornos = self.obtener_distancia_centro(centro_c_1, centro_c_2)

        porcentaje_distancia = distancia_contornos / (distancia_1 + distancia_2)

        if porcentaje_distancia > 1.0:
            porcentaje_distancia = 1.0
        

        porcentaje_distancia = 1.0 - porcentaje_distancia

        porcentaje_distancia = porcentaje_distancia * 100

        s_porcentaje = f'porcentaje {porcentaje_distancia:.2f}%'

        porcentaje_distancia = s_porcentaje.split(' ')[1]

        return distancia_contornos, porcentaje_distancia


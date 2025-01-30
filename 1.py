import cv2
import numpy as np

def count_words(image_path):
    # Cargar la imagen
    image = cv2.imread(image_path)
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar umbralización
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos para detectar palabras
    word_count = 0
    min_area = 50  # Ajustar según tamaño del texto
    max_area = 5000
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            word_count += 1
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    
    # Mostrar resultado
    cv2.imshow('Detected Words', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return word_count

# Ejemplo de uso
image_path = '1.png'  # Reemplazar con la ruta de la imagen
total_words = count_words(image_path)
print(f'Palabras detectadas: {total_words}')

import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime

# Crear base de datos
ruta = 'Empleados'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

print(nombres_empleados)

# Codificar imágenes
def codificar(imagenes):
    # Crear una lista nueva
    lista_codificada = []
    # Pasar todas las imágenes a RGB
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        # Codificar
        codificado = fr.face_encodings(imagen)[0]
        # Agregar a la lista
        lista_codificada.append(codificado)
    # Devolver lista codificada
    return lista_codificada

# Registrar los ingresos
def registrar_ingresos(persona):
    with open('registro.csv', 'a') as f:
        lista_datos = f.readlines()
        nombres_registro = [linea.split(',')[0] for linea in lista_datos]

        if persona not in nombres_registro:
            ahora = datetime.now()
            string_ahora = ahora.strftime('%H:%M:%S')
            f.write(f'{persona}, {string_ahora}\n')

lista_empleados_codificada = codificar(mis_imagenes)

# Tomar una imagen de la cámara web
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Leer imagen de la cámara
exito, imagen = captura.read()

if not exito:
    print("No se ha podido tomar la captura")
else:
    # Reconocer cara en captura
    cara_captura = fr.face_locations(imagen)

    # Codificar cara capturada
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

    # Buscar coincidencias
    for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificada, caracodif)
        distancias = fr.face_distance(lista_empleados_codificada, caracodif)
        print(distancias)


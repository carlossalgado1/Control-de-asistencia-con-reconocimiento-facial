import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime

# === Crear base de datos ===
ruta = 'Empleados'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

print("Empleados encontrados:", nombres_empleados)

# === Codificar imágenes ===
def codificar(imagenes):
    lista_codificada = []
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        codificado = fr.face_encodings(imagen)[0]
        lista_codificada.append(codificado)
    return lista_codificada

# === Registrar los ingresos ===
def registrar_ingresos(persona):
    with open('registro.csv', 'a+') as f:
        f.seek(0)
        lista_datos = f.readlines()
        nombres_registro = [linea.split(',')[0].strip() for linea in lista_datos]

        if persona not in nombres_registro:
            ahora = datetime.now()
            string_ahora = ahora.strftime('%H:%M:%S')
            f.write(f'{persona}, {string_ahora}\n')
            print(f"[✔] Registrado: {persona} a las {string_ahora}")
        else:
            print(f"[ℹ] {persona} ya fue registrado.")

# === Codificar empleados ===
lista_empleados_codificada = codificar(mis_imagenes)

# === Captura segura ===
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

try:
    while True:
        exito, imagen = captura.read()
        if not exito:
            print("[✖] Error al acceder a la cámara.")
            break

        imagen_chica = cv2.resize(imagen, (0, 0), fx=0.5, fy=0.5)
        imagen_rgb = cv2.cvtColor(imagen_chica, cv2.COLOR_BGR2RGB)

        caras = fr.face_locations(imagen_rgb)
        caras_codificadas = fr.face_encodings(imagen_rgb, caras)

        for codif, ubicacion in zip(caras_codificadas, caras):
            coincidencias = fr.compare_faces(lista_empleados_codificada, codif)
            distancias = fr.face_distance(lista_empleados_codificada, codif)

            if len(distancias) > 0:
                indice = numpy.argmin(distancias)

                if coincidencias[indice]:
                    nombre = nombres_empleados[indice]
                    y1, x2, y2, x1 = ubicacion
                    y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2  # porque usamos imagen_chica

                    cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(imagen, nombre, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    registrar_ingresos(nombre)

        cv2.imshow("Reconocimiento Facial", imagen)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[ℹ] Se presionó 'q'. Cerrando...")
            break

except Exception as e:
    print("[⚠] Ocurrió un error:", e)

finally:
    captura.release()
    cv2.destroyAllWindows()
    print("[✔] Cámara liberada y ventanas cerradas.")

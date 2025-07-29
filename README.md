# Asistencia - Sistema de Registro de Asistencia por Reconocimiento Facial

Este proyecto utiliza **OpenCV** y **Face Recognition** para crear un sistema simple de registro de asistencia mediante reconocimiento facial. Las caras de los empleados se registran previamente, y el sistema identifica y registra la hora de entrada cuando un empleado aparece frente a la cámara.

---

## Requisitos

- Python 3.6 o superior  
- OpenCV  
- face_recognition  
- numpy  

---

## Instalación

1. Clona el repositorio:  
   `git clone https://github.com/carlossalgado1/Control-de-asistencia-con-reconocimiento-facial.git`

2. Entra al directorio del proyecto:  
   `cd Control-de-asistencia-con-reconocimiento-facial`

3. Crea y activa un entorno virtual (opcional pero recomendado):  
   ```bash
   python -m venv env
   source env/bin/activate    # Linux/Mac
   .\env\Scripts\activate     # Windows
Instala las dependencias:
pip install -r requirements.txt

Modo de uso
Prepara una carpeta llamada Empleados dentro del directorio del proyecto, con imágenes de los empleados. Cada archivo debe llamarse con el nombre del empleado, por ejemplo juan.jpg, maria.png, etc.

Ejecuta el script principal:
python asistencia.py

Se activará la cámara web y comenzará a detectar y reconocer las caras. Si se reconoce a un empleado, se mostrará su nombre en la pantalla y se registrará su hora de entrada en el archivo registro.csv.

Para salir, presiona la tecla q.

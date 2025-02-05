from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
from datetime import datetime
from exceptions import APIError, handle_generic_exception, handle_404_error, handle_api_error
import threading
from apinews import obtener_noticias_ciberseguridad, guardar_noticias_y_limpiar
import glob
import time

app = Flask(__name__)

# Registrar manejadores de excepciones en la aplicación
app.register_error_handler(404, handle_404_error)
app.register_error_handler(Exception, handle_generic_exception)
app.register_error_handler(APIError, handle_api_error)

# Intervalo en minutos para actualizar las noticias
INTERVALO_ACTUALIZACION = 240  # Puedes modificarlo según tu necesidad

def actualizar_noticias_periodicamente():
    """Función que actualiza las noticias periódicamente en segundo plano."""
    while True:
        try:
            print(f"[{datetime.now()}] Iniciando actualización de noticias...")
            noticias = obtener_noticias_ciberseguridad()
            if noticias:
                guardar_noticias_y_limpiar(noticias)
                print(f"[{datetime.now()}] Noticias actualizadas correctamente.")
            else:
                print(f"[{datetime.now()}] No se encontraron noticias nuevas.")
        except Exception as e:
            print(f"[{datetime.now()}] Error en la actualización de noticias: {e}")
        
        # Esperar el intervalo antes de la próxima actualización
        time.sleep(INTERVALO_ACTUALIZACION * 60)

@app.route('/')
def mostrar_noticias():
    """Carga y muestra las noticias desde el archivo JSON más reciente."""
    archivo_json = None
    archivos_json = glob.glob("noticias_ciberseguridad_*.json")

    if archivos_json:
        archivo_json = max(archivos_json, key=os.path.getctime)

    noticias = []
    if archivo_json:
        try:
            with open(archivo_json, "r") as f:
                noticias = json.load(f)
        except json.JSONDecodeError as e:
            raise APIError(f"Error al decodificar el archivo JSON: {e}", 500)
        except Exception as e:
            raise APIError(f"Error al leer el archivo de noticias: {str(e)}", 500)

    return render_template('noticias.html', noticias=noticias)

@app.route('/ads.txt')
def ads_txt():
    """Devuelve el archivo ads.txt desde la carpeta estática."""
    return send_from_directory('static', 'ads.txt')

# Iniciar el hilo de actualización de noticias en segundo plano
hilo_noticias = threading.Thread(target=actualizar_noticias_periodicamente, daemon=True)
hilo_noticias.start()

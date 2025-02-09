from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import threading
import time
import logging
from datetime import datetime
import glob
from exceptions import APIError, handle_generic_exception, handle_404_error, handle_api_error
from apinews import obtener_noticias_ciberseguridad, guardar_noticias_y_limpiar
import requests

# Configurar logging en lugar de print()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# Registrar manejadores de errores
app.register_error_handler(404, handle_404_error)
app.register_error_handler(Exception, handle_generic_exception)
app.register_error_handler(APIError, handle_api_error)

# Intervalo en minutos para actualizar las noticias
INTERVALO_ACTUALIZACION = 240  

# Evento para controlar el hilo
evento_parar = threading.Event()

def actualizar_noticias_periodicamente():
    """Actualiza noticias en segundo plano cada INTERVALO_ACTUALIZACION minutos."""
    while not evento_parar.is_set():
        try:
            logging.info("Iniciando actualización de noticias...")
            noticias = obtener_noticias_ciberseguridad()
            if noticias:
                guardar_noticias_y_limpiar(noticias)
                logging.info("Noticias actualizadas correctamente.")
            else:
                logging.warning("No se encontraron noticias nuevas.")
        except Exception as e:
            logging.error(f"Error en la actualización de noticias: {e}")
        
        # Esperar el intervalo antes de la próxima actualización
        evento_parar.wait(INTERVALO_ACTUALIZACION * 60)

@app.route('/')
def mostrar_noticias():
    """Carga y muestra las noticias desde el archivo JSON más reciente."""
    archivos_json = glob.glob("noticias_ciberseguridad_*.json")
    if not archivos_json:
        return render_template('noticias.html', noticias=[])

    archivo_json = max(archivos_json, key=os.path.getctime)

    try:
        with open(archivo_json, "r", encoding="utf-8") as f:
            noticias = json.load(f)
    except json.JSONDecodeError as e:
        raise APIError(f"Error al decodificar el archivo JSON: {e}", 500)
    except Exception as e:
        raise APIError(f"Error al leer el archivo de noticias: {str(e)}", 500)

    return render_template('noticias.html', noticias=noticias)
    """esto es un comentario"""

@app.route('/ads.txt')
def ads_txt():
    """Devuelve el archivo ads.txt desde la carpeta estática."""
    return send_from_directory('static', 'ads.txt')

# Iniciar el hilo de actualización de noticias en segundo plano
hilo_noticias = threading.Thread(target=actualizar_noticias_periodicamente, daemon=True)
hilo_noticias.start()

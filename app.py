from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
from datetime import datetime
from exceptions import APIError, handle_generic_exception, handle_404_error, handle_api_error
import threading
from apinews import obtener_noticias_ciberseguridad, guardar_noticias_y_limpiar
import glob


app = Flask(__name__)

# Registrar manejadores de excepciones en la aplicación
app.register_error_handler(404, handle_404_error)  # Error 404
app.register_error_handler(Exception, handle_generic_exception)  # Manejador de excepciones generales
app.register_error_handler(APIError, handle_api_error)  # Manejador de excepciones de API

# Intervalo en minutos para actualizar las noticias
INTERVALO_ACTUALIZACION = 360  # Cambia este valor según tu necesidad

# Función para actualizar noticias periódicamente
def actualizar_noticias_periodicamente():
    try:
        print("Iniciando actualización de noticias...")
        noticias = obtener_noticias_ciberseguridad()
        if noticias:
            guardar_noticias_y_limpiar(noticias)
            print("Noticias actualizadas y guardadas correctamente.")
        else:
            print("No se obtuvieron noticias para actualizar.")
    except Exception as e:
        print(f"Error en la actualización de noticias: {e}")
    finally:
        # Reprogramar el temporizador para el siguiente ciclo
        threading.Timer(INTERVALO_ACTUALIZACION * 60, actualizar_noticias_periodicamente).start()

@app.route('/')
def mostrar_noticias():
    # Buscar el archivo JSON más reciente
    archivo_json = None
    archivos_json = glob.glob("noticias_ciberseguridad_*.json")

    if archivos_json:
        # Seleccionar el archivo más reciente basado en el nombre
        archivo_json = max(archivos_json, key=os.path.getctime)
    
    noticias = []
    if archivo_json:
        try:
            with open(archivo_json, "r") as f:
                noticias = json.load(f)
        except json.JSONDecodeError as e:
            # Error si el archivo JSON está malformado
            raise APIError(f"Error al decodificar el archivo JSON: {e}", 500)
        except Exception as e:
            # Captura cualquier otra excepción relacionada con el manejo de archivos
            raise APIError(f"Error al leer el archivo de noticias: {str(e)}", 500)

    # Renderizar la plantilla HTML y pasar las noticias como contexto
    return render_template('noticias.html', noticias=noticias)

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

if __name__ == "__main__":
    # Iniciar la actualización periódica de noticias
    actualizar_noticias_periodicamente()
    # Ejecutar la aplicación Flask
    app.run(host='0.0.0.0', port=5000, debug=True)

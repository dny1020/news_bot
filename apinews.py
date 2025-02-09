from newsapi import NewsApiClient
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()
# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Obtener API Key desde variable de entorno

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError("API Key no encontrada. Asegúrate de definir 'NEWS_API_KEY' en el entorno.")

newsapi = NewsApiClient(api_key=API_KEY)

def obtener_contenido_completo(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        articulo = soup.find('article') or soup.find('div', class_='content') or soup.find('body')
        
        return articulo.text.strip() if articulo else "No se pudo extraer el contenido."
    except Exception as e:
        return f"Error al obtener contenido: {e}"

def obtener_noticias_ciberseguridad():
    try:
        all_articles = newsapi.get_everything(q='ciberseguridad OR ciberdelincuencia OR cibercriminales OR ciberdelito OR cibercrimen',
                language='es',
                sort_by='publishedAt',
                page_size=10)
        
        noticias = []
        if all_articles["status"] == "ok" and "articles" in all_articles:
            for articulo in all_articles["articles"]:
                url = articulo.get("url", "")
                contenido_completo = obtener_contenido_completo(url) if url else "No disponible"
                
                noticia = {
                    "titulo": articulo.get("title", "Sin título"),
                    "descripcion": articulo.get("description", "No hay descripción"),
                    "url": url,
                    "fecha_publicacion": articulo.get("publishedAt", "Fecha desconocida"),
                    "urlToImage": articulo.get("urlToImage", ""),
                    "contenido": contenido_completo
                }
                noticias.append(noticia)
        return noticias
    except Exception as e:
        print(f"Error al obtener las noticias: {e}")
        return []

def guardar_noticias_y_limpiar(noticias):
    try:
        nombre_archivo = f"noticias_ciberseguridad_{datetime.now().strftime('%Y-%m-%d')}.json"

        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(noticias, f, indent=4, ensure_ascii=False)

        for archivo in os.listdir():
            if archivo.endswith(".json") and archivo != nombre_archivo:
                try:
                    os.remove(archivo)
                    print(f"Archivo antiguo eliminado: {archivo}")
                except Exception as e:
                    print(f"No se pudo eliminar el archivo {archivo}: {e}")

        print(f"Noticias guardadas exitosamente en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar las noticias o limpiar archivos antiguos: {e}")

if __name__ == "__main__":
    print("Obteniendo noticias sobre ciberseguridad...")
    noticias = obtener_noticias_ciberseguridad()
    if noticias:
        guardar_noticias_y_limpiar(noticias)
    else:
        print("No se obtuvieron noticias.")
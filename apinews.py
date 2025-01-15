from newsapi import NewsApiClient
import json
from datetime import datetime
import os  # Importación necesaria para manipular el sistema de archivos

# Inicia el cliente de NewsAPI con tu API Key
newsapi = NewsApiClient(api_key='28c84e3930594befa1aeaff6b9d58d73')

# Función para obtener noticias sobre ciberseguridad
def obtener_noticias_ciberseguridad():
    try:

        all_articles = newsapi.get_everything(q='ciberseguridad OR ciberdelincuencia OR cibercriminales OR ciberdelito OR cibercrimen',
                language='es',
                sort_by='publishedAt',
                page_size=100)
        
    
        # Procesar las noticias obtenidass
        noticias = []
        if all_articles["status"] == "ok" and "articles" in all_articles:
            for articulo in all_articles["articles"]:
                noticia = {
                    "titulo": articulo.get("title", "Sin título"),
                    "descripcion": articulo.get("description", "No hay descripción"),
                    "url": articulo.get("url", ""),
                    "fecha_publicacion": articulo.get("publishedAt", "Fecha desconocida"),
                    "urlToImage": articulo.get("urlToImage", "")  # URL de la imagen, si existe
                }
                noticias.append(noticia)
        return noticias
    except Exception as e:
        print(f"Error al obtener las noticias: {e}")
        return []

# Función para guardar las noticias y eliminar otros archivos .json
def guardar_noticias_y_limpiar(noticias):
    try:
        # Crear nombre del archivo JSON basado en la fecha actual
        nombre_archivo = f"noticias_ciberseguridad_{datetime.now().strftime('%Y-%m-%d')}.json"

        # Guardar las noticias en el archivo JSON
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(noticias, f, indent=4, ensure_ascii=False)

        # Eliminar otros archivos .json en el directorio actual
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

# Función principal
if __name__ == "__main__":
    print("Obteniendo noticias sobre ciberseguridad...")
    
    # Obtener las noticias
    noticias = obtener_noticias_ciberseguridad()

    # Guardar las noticias si se obtuvieron correctamente
    if noticias:
        guardar_noticias_y_limpiar(noticias)
    else:
        print("No se obtuvieron noticias.")

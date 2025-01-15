# Usa una imagen base de Python
FROM python:3.9-slim-bullseye
 
# Establece el directorio de trabajo en el contenedor
WORKDIR /app
 
# Copia solo el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .
 
# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 
# Copia el resto de los archivos del proyecto al contenedor
COPY . .
 
# Expone el puerto en el que corre Flask
EXPOSE 80
 
# Comando para correr la app
CMD ["python", "app.py"]
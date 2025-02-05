# Imagen base de Python
FROM python:3.9-slim-bullseye

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 
# Exponer el puerto interno de Flask
EXPOSE 5000

# Comando para ejecutar Flask
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

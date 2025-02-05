#informacion imortante
📦 newsbot
 ┣ 📂 static/                # Archivos estáticos (CSS, JS, imágenes)
 ┣ 📂 templates/             # Plantillas HTML para la web
 ┣ 📂 nginx-proxy-manager/   # Configuración de proxy inverso (si se usa)
 ┣ 📜 apinews.py             # Script para obtener noticias
 ┣ 📜 app.py                 # Aplicación Flask
 ┣ 📜 exceptions.py          # Manejador de errores personalizados
 ┣ 📜 requirements.txt       # Dependencias de Python
 ┣ 📜 Dockerfile             # Configuración para Docker
 ┣ 📜 docker-compose.yaml    # Archivo de configuración para Docker Compose
 ┣ 📜 .dockerignore          # Archivos ignorados en Docker
 ┣ 📜 .gitignore             # Archivos ignorados en Git
 ┗ 📜 README.md              # Documentación


🚀 Instalación y Configuración

📌 Requisitos
Antes de comenzar, asegúrate de tener instalado:

Python 3.x
pip (administrador de paquetes de Python)
Docker y Docker Compose (opcional, para despliegue en contenedores)
Gunicorn (para producción)
🔧 Instalación Manual (Sin Docker)
1️⃣ Clona este repositorio:

git clone https://github.com/tuusuario/newsbot.git
cd newsbot
2️⃣ Crea un entorno virtual e instala las dependencias:

python3 -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Ejecuta la aplicación:

gunicorn -w 4 -b 0.0.0.0:8000 app:app
Luego, accede a http://localhost:8000/ en tu navegador.

🐳 Despliegue con Docker
1️⃣ Construye la imagen Docker:

docker build -t newsbot .
2️⃣ Ejecuta el contenedor:

docker run -d -p 8000:8000 --name newsbot newsbot
Si usas Docker Compose, ejecuta:

docker-compose up -d
🛠️ Configuración

El archivo apinews.py obtiene y guarda las noticias.
Las noticias se actualizan automáticamente cada 360 minutos (6 horas).
Puedes cambiar este valor en app.py modificando INTERVALO_ACTUALIZACION.
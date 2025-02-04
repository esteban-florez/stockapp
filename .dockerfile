FROM python:3.9

# Instala las dependencias del sistema (WeasyPrint)
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev

# Crea el directorio de la aplicación
WORKDIR /app

# Copia los archivos de tu aplicación
COPY . /app

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Ejecuta los comandos de build.sh (adaptados)
RUN python3 manage.py makemigrations --noinput
RUN python3 manage.py migrate --noinput
RUN python3 manage.py seed --noinput  # Si tienes un script de seed
RUN python3 manage.py collectstatic --noinput

# Configura WeasyPrint para usar las fuentes del sistema
ENV WEASYPRINT_FONTS_PATH /usr/share/fonts

# Comando para iniciar Gunicorn (adaptado para Docker)
CMD gunicorn stockapp.wsgi:application --bind 0.0.0.0:8080

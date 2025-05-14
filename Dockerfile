# Imagen base
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Exponer el puerto en el que correrá Django (ej: usando runserver)
EXPOSE 5000

# Comando por defecto para ejecutar la app (modo desarrollo)
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]

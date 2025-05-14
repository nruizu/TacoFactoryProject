# Imagen base
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]

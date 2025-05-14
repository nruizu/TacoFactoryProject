# Imagen base ligera de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo la carpeta que contiene el código
COPY Taller02 /app/Taller02

# Instalar Flask
RUN pip install flask

# Exponer el puerto en el que corre Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "Taller02/main.py"]
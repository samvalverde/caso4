# Usa una imagen base de Python
FROM python:3.12

# Variables de entorno para la base de datos MongoDB
ENV DB_HOST_MONGO=mongo
ENV DB_PORT_MONGO=27017
ENV DB_USER_MONGO=root
ENV DB_PASSWORD_MONGO=password

# Variables de entorno para redis
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0

# Establece el directorio de trabajo
WORKDIR /opt/app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para iniciar la aplicación Flask
CMD ["poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"]
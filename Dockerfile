# Utiliza una imagen base de Python
FROM python:3.8.3

# Establece el directiorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del archivo requirements.txt
RUN pip install -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo
COPY . .

# expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar tu aplicación Flask
CMD ["python", "app.py"]

# Usamos una base ligera de Python
FROM python:3.11-slim

# Evitamos que Python genere basura (.pyc) y habilitamos logs fluidos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalamos dependencias primero para aprovechar el cache de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el cerebro, el guardián y la memoria
COPY . .

# Exponemos el puerto de la interfaz WebView (Flask)
EXPOSE 5000

# Iniciamos el Agente Servidor (Escuchador de tareas y Patrullaje)
CMD ["python", "agente_servidor.py"]

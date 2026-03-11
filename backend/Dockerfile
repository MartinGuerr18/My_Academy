# Equivalente a tu package.json en Node — define el ambiente
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala dependencias primero (optimiza caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Puerto que expone Django (equivalente a ng serve en el 4200)
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
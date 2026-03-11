# My Academy

## Requisitos
- Docker Desktop
- Git

## Instalación

1. Clonar el repositorio
2. Crear el archivo `.env` en la raíz con este contenido:
```
DB_NAME=myacademy_db
DB_USER=myacademy_user
DB_PASSWORD=myacademy_pass
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-cambia-esto-en-produccion-xyz123
DEBUG=True
```
3. Levantar los contenedores:
```
docker-compose up --build
```
4. Correr migraciones:
```
docker-compose exec web python manage.py migrate
```
5. Entrar a http://localhost:8000/login/

## Ramas
- `main` → código estable
- `dev` → integración
- `feature/tu-nombre` → desarrollo individual
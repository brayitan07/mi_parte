# Django Starter

Plantilla base para proyectos Django.

## 1. Clonar el proyecto

```bash
git clone <url-del-repositorio>
cd mi_parte
```

## 2. Crear entorno virtual

```bash
python -m venv env
```

## 3. Activar entorno virtual

### Windows

```bash
env\Scripts\activate
```

### Linux / Mac

```bash
source env/bin/activate
```

## 4. Instalar dependencias

Si existe el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install django
pip install django-allauth
pip install PyJWT
pip install cryptography
pip install django-embed-video
pip install pillow
pip install reportlab
pip install openpyxl
```

## 5. Crear migraciones

```bash
python manage.py makemigrations
```

## 6. Aplicar migraciones

```bash
python manage.py migrate
```

## 7. Crear superusuario

```bash
python manage.py createsuperuser
```

## 8. Ejecutar servidor

```bash
python manage.py runserver
```

Abrir en el navegador:

```text
http://127.0.0.1:8000/
```

## Dependencias utilizadas

- Django
- django-allauth
- django-embed-video
- Pillow
- ReportLab
- OpenPyXL

## Generar requirements.txt

Después de instalar todas las librerías:

```bash
pip freeze > requirements.txt
```

## Actualizar requirements.txt

Cada vez que instales una nueva librería:

```bash
pip freeze > requirements.txt
```

## Reporte de notas (Excel y PDF)

Para que funcionen los reportes:

```bash
pip install reportlab openpyxl
```

o

```bash
pip install -r requirements.txt
```
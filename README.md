# Proyecto Ingenieria de Software

### Crear ambiente virtual
```
python -m venv env
```

### Activar el ambiente virtual
```
.\env\Scripts\activate
```
o
```
.\env\Scripts\Activate.ps1 
```

### Instalar dependencias. 

```
pip install -r requirements.txt
```

### Crear archivo para manejo de secretos y variables de entorno

Crear un archivo __.env__ y pegar lo siguiente reemplzando lo necesario. 
```
DATABASE_NAME=nombre_base_datos
DATABASE_USER=usuario_postgres
DATABASE_PASSWORD=contraseña
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Crear proyecto en Django

```
django-admin startproject proyectois
```

```
cd proyectois
```

### Crear una Aplicacion en django

```
python manage.py startapp evapp
```

### Configurar Base de datos

```
python manage.py migrate
```
La siguiente no!
```
python manage.py inspectdb > evapp/models.py
```

### Creación del Superusuario

```
python manage.py createsuperuser
```

### Ejecutar la Aplicación

```
python manage.py runserver
```
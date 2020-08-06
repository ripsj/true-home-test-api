Boilerplate (Django, AWS S3, Lambda)
========================================

> Framework [Django 2.2](https://docs.djangoproject.com/en/2.2/)

## Documentación

* [Acerca](#acerca)
* [Requisitos](#requisitos)
* [Estructura del Proyecto](#estructura-del-proyecto)
* [Instalación](#instalacion)
    - [Instalación Local](#local)
* [Crear una nueva app](#crear-una-nueva-app)
* [Deploy AWS Lambda](#deploy-aws-lambda)
* [Variables de entorno](#variables-de-entorno)
* [Postman](#postman)
* [Referencias](#referencias)

## Acerca

Template inicial con las funcionalidades básicas para el desarrollo de un proyecto basado en el Framework Django, utilizando tecnologias propias de AWS; Lambda, RDS, S3, API Gateway, CloudWatch.

El proyecto incluye el uso de zappa para el despligue en un entorno serverless, si quire saber un poco más de zappa consulte la documentación en su sitio oficial.

## Requisitos

- virtualenv
- Python 3
- pip
- (PostgreSQL) 9.5.15

## Estructura del proyecto
> Esta es la estructura básica del boilerplate.

```
boilerplate/
    venv/
        ... source files

    project/
        __init__.py
        urls.py
        wsgi.py
        settings.py

     apps/
         examples/
         security/
         ... more apps add here

    core/
         management/
             commands/
                 renameproject.py

         __init__.py
         applist.py
         internationalization.py
         mediafiles.py

     templates/
         email/
             base.html
             demo.html
             recover-password.html
             welcome-app.html

     .env.sample
     zappa_settings.json
     manage.py
     requeriments.txt
     super-secret-config.sample.json

```
## Instalación
> Se deben instalar los requisitos mencionados anteriormente.
> En caso que la instalación de los paquetes falle, tomarse en cuenta el siguiente paquete

```
Ubuntu
sudo apt-get install libpq-dev python-dev
pip install setuptools

```

```
# Descargar o Clonar
$ https://bitbucket.org/dacodes/django-rest-boilerplate/src/master/
```

## Deploy Local
#### Maquina virtual o localhost
> Las configuraciones pueden variar dependiendo del sistema operativo

#### Interactivo
```
# Asigna permisos al instalador
$ chmod +x installer.sh

# Inicia el instalador
$ bash installer.sh
```

#### Manual

```
# Crea un entorno virtual
$ virtualenv -p python3 venv

# Activa el entorno
$ source venv/bin/activate

# Variables locales
$ cp .env.sample .env

# Modificar variables necesarias
$ nano .env

# Instala los requerimientos
$ pip install -r requeriments.txt
```


## Deploy AWS Lambda en un entorno local
#### Lambda Serverless (usando zappa)
> Es necesario acceder a la consola de IAM de la cuenta de AWS y configurar un Grupo/Usuario para generar un Access key ID y un Secret access key.
> Debe otorgar los permisos y politicas necesarias para el despligue de la aplicación, aquí un [ejemplo de pólitica AWS](https://gist.github.com/AbnerGrajales/2f2ce15a4544e5a308bafb56fe23fcbe).
>
> Deberá tener instalado el [cliente de AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) para poder configurar la cuenta.
>
> Se deberá contar con un bucket para el archivo super-secret-config.json (aqui estan las configuraciones de la base de datos y variables de entorno).
>
> Se deberá contar con un RDS PostgreSQL para el despligue de la base de datos.
>
> Una ves desplegada la funcion se debe agregar el DNS de la lambda a la lista de ALLOWED_HOSTS.

```
# Configurar la cuenta AWS
$ aws configure

# Inicializar zappa (solo para proyectos de cero)
$ zappa init

# Despliegue inicial (dev o prod)
$ zappa deploy dev

# Actualización del despligue
$ zappa update dev

# Configurar variables de entorno remotas
$ cp super-secret-config.sample.json super-secret-config.json

# Desplegar variables al
$ aws s3 sync super-secret-config.json s3://<bucket-name>/

# Ejecutar migraciones remotamente
$ zappa manage dev migrate

# Crear un super user en zappa
$ zappa invoke --raw dev "from project.apps.security.models import User; User.objects.create_superuser('admin', 'example@email.com', 'algunpassword')"

# Ejecutar archivos estaticos
$ python manage.py collectstatics

```

## Variables de entorno
```
DEBUG=True
APPNAME=Boilerplate Django
SECRET_KEY=secret-code-here
URL_SERVER=http://localhost:8000
URL_WEBSITE=http://localhost:8000
TIME_ZONE=UTC
PAGE_SIZE=10

FCM_SERVER_KEY=

CONEKTA_PRIVATE_KEY=
SMS_KEY=

AWS_ENABLE=False
AWS_REGION=
AWS_STORAGE_BUCKET_NAME=
AWS_CLOUD_FRONT_URL=

EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=from@example.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587

DB_HOST=localhost
DB_NAME=dbname
DB_USER=root
DB_PASSWORD=
DB_PORT=5432

```

#### General
```
# Ejecutar migraciones
$ python manage.py migrate

# Ejecutar proyecto
$ python manage.py runserver

# AWS_ENABLE=False para no usar AWS S3

# Ejecutar archivos estaticos
$ python manage.py collectstatics
```

## Crear una nueva app dentro del proyecto
```
# Ingresa
$ cd project/apps

# Crear una nueva aplicacion
$ django-admin startapp myappname
```

## Postman
> El siguiente boilerplate contiene una collection de ejemplo y un environment, los siguientes documentos se deben tomar de base para la documentación de los endpoints creados.
```
postman_environment.json
postman_collection.json
```

## Referencias

* [Python](https://www.python.org/doc/)
* [Django](https://docs.djangoproject.com/en/2.0/)
* [AWS IAM](https://aws.amazon.com/iam/)
* [Zappa](https://www.zappa.io)
* [Pip, Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [Redis](https://redis.io/topics/quickstart)

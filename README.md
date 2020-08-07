Basic API for True Home Test
========================================

> Framework [Django 2.2](https://docs.djangoproject.com/en/2.2/)
## Acerca

 CRUD, básico, con Django Rest Framework en el cual se pueden Agregar nuevas Posts, Actualizarlas y Eliminarlas (con un borrado lógico)

## Requisitos

- virtualenv
- Python 3
- pip
- (PostgreSQL) 9.5.15

## Estructura del proyecto

```
raiz_del_proyecto/
    venv/
        ... source files

    project/
        __init__.py
        urls.py
        wsgi.py
        settings.py

     apps/
         categories/
         posts/

    core/

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

     .env
     manage.py
     requeriments.txt

```
## Referencias

* [Python](https://www.python.org/doc/)
* [Django](https://docs.djangoproject.com/en/2.0/)
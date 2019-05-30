# gestor_consulta

## Sistema gestor de consultas

Desarrollado en django, realizado con la idea de ser un administrador de consultas, que sea consumido vía rest

## Instalación
  
```
  mkvirtualenv gestor_consulta -p /usr/bin/python3
  pip install -r requirements.txt
```

## Crear migraciones

```
  python manage.py makemigrations base
  python manage.py makemigrations users
  python manage.py makemigrations consulta

  python manage.py migrate
```

## Cargar fixtures

```
  python manage.py loaddata fixtures/initial_entidad.json
  python manage.py loaddata fixtures/initial_municipio.json
  python manage.py loaddata fixtures/initial_parroquia.json
  python manage.py loaddata fixtures/initial_tipo_pregunta.json
```

## Correr aplicación

  `python manage.py runserver`

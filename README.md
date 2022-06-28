# TestTechnique

This is a backend application that was developed with Django 

# What you need to run this projects

* Docker (https://docs.docker.com/engine/install/)
* Docker compose (https://docs.docker.com/compose/install/compose-plugin/)


# To start the project in docker (using bash)
```
docker-compose up -d --build
```

and then to see logs :

```
docker ps
docker logs -f <container_name>
```

```
Open the file dachboard.html with your browser
```

# To run units tests

```
cd TestTechnique/
python manage.py test --verbosity=2
```
#!/bin/sh

cd TestTechnique
mkdir -p ./logs
mkdir -p ./static
yes | python manage.py makemigrations > /dev/stderr
yes | python manage.py makemigrations api > /dev/stderr
yes yes | python manage.py migrate > /dev/stderr

python manage.py runserver 0.0.0.0:5000 > /dev/stderr


#!/bin/bash

echo "Create database migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
python manage.py runserver 0.0.0.0:8000

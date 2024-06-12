#!/bin/sh
export PYTHONPATH="${PYTHONPATH}:${pwd}"
# pip install -e .
python manage.py makemigrations app
python manage.py migrate
python manage.py runscript create_super_user
python manage.py runscript add_data
python manage.py runserver 0.0.0.0:8100


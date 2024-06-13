echo "starting wsgi"
gunicorn geo_project.wsgi:application --bind 0.0.0.0:8100
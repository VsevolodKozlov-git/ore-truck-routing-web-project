#!/bin/sh
export PYTHONPATH="${PYTHONPATH}:${pwd}"


PROFILE_FILE="$HOME/.profile"

if [ -z "$IS_DJANGO_SET" ]; then
    echo "Начинает инициализация джанго"
    python manage.py collectstatic
    python manage.py makemigrations app
    python manage.py migrate
    python manage.py runscript create_super_user
    python manage.py runscript add_data
    echo "export IS_DJANGO_SET=1" >> "$PROFILE_FILE"
    export IS_DJANGO_SET=1
    # Apply the changes to the current session
    if [ -f "$SYSTEM_PROFILE_FILE" ]; then
        . "$SYSTEM_PROFILE_FILE"
    fi
else
  echo "Этап инициализации django пропущен"
fi

# python manage.py runserver 0.0.0.0:8100


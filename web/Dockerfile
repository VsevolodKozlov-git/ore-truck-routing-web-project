FROM ghcr.io/osgeo/gdal:alpine-small-latest
# FROM python:3.10

ENV PYTHONUNBUFFERED 1
# Устанавливаю python и библиотеки для GeoDjango с PostGis
RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache python3 py3-pip postgresql-client geos
# Создаю виртуальное окружение
WORKDIR /requirements
RUN python3 -m venv /requirements/venv
ENV PATH="/requirements/venv/bin:$PATH"
# Устанавливаю requirements
COPY requirements.txt .
RUN /requirements/venv/bin/pip install --upgrade pip
RUN /requirements/venv/bin/pip install -r requirements.txt
# Перемещаюсь в рабочую дирректорию приложения
WORKDIR /app
# Не копирую приложение, потому что оно будет с монтировано при помощи bind mount
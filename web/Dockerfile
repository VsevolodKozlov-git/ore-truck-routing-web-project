FROM ghcr.io/osgeo/gdal:alpine-small-latest
# FROM python:3.10

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache python3 py3-pip postgresql-client geos

# Обновляем пакетный менеджер
# RUN apt-get update -y

# # Ставим зависимости GDAL, PROJ
# RUN apt-get install -y gdal-bin libgdal-dev
# RUN apt-get install -y python3-gdal
# RUN apt-get install -y binutils libproj-dev
# RUN apt-get install -y postgresql-client

WORKDIR /requirements
RUN python3 -m venv /requirements/venv

COPY requirements.txt /requirements/requirements.txt
RUN /requirements/venv/bin/pip install --upgrade pip
RUN /requirements/venv/bin/pip install -r requirements.txt

ENV PATH="/requirements/venv/bin:$PATH"

WORKDIR /app
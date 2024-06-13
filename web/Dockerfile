FROM ghcr.io/osgeo/gdal:alpine-small-latest
# FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache python3 py3-pip postgresql-client geos

WORKDIR /requirements
RUN python3 -m venv /requirements/venv
ENV PATH="/requirements/venv/bin:$PATH"

COPY requirements.txt .
RUN /requirements/venv/bin/pip install --upgrade pip
RUN /requirements/venv/bin/pip install -r requirements.txt

WORKDIR /app
FROM python:3.12-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'backend.settings'

COPY requirements.txt requirements.txt

RUN  apt-get update && apt-get -y install postgresql postgresql-client
RUN  apt-get install --force-yes -y gcc
RUN  apt install --force-yes -y libpq-dev
RUN  apt-get -y install gettext
RUN  mkdir -p /opt/app/static/
RUN  mkdir -p /opt/app/media/
RUN  pip install --upgrade pip
RUN  pip install -r requirements.txt

RUN apt install netcat-traditional

COPY . .

RUN  chmod +x ./entrypoint.bash

EXPOSE 8000

ENTRYPOINT ["bash", "./entrypoint.bash"]

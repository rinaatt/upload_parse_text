FROM python:3.6-slim AS base

LABEL maintainer="rinaatt@gmail.com"

RUN apt-get update \
 && apt-get install -y gcc libc6-dev gettext sqlite3 --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -r django && useradd -r -g django django
RUN pip3 install -U pip && pip3 install -U setuptools

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -U -r /tmp/requirements.txt

RUN mkdir -p /var/app && chown -R django /var/app
VOLUME /var/app
WORKDIR /var/app


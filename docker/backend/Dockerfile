FROM python:3.6-slim

RUN mkdir -p /usr/src/app

RUN apt-get update \
 && apt-get install -y gcc libc6-dev gettext sqlite3 --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -U -r /tmp/requirements.txt

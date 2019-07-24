FROM python:3.7

RUN useradd -ms /bin/bash application

WORKDIR /home/application

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY application.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP application.py
ENV APP_ENV prod

RUN chown -R application:application ./
USER application

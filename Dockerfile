FROM python:3.6

RUN useradd -ms /bin/bash application

WORKDIR /home/application

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY application.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP application.py
ENV DATABASE_URL postgresql+psycopg2://admin_dev:wBcrn9L3iFpP4SwQDZ5v@problematic-dev.c303nxa0xbnw.us-west-1.rds.amazonaws.com:5432/problematic_dev

RUN chown -R application:application ./
USER application

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

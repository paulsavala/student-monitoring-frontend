#!/bin/bash
source venv/bin/activate
flask db upgrade
exec gunicorn application:app
python app/utils/create_admin.py
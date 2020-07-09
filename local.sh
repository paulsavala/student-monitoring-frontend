#!/bin/bash
source venv/bin/activate
export FLASK_APP=application.py
flask db init
flask db upgrade
flask run
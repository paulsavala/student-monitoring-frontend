#!/bin/bash
source venv/bin/activate
exec gunicorn application:app
#!/bin/bash
source venv/bin/activate
export FLASK_APP=application.py
export GOOGLE_CLIENT_ID=783089577751-7g0ob41ii6hkc0a57v2f8unmm395ghk6.apps.googleusercontent.com
export GOOGLE_CLIENT_SECRET=XoQUNqS2sD1RzaoyIbjvTvOx
export DATABASE_URL=sqlite:///../student_monitoring/app.db
flask run --cert adhoc
#!/bin/bash
export FLASK_APP=app.py
#flask run -h 0.0.0.0
gunicorn -b calc.manuelpm.me:5000  -w 4 app:app
#gunicorn -b localhost:5000  -w 4 app:app

#!/bin/sh
cd /code
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run --port 8089 --host=0.0.0.0

#!/bin/bash
source /home/www/code/postarama/venv/bin/activate
source /home/www/code/postarama/venv/bin/postactivate
exec gunicorn  -c "/home/www/code/postarama/gunicorn_config.py" yatube.wsgi


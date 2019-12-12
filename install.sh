#!/bin/bash
brew install python3
pip3 install django django-extensions pillow Werkzeug pyOpenSSL
python3 manage.py makemigrations
python3 manage.py migrate
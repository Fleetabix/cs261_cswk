#!/bin/bash
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@florin.cb', 'qwertyuiop')"
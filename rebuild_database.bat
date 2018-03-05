del db.sqlite3
deltree chatbot/migrations/__pycache__
del chatbot/migrations/$(ls chatbot/migrations/ | grep ^[0-9])
python manage.py makemigrations
python manage.py migrate
python ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@florin.cb', 'qwertyuiop')"

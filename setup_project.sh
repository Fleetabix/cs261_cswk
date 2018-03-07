#!/bin/bash

if [[ $1 == 3 ]]; then
	echo "------ Installing Requirments --------"
	pip3 install -r requirements.txt
	python3 -c "import nltk; nltk.download('punkt')"
	python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
	python3 -c "import nltk; nltk.download('vader_lexicon')"
	echo "-------- Rebuilding Database ---------"
	rm db.sqlite3
	rm -r chatbot/migrations/__pycache__
	rm chatbot/migrations/$(ls chatbot/migrations/ | grep ^[0-9])
	python3 manage.py makemigrations
	python3 manage.py migrate
	echo "-------- Populating Database ---------"
	python3 ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@florin.cb', 'qwertyuiop')"
	python3 manage.py populate_db
else
	echo "------ Installing Requirments --------"
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('punkt')"
	python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
	python3 -c "import nltk; nltk.download('vader_lexicon')"
	echo "-------- Rebuilding Database ---------"
	rm db.sqlite3
	rm -r chatbot/migrations/__pycache__
	rm chatbot/migrations/$(ls chatbot/migrations/ | grep ^[0-9])
	python manage.py makemigrations
	python manage.py migrate
	echo "-------- Populating Database ---------"
	python ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@florin.cb', 'qwertyuiop')"
	python manage.py populate_db
fi

echo "---------- Setup Complete ------------"
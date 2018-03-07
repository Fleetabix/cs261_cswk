#!/bin/bash

if [[ $1 == 3 ]]; then
	pip3 install -r requirements.txt
	python3 -c "import nltk; nltk.download('punkt')"
	python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
	./rebuild_database.sh
	python3 manage.py populate_db
else
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('punkt')"
	python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
	./rebuild_database.sh
	python manage.py populate_db
fi
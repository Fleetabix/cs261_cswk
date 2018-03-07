#!/bin/bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
./rebuild_database.sh
python manage.py populate_db
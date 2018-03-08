
echo "------ Installing Requirments --------"
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
python -c "import nltk; nltk.download('vader_lexicon')"
echo "-------- Rebuilding Database ---------"
del db.sqlite3
del chatbot/migrations/__pycache__
dir -name chatbot/migrations | select-string -pattern "[0-9]_" | %{rm chatbot/migrations/$_}
python manage.py makemigrations
python manage.py migrate
echo "-------- Populating Database ---------"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@florin.cb', 'qwertyuiop')"
python manage.py populate_db


echo "---------- Setup Complete ------------"
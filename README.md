# cs261_cswk
Financial Trader Chatbot

## helpfull commands

When using the manage.py script, make sure it's running on python 3. Using just 'python'
can work, but if it doesn't use 'python3' to specify your version.

To start the server so you can view the website
```
$ python manage.py runserver 
```

To run the tests
```
$ python manage.py test chatbot 
```

When modifying the chatbot database models, you might need to run the following to apply the changes
```
# to create migrations for the database
$ python manage.py makemigrations
# to pply the changes to the database
$ python manage.py migrate
```

## project structure

- website/ (the base website code, we do not need to edit this, just add the chatbot app in the settings)
- chatbot/ (this is where most, if not all of our code will be
   - models.py (where our database models are defined)
   - views.py  (where the content of each webpage will be defined)
   - test.py   (where the unit tests will be written)
   - urls.py   (where we map URLs to views for this project)
   - static/   (where all the static files will be placed - e.g. stylesheets, images, js)
   - templates/ (where our page templates are stored)


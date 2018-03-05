# cs261_cswk
Financial Trader Chatbot

## Dependencies

For the chatbot to function properly, you need to install some python packages before
trying to use the data or nlp functions. To install them just use
```
$ pip3 install -r requirments.txt
```
Add any new requirements to the `requirements.txt` file (the version can be obtained by
running `pip3 freeze` and looking for your package)

Lastly, some modules may not install properly on the DCS machines. I have not found
a way to fix this, so just run and test the chatbot on your own laptops.

## Helpful commands

When using the manage.py script, make sure it's running on python 3. Using just 'python'
can work, but if it doesn't use 'python3' to specify your version.

To start the server so you can view the website
```
$ python manage.py runserver 
```

When modifying the chatbot database models, you might need to run the following to apply the changes
```
# to create migrations for the database
$ python manage.py makemigrations
# to apply the changes to the database
$ python manage.py migrate
```

Once the server is running, visit the chatbot by going to _localhost:8000/chatbot_

## Testing
Testing is done via unit tests, there are two test modules; DataTests and NLPTests. All tests can be run using
```
$ python -W "ignore" manage.py test chatbot 
```
where the 'W' flag tells the testing client to ignore warnings (in this case warnings from the data module using google finance api)

You can also run an individual test class or test using the following respectively
```
$ python -W "ignore" manage.py test chatbot.tests.NLPTests
$ python -W "ignore" manage.py test chatbot.tests.NLPTests.test_can_identify....
```

## Database Issues
Destroy and rebuild the database using the following command. You should do this if ot's giving you errors such as some column doesn't exist
```
$ ./rebuild_database.sh
```

## Populating the Database

The database can now be populated using a script from the command line. To alter this script go to `chatbot/management/populate_db.py'. To run this script enter the following and execute
the following commands
```
$ python3 manage.py populate_db
```

## Creating users

The website should now support users, but there isn't a sign up page yet. To create your own user,
go to _localhost:8000/admin_ and sign in with
- username: 'admin'
- password: 'qwertyuiop'

then simply add a user by pressing '+ Add' on the user link. Not sure if it will be important in the future, but when registering a user, add them to the 'Chatbot Users' group.

## Project structure

- website/ (the base website code, we do not need to edit this, just add the chatbot app in the settings)
- chatbot/ (this is where most, if not all of our code will be
   - models.py (where our database models are defined)
   - views.py  (where the content of each webpage will be defined)
   - test.py   (where the unit tests will be written)
   - urls.py   (where we map URLs to views for this project)
   - static/   (where all the static files will be placed - e.g. stylesheets, images, js)
   - templates/ (where our page templates are stored)


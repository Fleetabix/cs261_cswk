# FLORIN
Financial Trader Chatbot

## Setup
Here are some instructions to help you set up the project to try out.

### Virtual Environment
Although this is not needed, you can setup and run this project inside of a python virtual
environment. The benifit of this is that all the requirments this project need downloaded will
only exist inside the virtual environment and will not override or conflict with your normal
python packages.

After downloading `virtualenv` (`apt-get install virtualenv`, `brew install virtualenv`, etc.)
run the following
```
# create an environment called florin-env
$ virtualenv florin-env
# start up the virtual environment
$ source florin-env/bin/activate
```
To exit the environment just enter `deactivate` and it should take you back to normal.

### Quick Setup
There is a script which will hopefully download all dependencies, configure the database correctly
and populate it. If this doesn't work, there are step by step instructions after this section
on how to setup the project manually. To use this command run the following.
```
$ ./setup_project.sh
```
If you need to explicitly use `python3` instead of `python`, just add a lone argument of '3'.

### Dependencies
To install the dependencies, make sure you have pip (might be pip3) installed then run
```
pip install -r requirments.txt
```
where `requirments.txt` is in the root directory of the project.

### Database
The database should work fine straight of, but if when trying to run the project it's coming up
with errors, run
```
$ ./rebuild_database.sh
```
This should delete the database, create it again and re-populate it. Please make sure that the
python the script uses is version 3 or above (if it is not, just change the command to `python3`
wherever you see `python` in the script)


## Running the Project
When using the manage.py script, make sure it's running on python 3. Using just 'python'
can work, but if it doesn't use 'python3' to specify your version.

To start the server so you can view the website
```
$ python manage.py runserver 
```
or if you want to access this project on different devices on the same local network use
```
$ python manage.py runserver 0.0.0.0:8000
```

Once the server is running, visit the chatbot by going to _localhost:8000/_ if on the same
machine of _(local_ip_of_computer):8000_ if trying to access it on another device.


## Populating the Database
The database can now be manually populated using a script from the command line. To alter this script go to `chatbot/management/populate_db.py'. To run this script enter the following and execute
the following commands
```
$ python3 manage.py populate_db
```
Note: This command is run during `./rebuild_database.sh` so you do not need to execute this afterwards.


## Simulating Price Drops
To test if the alert system works, you can use the following command
```
$ python manage.py simulate_price_drop <ticker1> <ticker2> ...
```
This will drop the percentage difference of these companies in the database to a random number and cache them for 1 minute.

Alerts for companies are only shown if there is not a previous alert for the same company that is experiencing a price drop within the last hour. If you want to repeat the alert test (but don't want to wait an hour) just run the above command but include the `--delete-alerts` flag at the end.


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


## Creating users
The website should now support users, but there isn't a sign up page yet. To create your own user,
go to _localhost:8000/admin_ and sign in with
- username: 'admin'
- password: 'qwertyuiop'

then simply add a user by pressing '+ Add' on the user link. Not sure if it will be important in the future, but when registering a user, add them to the 'Chatbot Users' group.

There is also a test user with credentials
- username: 'johnsmith'
- password: 'qwertyuiop'
that you could use for the website.


## Project structure
- website/ (the base website code, we do not need to edit this, just add the chatbot app in the settings)
- chatbot/ (this is where most, if not all of our code will be
   - models.py (where our database models are defined)
   - views.py  (where the content of each webpage will be defined)
   - test.py   (where the unit tests will be written)
   - urls.py   (where we map URLs to views for this project)
   - static/   (where all the static files will be placed - e.g. stylesheets, images, js)
   - templates/ (where our page templates are stored)


# Splinter - O mestre do Estudo
## Pre-requisites
This is set up using PostgreSQL already, and with DEBUG mode enabled by default. So make sure to have PostgreSQL already installed with:
* a 'postgres' user
* a 'splinter' database

Or simply modify the `config.py` file accordingly.

## Setup
1. Install [`virtualenv`](https://virtualenv.pypa.io/en/latest/userguide.html#usage)
    ```bash
$ [sudo] pip install virtualenv
    ```
2. Download this Repository:
    ```bash
    $ git clone https://github.com/matheusprusch/splinter.git
    ```
3. Inside it, create a new virtual environment:
    ```bash
    $ virtualenv env
    ```
4. Then activate it:
    ```bash
    $ source env/bin/activate
    ```
Or, on Windows:
    ```
    \path\to\env\Scripts\activate
    ```
5. Finally, do:
    ```bash
    pip install -r requirements.txt
    ```
This will install all dependencies for you.
6. You can then start the app with:
    ```bash
    $ ./manage.py runserver
    ```

## Project Structure
```
├── README.md
├── app
│   ├── __init__.py   « Flask Main App
│   ├── api           « File for each pair endpoint (e.g. course and courses)
│   └── models        « Models defined. Details can be found on this repo's wiki
├── config.py         « Environment configurations.
├── manage.py         « The manager. We can run the server from here.
├── migrations        « Migrations folder with configs and revision files
├── requirements.txt
├── test.db           « SQLite3 DB for easy access
└── tests
```

## Migrations
The migrations can be invoked directly from the manager. This can be done in two parts:
1. First, verify if there are any changes to the current (up to date) database model:
```bash
$ ./manage.py db migrate
```
2. If there are differences, the above command will generate a new revision file. We can then upgrade the database from it:
```bash
$ ./manage.py db upgrade
```

## Authentication
To add authentication (auth.login_required) and verify if the user is admin (aithentication.is_administrator) to the methods on the app/api modules, simply do:
```python
from .. import authentication
from .. import auth
[...]

@auth.login_required
@authentication.is_administrator
def get():
    pass
```

## Useful Links
#### Yo Generator and Template
https://github.com/yeoman/yo
https://github.com/ColeKettler/generator-flask-api

#### Flask-RESTful
http://flask-restful-cn.readthedocs.io/en/0.3.4/index.html
http://kzky.hatenablog.com/entry/2015/11/02/Flask-Restful

#### Flask-SQLAlchemy
http://flask-sqlalchemy.pocoo.org/2.1/
https://www.codementor.io/python/tutorial/understanding-sqlalchemy-cheat-sheet

#### Flask-HTTPAuth
http://flask-httpauth.readthedocs.io/en/latest/

#### Example of Resources:
https://github.com/mmautner/simple_api/blob/master/resources.py

#### Flask-Migrate
https://github.com/miguelgrinberg/Flask-Migrate

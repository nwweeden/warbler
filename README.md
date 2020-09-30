# warbler

## Overview
- This application is designed as a replica of Twitter. Users can create a profile, post messages, follow other users, and 'like' different messages.

## Setup
- Create the virtual environment
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
- Set up the database
```
(venv) $ createdb warbler
(venv) $ python seed.py
```
- Start the server
```
(venv) $ flask run
```

## Run tests
- To run a file containing unittests:
```
FLASK_ENV=production python -m unittest <name-of-python-file>
```
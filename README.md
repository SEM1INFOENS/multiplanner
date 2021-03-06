You must replace `meowmeowmeow` with your personal API key.[![Build Status](https://travis-ci.com/SEM1INFOENS/multiplanner.svg?branch=master)](https://travis-ci.com/SEM1INFOENS/multiplanner)

# multiplanner
Here you could find a project dedicated to money and friendship.

## Requirements
All required python packages are listed in `requirements.txt`.
We currently use:
- python 3.6.4
- django 2.1.5
- pytest 3.9.1

## Installation
One could install necessary packages using the following:
```bash
pip install -r requirements.txt
```
Test installation with:
```bash
python3 manage.py test
```
Make migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
```
Launch the server using:
```bash
python3 manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/ `.

For now, you can see the main page at `http://127.0.0.1:8000/`.


## Online version
An online version is aviable at https://multiplanner.herokuapp.com/
To run commands in the server, 
first install the heroku toolbelt (https://devcenter.heroku.com/articles/heroku-cli).
Then run :
```bash
heroku login
heroku run -a multiplanner <your_command>
```

To apply migrations / create db :
```bash
heroku run -a multiplanner ./manage.py migrate
heroku run -a multiplanner ./manage.py migrate --run-syncdb
```
To start the server : 
```bash
heroku ps:scale web=1 -a multiplanner
```

> **The database should not be stored on heroku.**
> **For now it is the case but we may sometimes lose the db and have to recreate it.**
>	
> **In the future we will have to place the db somewhere else**


## Project architecture

### Project documentation

`pip install sphinx` to install docs generating tool. Then 
```
cd docs
sphinx-apidoc -o . ..
make html
```

Documentation will be available in `docs/_build/index.html`.

### Generate architecture's graph
Requirements:
- `django-extensions`
- `pyparsing` and `pydot` or `pygraphviz`

Uncomment the `grango_extensions` lines in [manage.py](manage.py) and [multiplanner/settings.py](multiplanner/settings.py) then

Generate a `.dot` graph:
```bash
python3 manage.py graph_models -a > architecture_graph.dot
```
Generate a `.png` image graph:
```bash
python3 manage.py graph_models --pydot -a -g -o architecture_graph_pydot.png
```
or:
```bash
python3 manage.py graph_models --pygraphviz -a -g -o architecture_graph_pygraphviz.png
```

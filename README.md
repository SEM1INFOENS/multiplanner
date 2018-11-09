[![Build Status](https://travis-ci.com/SEM1INFOENS/multiplanner.svg?branch=master)](https://travis-ci.com/SEM1INFOENS/multiplanner)

# multiplanner
Here you could find a project dedicated to money and friendship.

## Requirements
All required python packages are listed in `requirements.txt`.
We currently use:
- python 3.6.4
- django 2.1.2
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
python3 manage.py migrate
```
Launch the server using:
```bash
python3 manage.py runserver
```
The applicatioin will be available at `http://127.0.0.1:8000/ `.

For now, you can see list of users at `http://127.0.0.1:8000/users`, with links to user's transactions.


## Project architecture
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


### Description
* multiplanner
* presentation
  * User <https://docs.djangoproject.com/fr/2.1/ref/contrib/auth/>
    * username (mandatory)
    * first_name
    * last_name
    * email
    * password
    * user_merpissions
    * is_staff
    * ...
* relationships
  * Friendships
    * user
    * friend_list
    * invited_list
  * SecreteMark
    * user
    * marked_user
    * mark
* groups
  * Group
    * name
    * members
    * transactions
* accounting
  * SharedAccount
    * name
    * members
  * Transaction
    * motive
    * date
    * payer
    * amount
    * beneficiaries
* agenda
  * TimeRange
    * date
    * duration
  * Event
    * date
    * place
    * creator
    * attendees
    * invited
    * transactions
  * MeetingRules
    * minimum_delay
    * maximum_delay
    * duration
    * possible_time_ranges
    * creator
    * administrators

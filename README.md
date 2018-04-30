# flask-sample
Flask App


Install
-------

    # clone the repository
    git clone https://github.com/ADR-Project/flask-adr.git
    cd flask-adr

Create a virtualenv and activate it::

    python3 -m venv env_flask
    . env_flask/bin/activate



Authnitcation
---------------

GET
url : http://127.0.0.1:5000/api/token
pass username and password in auth headers
you will get a token. Use this token for future auth


Create a new user
--------------------

POST
http://127.0.0.1:5000/api/users

pass
        password
        email
        first_name
        last_name


To check authentication
---------------------------

GET

http://127.0.0.1:5000/api/resource

pass

token obtained from token api in auth headers
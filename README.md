## Description

Backend for a Messaging app utilizing Django REST Framework. Supports both direct messages and multi-user groups. Features robust validations and permissions system

## Installation
Clone the repository using the link on the repository page

cd into the repository folder and type:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
migrate database and run the server with:
```
python manage.py migrate
python manage.py runserver
```

## Usage
Create user by filling up sign up form located at `/accounts/signup`

To obtain user token visit `/api/token`

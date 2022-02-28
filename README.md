# Tindeed

## Language Versions in use
- @vue/cli: 5.0.1
- python: 3.10.2
- django: 4.0.2

## Installing Locally
1. navigate into client and run ```npm i``` to install the required npm packages.
2. run ```pip install djangorestframework django-cors-headers django-environ``` in any directory.
3. add a file named .env in the api/api directory (the same one as settings.py) and enter the secret key posted on teams.

## Running servers
**api:** navigate into the api directory and run ```python manage.py runserver```. The django app will be available at localhost:8000

**client:** navigate into the client directory and run ```npm run serve```. The vue app will be available at localhost:8080

**remote server:** 134.209.29.204


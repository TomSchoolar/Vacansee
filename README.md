# Tindeed

## Language Versions in use
- @vue/cli: 5.0.1
- python: 3.10.2
- django: 4.0.2

## Local Dev Environment

### Installing Locally
1. navigate into client and run ```npm i``` to install the required npm packages.
2. run ```pip install djangorestframework django-cors-headers django-environ``` in any directory.
3. add a file named .env in the api/api directory (the same one as settings.py) and enter the secret key posted on teams.

### Running Servers Locally
**api:** navigate into the api directory and run ```python manage.py runserver```. The django app will be available at localhost:8000

**client:** navigate into the client directory and run ```npm run serve```. The vue app will be available at localhost:8080


## Requirements

A full list of required packages is available at:

- client/package.json for vue
- api/requirements.txt for django (excluding the postgres package)

New packages installed for the client should be added to package.json automatically (if you use the -S/--save flag or to dev-dependencies with --save-dev). Packages installed for django have to be manually added to api/requirements.txt using ```pip freeze > requirements.txt``` 

**IMPORTANT:** If you update requirements.txt, make sure you remove the psycopg2 line as this package only works for Windows and psycopg2-binary must be used for linux. However, if the wrong one is present in the requirements file when it is used to install dependencies, it will crash the intstaller process and therefore the correct version must be installed manually.

To install the dependencies for the client, navigate into the client directory and run ```npm i```, for the api navigate into the api directory and run ```pip install -r requirements.txt && pip install psycopg2-binary``` removing the -binary if necessary (i.e. if on Windows).


## CI/CD

The CI pipeline will automatically test every commit to any branch and build, test and then deploy any commits or merges into the main branch. This is done using two custom gitlab runners on the remote vm (one running a node container and the other a python one according to the version specs above). This is because the shared runners are not able to connect to the database and also because they are shared and therefore slow.

## Testing

Testing is done using Jest for js/vue and unittest (the default python testing framework) for python/django. The relevant docs are linked below:

- **Jest:** https://jestjs.io/docs/getting-started
- **vue.js:** https://vuejs.org/guide/scaling-up/testing.html
- **unittest:** https://docs.python.org/3/library/unittest.html
- **django:** https://docs.djangoproject.com/en/4.0/topics/testing/overview/
 
### Testing in python

Tests are detected and run according to the Vue/Jest and Django/unittest docs. There are example tests in api/api/tests_example.py and client/tests/unit/example.spec.js.

In order to be make sure python tests are discoverable, they must be in a file with the filename beginning with the word test and the test functions must also begin with the word test. e.g.

``` 
/api/test_demo.py:
    from django.test import TestCase

    class FooTest(TestCase):

        def this_wont_run(self):
            print 'Fail'

        def test_this_will(self):
            print 'Win'
```

Each django app will auto-generate a tests.py file, this will be insignificant to hold all the tests for each app so it is advisable to create a tests folder with multiple test_namehere.py files.

To run the tests, navigate to /api and run ```python manage.py test```. To run tests and get coverage information, run:

- ```coverage erase```
- ```coverage run --source='.' manage.py test```
- ```coverage report```

in the same directory. To view a more interactive and detailed report, run ```coverage html``` instead of ```coverage report```. Open the generated html file in a browser and you will be able to see which lines are covered by tests and which are not, file by file. To view the basic coverage report on gitlab, click on the relevant pipeline and then on the run-python-unit-tests job to view the summary at the bottom of the log.

### Testing in js

To make sure Jest tests are discovered, they should be put in the tests directory and the filenames should be suffixed with .spec.js. It is good practice to put tests in a directory named \_\_tests__ but that requires additional configuration for them to be discovered correctly and I cba with that. If anyone else wants to then please go right ahead. To run the tests, navigate to the client directory and run ```npm test```. There will be a report of test pass/fail results and also a coverage summary. To see this in the gitlab pipeline, go to the relevant pipeline, click on the run-js-unit-tests job and navigate to the bottom of the log.

There is an example test file at client/tests/unit/example.spec.js.

## Environment Variables

To update environment variables, they must be changed locally and also on gitlab. Go to the repo, settings, 'CI/CD' and then 'Variables'. Add/update/remove the required env var in both the ENV_FILE (for the production server) and also TEST_ENV_FILE (for the application during testing in the ci pipeline). When the environment variables are updated on gitlab, these will be reflected the next time the test/deploy stages are run respectively. 

Absolutely no sensitive/secret data should be stored anywhere in the client code. If it is possible for the code to access it, it is possible for anyone with chrome dev tools to access it as well. All authentication/verification should be done server side on the api.

## Live servers

**remote server ip:** 134.209.29.204

The remote vm hosts the following:

- **postgres server:** port 5432
- two gitlab runners: one for node, one for python
- **gunicorn django server:** port 8000
- **nginx vue server:** port 80

## Databases

The remote postgres server contains three main databases, one called tpdev (for local development), one called tptest (for pipeline api testing) and one called tpproduction (for use by the live app). Migrations are carried out on the testing and production databases automatically everytime the api testing and build jobs are called in gitlab but the development database will have to have migrations done manually by one person whenever the models are updated. This is done by running the following in the top level api directory:

- ```python manage.py makemigrations```
- ```python manage.py migrate```

## Code approval/merge process

Below is an outline of the code integration process we discussed:

1. Develop each kanban task on a new branch (```git checkout -b [branch name]```) and commit any changes to that branch.
2. When the feature/task is complete, run tests locally and then push to the branch on gitlab (```git push -u [branch name]```)
3. Create a merge request and assign someone if you want, otherwise maybe make a kanban task or ask on teams idk
4. Someone should review your pr and then merge into main
5. The pipeline will build, test and deploy the changes if there are no issues with the code

You can then remove the branch locally using ```git fetch --prune```
# Vacansee 
Note: Since the server is no longer running some functionality of the repo may be broken

[![pipeline status](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/badges/main/pipeline.svg)](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/-/commits/main) [![coverage report](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/badges/main/coverage.svg?job=run-python-unit-tests&key_text=API%20Coverage&key_width=90&min_good=90&min_acceptable=80&min_medium=70)](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/-/commits/main) [![coverage report](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/badges/main/coverage.svg?job=run-js-unit-tests&key_text=Client%20Coverage&key_width=100&min_good=90&min_acceptable=80&min_medium=70)](https://git-teaching.cs.bham.ac.uk/mod-team-project-2021/team45-21/-/commits/main)

## Language Versions in use
- @vue/cli: 5.0.1
- python: 3.10.2
- django: 4.0.2


## Local Dev Environment

### Installing Locally
1. navigate into client and run ```npm i``` to install the required npm packages.
2. run ```pip install -r requirements.txt && pip install psycopg2``` in the top level api directory.
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


## Pipeline Replication

In order to replicate the pipeline that we have in operation in this repository, follow the steps below:

1. Create a new ssh key pair. Copy the public key into the /root/.ssh/authorized_keys file.
2. Create the following GitLab CI/CD Variables:
    - SERVER_IP (Variable): the ip of the hosting server
    - SSH_PRIVATE_KEY (Variable): the value of the private key generated in the previous step
    - ENV_FILE (File): contains all of the secret key value pairs from the api for use in production
    - TEST_ENV_FILE (File): contains all of the secret key value pairs from the api for use in testing (same as above but we use a separate db for testing)
    - PRODUCTION_CLIENT_ENV_FILE (File): contains the api endpoint for use by the client in production
3. ssh into the server and create a directory ~/code (at the same level as /home, /usr etc)
4. create a directory ~/code/client
5. assuming you are using the same .gitlab-ci file as is in this repository, you should be good to go

n.b. The above instructions require an Ubuntu 20.04 server with a public IPv4 address.


## Making requests to the api

The client has a package called axios installed to send and receive requests/responses to/from the api. The docs can be found here:

- https://www.npmjs.com/package/axios
- https://axios-http.com/docs/intro

The auth system uses json web tokens (jwts) in the form of access and refresh tokens to provide api access. In order for this system to work, a modified version of the default axios instance must be imported and used in sfcs. Further, in the same file as the modified axios object (called api) there is a request error handler to standardise error handling and tidy up the sfcs. Both objects can be imported and used like this:

```javascript
import api, { apiCatchError } from '@/assets/js/api';

const makeRequest = async () => {
    const response = await api({
        url: '/e/vacancy/',
        method: 'get',
        responseType: 'json'
    }).catch(apiCatchError);

    return response?.data
}
```

You will notice in the above example that baseURL and timeout are not defined in the request object, this is because they have been pre-defined in the api object as the api endpoint and 3000 (ms) respectively. These can be overridden if required by setting them in the request object, this might be useful if a request takes a long time (although idk why a request would be taking 3+ seconds).

The authorisation token has also not been added to the request object as the api object adds this itself before sending the request. It will attach the access token unless the url is in an array in the source file (currently only includes /refreshtoken/ and /logout/) in which case the refresh token will be attached. The instance will also update the auth token on all subsequent requests following a token refresh request including those submitted before the refresh request returned. All jwt helper functions have been removed apart from logout() since jwt manipulation should not really occur in the client, if you need user data outside of getting it from the api, this can be retrived from the session in localStorage.

The api object, as well as attaching the auth tokens to every request, handles the case where a request fails with status 401. If this happens, and a refresh token can be retrieved from localStorage, it makes a token refresh request to receive a token pair if the refresh token is valid. If the refresh token has expired, is missing or the refresh request fails in some other way, the user is logged out. Further, token reuse results in both parties that used the same token in refresh requests being logged out (once their access token has expired).

All existing api requests on main have been updated to use the api object, make sure that any new routes also use this otherwise the authentication system will fail and all requests will result in 401 if you don't provide an access token and *all* requests after the access token has expired will fail.

Finally, do not pass the current user id as a param/data item in an api request, get the id from the jwt only on the api side. To help enforce this and for improved security, the user id has been removed from the session.



## CI/CD

The CI pipeline will automatically test every commit to any branch and build, test and then deploy any commits or merges into the main branch. This is done using two custom gitlab runners on the remote vm (one running a node container and the other a python one according to the version specs above). This is because the shared runners are not able to connect to the database and also because they are shared and therefore slow.

### Artifacts

Build artifacts for the whole repository are available on the jobs tab of the latest pipeline for each branch with a default expiry of somewhere between 1 week - 30 days (I can't remember, rip). Testing and coverage reports are also available for download on the testing jobs in the same tab.


## Testing

Testing is done using Jest for js/vue and unittest (the default python testing framework) for python/django. The relevant docs are linked below:

- **Jest:** https://jestjs.io/docs/getting-started
- **vue.js:** https://vuejs.org/guide/scaling-up/testing.html
- **unittest:** https://docs.python.org/3/library/unittest.html
- **django:** https://docs.djangoproject.com/en/4.0/topics/testing/overview/
 
### Testing in python

Tests are detected and run according to the Vue/Jest and Django/unittest docs. There are example tests in api/api/tests_example.py and client/tests/unit/example.spec.js.

In order to be make sure python tests are discoverable, they must be in a file with the filename beginning with the word test and the test functions must also begin with the word test. e.g.

```python 
/api/test_demo.py:
    from django.test import TestCase

    class FooTest(TestCase):

        # set the fixtures you want the temporary test db (not tptest) to use while running the tests in this class
        fixtures = ['authentication/fixutures/fixtures.json'] 

        def this_wont_run(self):
            print('Fail')

        def test_this_will(self):
            print('Win')
```

Each django app will auto-generate a tests.py file, this will be insufficient to hold all the tests for each app so it is advisable to create a tests folder with multiple test_namehere.py files. If creating a tests directory, you also need to create an empty file called \_\_init\_\_.py in order to make django discover the tests files in the directory.

To run the tests, navigate to /api and run ```python manage.py test```. To run tests and get coverage information, run:

- ```coverage erase```
- ```coverage run --source='.' manage.py test```
- ```coverage report```

in the same directory. To view a more interactive and detailed report, run ```coverage html``` instead of ```coverage report```. Open the generated html file in a browser and you will be able to see which lines are covered by tests and which are not, file by file. To view the basic coverage report on gitlab, click on the relevant pipeline and then on the run-python-unit-tests job to view the summary at the bottom of the log.

### Testing in js

To make sure Jest tests are discovered, they should be put in the tests directory and the filenames should be suffixed with .spec.js. It is good practice to put tests in a directory named \_\_tests__ but that requires additional configuration for them to be discovered correctly and I cba with that. If anyone else wants to then please go right ahead. To run the tests, navigate to the client directory and run ```npm test```. There will be a report of test pass/fail results and also a coverage summary. To see this in the gitlab pipeline, go to the relevant pipeline, click on the run-js-unit-tests job and navigate to the bottom of the log.

To explore coverage in more detail, go to the tests/coverage folder and open index.html.

There is an example test file at client/tests/unit/example.spec.js.

n.b. due to a bug with the default babel coverage detection provider, we are having to use the experimental v8 provider since the babel one ignores all new sfcs.

### Test coverage integration with gitlab

Cobertura xml coverage reports files are created by the api and client testing frameworks which are uploaded to gitlab as artifacts, these should allow code coverage to be reviewed in gitlab diffs. The client and api testing jobs in the ci pipeline also report headline coverage statistics which can then be seen in the jobs tab of a pipeline and at the top of this readme.

Test coverage grading is set as follows:

- **90%+**: good
- **80%+**: acceptable
- **70%+**: medium
- **<70%**: low


## Environment Variables

To update api environment variables, they must be changed locally and also on gitlab. Go to the repo, settings, 'CI/CD' and then 'Variables'. Add/update/remove the required env var in both the ENV_FILE (for the production server) and also TEST_ENV_FILE (for the application during testing in the ci pipeline). When the environment variables are updated on gitlab, these will be reflected the next time the test/deploy stages are run respectively. 

Absolutely no sensitive/secret data should be stored anywhere in the client code. If it is possible for the code to access it, it is possible for anyone with chrome dev tools to access it as well. All authentication/verification should be done server side on the api. There is an .env file in the client directory for variables dependent on environment (such as api endpoint). All client env vars must be prepended with ```VUE_APP_``` in order for vue to load them. Like with the api env vars, and new/updated env vars need to be added/changed in CI/CD settings as well as locally and the local .env file mustn't be committed to version control as it will conflict with the env vars from gitlab.

There is currently no .env file for the client in the test job.


## Live servers

**remote server ip:** 134.209.29.204

The remote vm hosts the following:

- **postgres server:** port 5432
- two gitlab runners: one for node, one for python
- **gunicorn django api server:** **api.tp45.co.uk**
- **nginx vue client server:** **tp45.co.uk**

The client is now running at **tp45.co.uk** with ssl enabled.


## Databases

The remote postgres server contains three main databases, one called tpdev (for local development), one called tptest (for use when writing tests to populate with whichever fixtures your tests use) and one called tpproduction (for use by the live app). Note that the tptest database is not actually used by django while testing, the tests set up their own temporary, test database. Migrations are carried out on the testing and production databases automatically everytime the api testing and build jobs are called in gitlab but the development database will have to have migrations done manually by one person whenever the models are updated. This is done by running the following in the top level api directory:

- ```python manage.py makemigrations```
- ```python manage.py migrate```

Changing the data to be seeded can be done by editing the fixtures.json file. The database can be seeded with the command:

- ```python manage.py loaddata fixtures.json```

## Code approval/merge process

Below is an outline of the code integration process we discussed:

1. Develop each kanban task on a new branch (```git checkout -b [branch name]```) and commit any changes to that branch.
2. When the feature/task is complete, run tests locally and then push to the branch on gitlab (```git push -u origin [branch name]```)
3. Create a merge request and assign someone if you want, otherwise maybe make a kanban task or ask on teams idk
4. Someone should review your pr and then merge into main
5. The pipeline will build, test and deploy the changes if there are no issues with the code

You can then remove the branch locally using ```git fetch --prune```


## Colour palette & CSS colour vars

Most of these colours are also set as CSS colour variables in @/App.vue so are readable in every component. It's quicker just to write white or #fff anyway and the same with black so they have not been added. Some colours also have emphasis colours for when they are used to colour a button and you need to change the colour in the hover/focus/active state(s).

| colour name   | hex     |  css var           | 
| ------------- | ------- | ------------------ |
| red           | #cc2936 | var(--red)         |
| _red focus_   | #bb2531 | var(--red-focus)   |
| blue          | #08415c | var(--blue)        |
| _blue focus_  | #0a567a | var(--blue-focus)  |
| slate grey    | #6b818c | var(--slate)       |
| _slate focus_ | #627680 | var(--slate-focus) |
| white         | #ffffff |                    |
| jet           | #333333 | var(--jet)         |
| black         | #000000 |                    |


palette if you wanna mess around to find new colours or something: https://coolors.co/08415c-cc2936-6b818c-ffffff-333333

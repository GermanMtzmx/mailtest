# Django REST App

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```bash
$ sudo apt-get install python3-dev python3-venv linux-headers-$(uname -r) build-essential
$ python -m venv /path/to/venv
$ source /path/to/venv/bin/activate
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```bash
(venv)$ pip install -r requirements.txt
```

### Making database migrations

```bash
(venv)$ python manage.py makemigrations
```

### Applying database migrations

```bash
(venv)$ python manage.py migrate
```

### Loading initial database data

```bash
(venv)$ python manage.py loaddata fixtures/auth_users.json
(venv)$ python manage.py loaddata --app accounts users
```

### Running django development server

```bash
(venv)$ python manage.py runserver localhost:9001
```

### Running celery worker and beat

```bash
(venv)$ python -m celery -A app worker -E -B -l info
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

```bash
(venv)$ python manage.py test
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django framework](https://www.djangoproject.com/)
* [REST framework](http://www.django-rest-framework.org/)
* [Channels](https://channels.readthedocs.io/en/stable/)
* [Celery](http://www.celeryproject.org/)

## Contributing

Please read CONTRIBUTING file for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

See the list of contributors who participated in this project.

## License

This project is licensed under the X License - see the LICENSE.md file for details.

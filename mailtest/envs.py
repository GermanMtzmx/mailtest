import os
import socket

from celery.schedules import crontab


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Env:
    """Env"""

    SECRET_KEY = ')&!pn-u*ijid#&*nzcvse!w^b1#o3ix)cilvq+838yov$q5o1i'

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    ROOT_URLCONF = 'mailtest.urls'

    WSGI_APPLICATION = 'app.wsgi.application'

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    STATIC_URL = '/static/'
    STATIC_ROOT = 'collectstatic'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'media'

    EMAIL_HOST = 'mail.xtistoremexico.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'noreply@xtistoremexico.com'
    EMAIL_HOST_PASSWORD = 'T7a3up$8'
    DEFAULT_FROM_EMAIL = 'noreply@xtistoremexico.com'
    # EMAIL_HOST = 'smtp.gmail.com'
    # EMAIL_PORT = 587
    # EMAIL_USE_TLS = True
    # EMAIL_HOST_USER = 'ironbit.test2@gmail.com'
    # EMAIL_HOST_PASSWORD = 'Ironbit2017'
    # DEFAULT_FROM_EMAIL = 'ironbit.test2@gmail.com'
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = ()
    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
    )
    CORS_ALLOW_HEADERS = (
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
        'time-zone',
    )

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgiref.inmemory.ChannelLayer',
            # 'BACKEND': 'asgi_redis.RedisChannelLayer',
            'ROUTING': 'app.routing.channel_routing',
            # 'CONFIG': {
            #     'hosts': [('localhost', 6379)],
            # },
        },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': 'djdb',
    #         'USER': 'djuser',
    #         'PASSWORD': 'p455w0rd',
    #         'HOST': 'localhost',
    #         'PORT': '5432',
    #     },
    # }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'djdb',
    #         'USER': 'djuser',
    #         'PASSWORD': 'p455w0rd',
    #         'HOST': 'localhost',
    #         'PORT': '3306',
    #         'OPTIONS': {
    #             'init_command': 'SET sql_mode=\'STRICT_TRANS_TABLES\'',
    #         }
    #     }
    # }

    AUTH_TOKEN_EXPIRE = 316224000 # 10 years

    SIGNUP_CODE_EXPIRE = 600 # 10 minutes
    SIGNUP_EMAIL_USE_LIMIT = 5 # 5 times

    PASSWD_RESET_TOKEN_EXPIRE = 600 # 10 minutes
    PASSWD_RESET_URL = 'http://localhost:8000/accounts/me/passwd/reset'

    # Firebase Cloud Messaging
    FCM_TOKEN = 'AAAAcA3b7Is:APA91bFOjWJKMDljaXTgiSw_CYHdpo7yY-GRTzq0kG8eo_f75LCLtM1YC0EH-ZW_VzoQnxbYQxSraMiQ-8oUhMC__gM46igqOrN9hEgZlQZeWovWg4hiobIa_1j9PNq8v3fGOAVGpxbu'
    FCM_SENDER_ID = '481268853899'
    FCM_URL = 'https://fcm.googleapis.com/fcm/send'
    FCM_DEFAULT_ICON = '/images/fcm.png'

    # Celery: Distributed Task Queue
    CELERY_BROKER_URL = 'sqla+sqlite:///celery.sqlite3'
    CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite3'

    CELERY_BEAT_SCHEDULE = {
        'run-every-minute': {
            'task': 'common.tasks.add',
            'schedule': crontab(),
            'args': (2, 5),
        },
    }
    CELERY_BEAT_SCHEDULER = 'celery.beat:PersistentScheduler'
    CELERY_BEAT_SCHEDULE_FILENAME = 'schedule.db'


class ExampleEnv(Env):
    """Example env"""

    DEBUG = True


class ProductionEnv(Env):
    """Production env"""

    DEBUG = False


envs = {
    'example': ExampleEnv,
    'production': ProductionEnv,
}

env = envs.get(os.environ.get(
    'ENV_NAME') or socket.gethostname(), Env)()

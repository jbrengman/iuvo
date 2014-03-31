"""
Django settings for iuvo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from configurations import Configuration, values
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '9mh305v5ku%5m&_7gb4m+(3)v_*)9^uu+)8!@g=j2_)3g3en@7'

    ALLOWED_HOSTS = []

    # Application definition
    DEFAULT_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'south',
        'bootstrap3',
        'registration',
        'django_crontab',
    )

    LOCAL_APPS = (
        'iuvo_app',
    )

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    ACCOUNT_ACTIVATION_DAYS = 3

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'user@gmail.com'
    EMAIL_HOST_PASSWORD = 'secret'
    DEFAULT_FROM_EMAIL = 'user@gmail.com'
    EMAIL_PORT = 587

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'iuvo.urls'

    WSGI_APPLICATION = 'iuvo.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'iuvodb',
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

     # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_URL = '/static/'

    # run "python manage.py crontab add" to add jobs to crontab
    # run "python manage.py crontab remove" to remove jobs
    CRONJOBS = [
        ('*/5 * * * *', 'iuvo.iuvo_app.cron.my_scheduled_job')
    ]


class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    INSTALLED_APPS = Base.INSTALLED_APPS + ('debug_toolbar',)

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Prod(Base):
    pass

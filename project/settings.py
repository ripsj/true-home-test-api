import os
import datetime
from .core.applist import *
from .core.internationalization import *
from .core.mediafiles import *

def getenvar(name):
    """Get the environment variable or return exception."""
    try:
        val = os.environ.get(name)
        # print('Variable', name)
        # print(val)
        if val == 'True':
            val = True
        if val == 'False':
            val = False

        return val
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(name)
        raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenvar('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenvar('DEBUG')

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

APPNAME = getenvar('APPNAME')

# AUTH_USER_MODEL
AUTH_USER_MODEL = 'security.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=7),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'project.common.exception_handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'project.common.pagination.PageNumberPagination',
    'PAGE_SIZE': getenvar('PAGE_SIZE'),
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': getenvar('DB_HOST'),
        'NAME': getenvar('DB_NAME'),
        'USER': getenvar('DB_USER'),
        'PASSWORD': getenvar('DB_PASSWORD'),
        'PORT': getenvar('DB_PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
AWS_ENABLE = getenvar('AWS_ENABLE')

if AWS_ENABLE:
    # S3_BUCKET = "zappa-putwja4zp"
    # STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    # # AWS_ACCESS_KEY_ID = 'AKIARJVAAG3YLVGJWOVY'
    # # AWS_SECRET_ACCESS_KEY = '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'
    # AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET
    # STATIC_URL = "https://%s.s3.amazonaws.com/" % S3_BUCKET

    print('use aws s3')
    # AWS_DEFAULT_ACL = None

    AWS_ACCESS_KEY_ID = getenvar('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = getenvar('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = getenvar('AWS_STORAGE_BUCKET_NAME')
    AWS_CLOUD_FRONT_URL = getenvar('AWS_CLOUD_FRONT_URL')
    AWS_REGION = getenvar('AWS_REGION')

    if AWS_CLOUD_FRONT_URL:
        AWS_S3_CUSTOM_DOMAIN = '%s' % AWS_CLOUD_FRONT_URL
    else:
        AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_ENCRYPTION = True

    # Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_BUCKET_NAME_STATIC = getenvar('AWS_STORAGE_BUCKET_NAME')

    if AWS_CLOUD_FRONT_URL:
        STATIC_URL = "https://%s/" % (AWS_CLOUD_FRONT_URL)
    else:
        STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME)

    # Media files
    DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

else:
    print('local files')
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ORIGIN_ALLOW_ALL = True 
SITE_ID = 1

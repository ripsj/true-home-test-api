__DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
)
__OWN_APPS = (
    'project.core',
    # apps created
    'project.apps.security',
    'project.apps.posts',
    'project.apps.categories',
)
__THIRD_PARTY_APPS = (
    'django_s3_storage',
    'rest_framework',
)
INSTALLED_APPS = __DJANGO_APPS + __OWN_APPS + __THIRD_PARTY_APPS

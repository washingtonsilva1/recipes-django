import os
from pathlib import Path
from utils.utils import parse_str_to_list


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = parse_str_to_list(
    os.environ.get('ALLOWED_HOSTS', ''),
    ','
)
CSRF_TRUSTED_ORIGINS = parse_str_to_list(
    os.environ.get('CSRF_TRUSTED_ORIGINS', ''),
    ','
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PAGINATION SETTINGS
RECIPES_PER_PAGE = int(os.environ.get('RECIPES_PER_PAGE'))
PAGES_TO_DISPLAY = int(os.environ.get('PAGES_TO_DISPLAY'))

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

from .middleware import MIDDLEWARE
from .installed_apps import INSTALLED_APPS


INSTALLED_APPS = [
    'debug_toolbar',
] + INSTALLED_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]

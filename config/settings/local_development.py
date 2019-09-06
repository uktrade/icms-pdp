from .non_prod_base import *  # NOQA”
import environ
import os

env = environ.Env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # NOQA”
    }
}

# Debug toolbar config
INTERNAL_IPS = ('127.0.0.1', 'localhost')
INSTALLED_APPS += [  # NOQA
    'debug_toolbar',
    'livereload'
]

MIDDLEWARE += [  # NOQA
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'livereload.middleware.LiveReloadScript',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda x: True
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('ICMS_SECRET_KEY', default='development')
DEBUG = env.bool('ICMS_DEBUG', True)

# Email
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', '')
EMAIL_FROM = env.str('ICMS_EMAIL_FROM',
                     'enquiries.ilb@icms.trade.dev.uktrade.io')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} - {message} [{module}]',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'web': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}

LIVERELOAD_HOST = "0.0.0.0"
LIVERELOAD_PORT = 35729


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'webpack_bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),  # NOQA”
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

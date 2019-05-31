from Drman.settings.base import *

DEBUG = False

SECRET_KEY = 'na1)zp34m0hov&*38y_7di1=&025rp)g=c9013tiwl6ch4=w6d'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['193.176.242.97']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}






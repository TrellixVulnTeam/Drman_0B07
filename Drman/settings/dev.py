from Drman.settings.base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'na1)zp34m0hov&*38y_7di1=&025rp)g=c9013tiwl6ch4=w6d'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

#SiteMap
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

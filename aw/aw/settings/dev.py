from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ugv6@a^=o)@fjjkla)aw_%wolhj&dhaz8cb^9=mom!3yvk3k%*"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'site.crs@yandex.ru'
EMAIL_HOST_PASSWORD = 'cr$2023'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL ='site.crs@yandex.ru'
EMAIL_TO = 'sk@i-fabrika.kz'




try:
    from .local import *
except ImportError:
    pass

SECRET_KEY = 'i#%ew3j&g9fg*p++n$5=f*=ko)2=2=m-e)(7fl@pjg$c=wb=w%'

DEBUG = False

ALLOWED_HOSTS = ['188.40.166.185']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bidilo',
        'USER': 'bidilouser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

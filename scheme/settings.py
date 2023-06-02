from pathlib import Path


BASE_DIR       = Path(__file__).resolve().parent.parent
SECRET_KEY     = 'django-insecure-a@z!v*k0_u5*%fp(ix9l=7g59z12hi)bgjnq1l-_61*q!u3@cx'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Scheme
    'circles.apps.CirclesConfig',
    'signals.apps.SignalsConfig',
    'spaces.apps.SpacesConfig',
    'tasks.apps.TasksConfig',
    'user.apps.UserConfig',
    'home.apps.HomeConfig',
    # Third Party
    'rest_framework',
    'mptt'
]

MIDDLEWARE     = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES      = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "html" ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'filters':'helpers.filters',
            }
        },
    },
]

# Database

DATABASES          = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Web

DEBUG            = True
ROOT_URLCONF     = 'scheme.urls'
WSGI_APPLICATION = 'scheme.wsgi.application'
ALLOWED_HOSTS    = [
    '127.0.0.1',
    '192.168.1.10',
    '192.168.1.24'
]
AUTH_USER_MODEL  = 'user.Account'

# Password validation

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

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Africa/Cairo'
USE_I18N      = True
USE_TZ        = True

# Messages

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS    = [
    BASE_DIR / 'static',
]

STATIC_URL          = '/static/'
STATIC_ROOT         = 'scheme'

MEDIA_URL           = '/media/'
MEDIA_ROOT          = BASE_DIR / 'media'
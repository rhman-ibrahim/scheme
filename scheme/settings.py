from pathlib import Path


BASE_DIR       = Path(__file__).resolve().parent.parent
SECRET_KEY     = 'django-insecure-a@z!v*k0_u5*%fp(ix9l=7g59z12hi)bgjnq1l-_61*q!u3@cx'

DEBUG            = True

ALLOWED_HOSTS    = [
    '192.168.43.110', # Hostspot
    '192.168.1.15',   # Wi-Fi
    '127.0.0.1',      # localhost
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Scheme
    'user.apps.UserConfig',
    'mate.apps.MateConfig',
    'team.apps.TeamConfig',
    'ping.apps.PingConfig',
    'home.apps.HomeConfig',
    # reset framework
    'dapi.apps.DapiConfig',
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    # Third Party
    'corsheaders',
    'channels',
    'mptt',
]

MIDDLEWARE     = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF     = 'scheme.urls'

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
                # Scheme
                'team.processors.space'
            ],
            # Scheme
            'libraries':{
                'filters':'helpers.filters'
            }
        },
    },
]

# Web
WSGI_APPLICATION = 'scheme.wsgi.application'

# Database
DATABASES          = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS    = [
    BASE_DIR / 'static',
    BASE_DIR / 'ping/static',
    BASE_DIR / 'user/static'
]

STATIC_URL          = '/static/'
STATIC_ROOT         = 'scheme'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# User
AUTH_USER_MODEL  = 'user.Account'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ASGI
ASGI_APPLICATION = 'scheme.asgi.application'

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG":
        {
            "hosts": [
                (
                    "localhost",
                    6379
                )
            ],
        },
    },
}

# API
REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'dapi.models.SchemeToken',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
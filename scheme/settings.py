from pathlib import Path
from datetime import timedelta

BASE_DIR         = Path(__file__).resolve().parent.parent
SECRET_KEY       = 'django-insecure-a@z!v*k0_u5*%fp(ix9l=7g59z12hi)bgjnq1l-_61*q!u3@cx'
DEBUG            = True
ALLOWED_HOSTS    = [
    '3850-197-48-58-83.ngrok-free.app'
]

INSTALLED_APPS   = [
    
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
    # 'rest_framework.authtoken',
    
    # JWT
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    # Third Party
    'corsheaders',
    'channels',
    'mptt',
]

MIDDLEWARE       = [
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

TEMPLATES        = [
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
DATABASES        = {
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
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'Africa/Cairo'
USE_I18N         = True
USE_TZ           = True

# Static files (CSS, JavaScript, Images)
STATICFILES_DI   = [
    BASE_DIR / 'static',
    BASE_DIR / 'ping/static',
    BASE_DIR / 'user/static'
]

STATIC_URL       = '/static/'
STATIC_ROOT      = 'scheme'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL  = 'user.Account'
MESSAGE_STORAGE  = 'django.contrib.messages.storage.session.SessionStorage'
ASGI_APPLICATION = 'scheme.asgi.application'

# CORS
CORS_ORIGIN_ALLOW_ALL   = False
CORS_ALLOW_CREDENTIALS  = True
CORS_ORIGIN_WHITELIST   = [
    'https://6bba-197-48-58-83.ngrok-free.app'
]
CORS_ALLOWED_ORIGINS    = [
    'https://6bba-197-48-58-83.ngrok-free.app'
]
CORS_EXPOSE_HEADERS = [
    'Set-Cookie',
]

# CSRF
# CSRF_COOKIE_SECURE      = False
# CSRF_COOKIE_SAMESITE    = None
# CSRF_COOKIE_HTTPONLY    = False

# SESSION_COOKIE_SECURE   = False
# SESSION_COOKIE_HTTPONLY = False
# SESSION_COOKIE_SAMESITE = None
# SESSION_COOKIE_DOMAIN   = '6bba-197-48-58-83.ngrok-free.app'

# Channels
CHANNEL_LAYERS   = {
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
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'dapi.models.SchemeToken',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# JWT

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}
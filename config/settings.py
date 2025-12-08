"""
Django settings for config project.
"""

from pathlib import Path
import environ
import os
import dj_database_url

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists locally
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', 'auth.oneclickmed.ng', '.vercel.app']
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # Local apps
    'auth_service',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auth_service.middleware.ProductAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication',],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated',],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer',],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser',],
    'EXCEPTION_HANDLER': 'auth_service.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': env('RATE_LIMIT_PER_MINUTE', default='60/minute'),
        'user': env('RATE_LIMIT_PER_HOUR', default='1000/hour'),
    }
}

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'https://oneclickmed.ng',
    'https://www.oneclickmed.ng',
    'https://auth.oneclickmed.ng',
])
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
]

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https://oneclickmed.ng", "https://*.oneclickmed.ng")
CSP_FONT_SRC = ("'self'",)

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

BACKEND_URL = env('BACKEND_URL', default='https://auth.oneclickmed.ng')

# Brevo & HubSpot
BREVO_API_KEY = env('BREVO_API_KEY', default='')
BREVO_SENDER_EMAIL = env('BREVO_SENDER_EMAIL', default='')
BREVO_SENDER_NAME = env('BREVO_SENDER_NAME', default='OCM Services')
HUBSPOT_API_KEY = env('HUBSPOT_API_KEY', default='')

# Firebase configs (env variables)
FIREBASE_TEST_CONFIG = {key: env(key, default='') for key in [
    'FIREBASE_TEST_TYPE', 'FIREBASE_TEST_PROJECT_ID', 'FIREBASE_TEST_PRIVATE_KEY_ID',
    'FIREBASE_TEST_PRIVATE_KEY', 'FIREBASE_TEST_CLIENT_EMAIL', 'FIREBASE_TEST_CLIENT_ID',
    'FIREBASE_TEST_AUTH_URI', 'FIREBASE_TEST_TOKEN_URI', 'FIREBASE_TEST_AUTH_PROVIDER_CERT_URL',
    'FIREBASE_TEST_CLIENT_CERT_URL'
]}
FIREBASE_PROD_CONFIG = {key: env(key, default='') for key in [
    'FIREBASE_PROD_TYPE', 'FIREBASE_PROD_PROJECT_ID', 'FIREBASE_PROD_PRIVATE_KEY_ID',
    'FIREBASE_PROD_PRIVATE_KEY', 'FIREBASE_PROD_CLIENT_EMAIL', 'FIREBASE_PROD_CLIENT_ID',
    'FIREBASE_PROD_AUTH_URI', 'FIREBASE_PROD_TOKEN_URI', 'FIREBASE_PROD_AUTH_PROVIDER_CERT_URL',
    'FIREBASE_PROD_CLIENT_CERT_URL'
]}

# Products config
PRODUCTS_CONFIG = {
    'beta_health': {'name': 'Beta Health', 'test_tenant_id': env('BETA_HEALTH_TEST_TENANT_ID', ''), 'prod_tenant_id': env('BETA_HEALTH_PROD_TENANT_ID', '')},
    'ehr': {'name': 'EHR', 'test_tenant_id': env('EHR_TEST_TENANT_ID', ''), 'prod_tenant_id': env('EHR_PROD_TENANT_ID', '')},
    'emergency_service': {'name': 'Emergency Service', 'test_tenant_id': env('EMERGENCY_SERVICE_TEST_TENANT_ID', ''), 'prod_tenant_id': env('EMERGENCY_SERVICE_PROD_TENANT_ID', '')},
}

# Logging - console only
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': os.environ.get('LOG_LEVEL', 'INFO'), 'propagate': False},
        'auth_service': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

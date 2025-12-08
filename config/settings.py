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

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', 'auth.oneclickmed.ng', '.vercel.app'])

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




DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
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

# CORS Settings
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'https://oneclickmed.ng',
    'https://www.oneclickmed.ng',
    'https://auth.oneclickmed.ng',
])
CORS_ALLOW_CREDENTIALS = True

# Allow all localhost/127.0.0.1 origins for local development
# Since we use token authentication, this is safe
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
]

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
# Note: 'unsafe-inline' is needed for our branded HTML pages with inline styles
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https://oneclickmed.ng", "https://*.oneclickmed.ng")
CSP_FONT_SRC = ("'self'",)

# HTTPS Settings (uncomment for production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Backend URL Configuration
BACKEND_URL = env('BACKEND_URL', default='https://auth.oneclickmed.ng')

# Brevo Configuration
BREVO_API_KEY = env('BREVO_API_KEY', default='')
BREVO_SENDER_EMAIL = env('BREVO_SENDER_EMAIL', default='')
BREVO_SENDER_NAME = env('BREVO_SENDER_NAME', default='OCM Services')

# HubSpot Configuration (for Beta Health newsletter)
HUBSPOT_API_KEY = env('HUBSPOT_API_KEY', default='')

# Firebase Configuration
# Firebase credentials stored as individual environment variables
FIREBASE_TEST_CONFIG = {
    'type': env('FIREBASE_TEST_TYPE', default='service_account'),
    'project_id': env('FIREBASE_TEST_PROJECT_ID', default=''),
    'private_key_id': env('FIREBASE_TEST_PRIVATE_KEY_ID', default=''),
    'private_key': env('FIREBASE_TEST_PRIVATE_KEY', default=''),
    'client_email': env('FIREBASE_TEST_CLIENT_EMAIL', default=''),
    'client_id': env('FIREBASE_TEST_CLIENT_ID', default=''),
    'auth_uri': env('FIREBASE_TEST_AUTH_URI', default='https://accounts.google.com/o/oauth2/auth'),
    'token_uri': env('FIREBASE_TEST_TOKEN_URI', default='https://oauth2.googleapis.com/token'),
    'auth_provider_x509_cert_url': env('FIREBASE_TEST_AUTH_PROVIDER_CERT_URL', default='https://www.googleapis.com/oauth2/v1/certs'),
    'client_x509_cert_url': env('FIREBASE_TEST_CLIENT_CERT_URL', default=''),
}

FIREBASE_PROD_CONFIG = {
    'type': env('FIREBASE_PROD_TYPE', default='service_account'),
    'project_id': env('FIREBASE_PROD_PROJECT_ID', default=''),
    'private_key_id': env('FIREBASE_PROD_PRIVATE_KEY_ID', default=''),
    'private_key': env('FIREBASE_PROD_PRIVATE_KEY', default=''),
    'client_email': env('FIREBASE_PROD_CLIENT_EMAIL', default=''),
    'client_id': env('FIREBASE_PROD_CLIENT_ID', default=''),
    'auth_uri': env('FIREBASE_PROD_AUTH_URI', default='https://accounts.google.com/o/oauth2/auth'),
    'token_uri': env('FIREBASE_PROD_TOKEN_URI', default='https://oauth2.googleapis.com/token'),
    'auth_provider_x509_cert_url': env('FIREBASE_PROD_AUTH_PROVIDER_CERT_URL', default='https://www.googleapis.com/oauth2/v1/certs'),
    'client_x509_cert_url': env('FIREBASE_PROD_CLIENT_CERT_URL', default=''),
}

# Product Configurations
# Tokens are auto-generated via DRF when running: python manage.py populate_products
PRODUCTS_CONFIG = {
    'beta_health': {
        'name': 'Beta Health',
        'test_tenant_id': env('BETA_HEALTH_TEST_TENANT_ID', default=''),
        'prod_tenant_id': env('BETA_HEALTH_PROD_TENANT_ID', default=''),
    },
    'ehr': {
        'name': 'EHR',
        'test_tenant_id': env('EHR_TEST_TENANT_ID', default=''),
        'prod_tenant_id': env('EHR_PROD_TENANT_ID', default=''),
    },
    'emergency_service': {
        'name': 'Emergency Service',
        'test_tenant_id': env('EMERGENCY_SERVICE_TEST_TENANT_ID', default=''),
        'prod_tenant_id': env('EMERGENCY_SERVICE_PROD_TENANT_ID', default=''),
    },
}

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': env('LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'auth_service': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

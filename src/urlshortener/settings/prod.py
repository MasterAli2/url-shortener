from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.friendlyfish.dev']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT', '5432'),
    }
}

# HTTPS
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Clickjacking
X_FRAME_OPTIONS = 'DENY'

# Content sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS filter
SECURE_BROWSER_XSS_FILTER = True

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

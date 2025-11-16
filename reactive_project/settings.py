"""
Django settings for reactive_project project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-development-key-123456789'


DEBUG = os.environ.get('DEBUG', 'True') == 'True'

if not DEBUG:
    # Настройки для продакшн
    ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'server-ip-address']
    
    # Настройки для статических файлов
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Безопасность
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-here')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    # Настройки для разработки
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = 'django-insecure-development-key-123456789'


ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',  # Добавляем админку
    'django.contrib.auth',   # Добавляем аутентификацию
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'button_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Для админки
    'django.contrib.messages.middleware.MessageMiddleware',     # Для админки
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reactive_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',    # Для админки
                'django.contrib.messages.context_processors.messages',  # Для админки
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Добавляем настройки аутентификации
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Channels configuration
ASGI_APPLICATION = 'reactive_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
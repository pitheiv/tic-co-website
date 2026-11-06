"""
Django settings for config project.
Chạy được trên máy (local), PythonAnywhere và Render.
"""

import os
from pathlib import Path

try:
    import dj_database_url
except ImportError:          # chạy SQLite thì không cần thư viện này
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------
# MÔI TRƯỜNG: "PRODUCTION" (đặt trong file WSGI của PythonAnywhere)
# hoặc "RENDER" (Render tự đặt) nghĩa là đang chạy trên mạng thật.
# ---------------------------------------------------------------
PRODUCTION = bool(os.environ.get("PRODUCTION") or os.environ.get("RENDER"))

# Khóa bí mật: trên mạng thật PHẢI đặt biến SECRET_KEY.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-chi-dung-tren-may-ban-khong-dung-khi-ban-hang-that",
)

DEBUG = not PRODUCTION

# Đổi "tenban" thành tên tài khoản PythonAnywhere của bạn
PYTHONANYWHERE_HOST = "tenban.pythonanywhere.com"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", PYTHONANYWHERE_HOST]
CSRF_TRUSTED_ORIGINS = [f"https://{PYTHONANYWHERE_HOST}"]

if not PRODUCTION:
    ALLOWED_HOSTS.append("*")   # để điện thoại cùng WiFi vào xem khi chạy trên máy

render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")


# ---------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'store',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------------------------------------------------------
# Database: mặc định SQLite; nếu có biến DATABASE_URL thì dùng PostgreSQL
# ---------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get("DATABASE_URL") and dj_database_url:
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)


# ---------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------
# Ngôn ngữ và múi giờ
# ---------------------------------------------------------------
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------
# File tĩnh (CSS, ảnh, video) và file upload (ảnh món)
# ---------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ---------------------------------------------------------------
# Email (mặc định in ra terminal)
# ---------------------------------------------------------------
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
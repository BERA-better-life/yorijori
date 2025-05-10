import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv



# BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# .env 파일 로드
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 보안을 위해 새로운 SECRET_KEY 생성 (실제 운영에서는 환경 변수로 관리 권장) + .env 없을 때도 기본 키 자동 생성
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# DEBUG 모드 설정 (운영 환경에서는 False로 설정해야 함)
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# ALLOWED_HOSTS 설정 (배포 시 도메인 추가 필요) 
ALLOWED_HOSTS = ALLOWED_HOSTS = ['*'] # 0503 배포용 os.getenv("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1").split()

AUTH_USER_MODEL = 'users.Users'
# MySQL 데이터베이스 설정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yorijori_db',
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION',
        },
    }
}

# INSTALLED_APPS (기본 앱 + 추가 앱 설정)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 추가 앱 (예: 'yorijori' 프로젝트 앱)
    'yorijori',
    'recipes',    
    'rest_framework',
    'favorite',
    'notification', 
    'users',
    'ingredients',
    'shopping',

    
]

# MIDDLEWARE 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL 설정
ROOT_URLCONF = 'yorijori.urls'

# WSGI 애플리케이션
WSGI_APPLICATION = 'yorijori.wsgi.application'

# STATIC & MEDIA 설정
URL = '/static/'
MEDIA_URL = '/media/'
#STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = BASE_DIR / "media"

# TIME_ZONE & LANGUAGE 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DEFAULT_AUTO_FIELD 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import pymysql
pymysql.install_as_MySQLdb()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "user_id",
}

# 정적 파일 설정 추가
STATIC_URL = '/static/'
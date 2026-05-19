# =============================================
# restaurant_project/config.py
# =============================================

import os
from pathlib import Path

from dotenv import load_dotenv

# =============== SECRET KEYS & CONFIG ===============


# Generate a strong secret key and keep it safe
SECRET_KEY = 'django-insecure-8^h!2+m=d6)j5+g(js9(g1w^6+_8p_g$e@lpohn!i+#11nmhdp'

# =============== DEVELOPMENT / PRODUCTION ===============

# 3. SET TO FALSE FOR PRODUCTION
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '187.77.180.249']

# =============== DATABASE (Optional) ===============

DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3'),
}

# =============== PRODUCTION SETTINGS (when DEBUG=False) ===============

if not DEBUG:
    ALLOWED_HOSTS = ['infowavesandwings.co.uk', 'www.infowavesandwings.co.uk', '.infowavesandwings.co.uk', 'infowavesandwings', "srv1673913.hstgr.cloud", "187.77.180.249"]

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load the environment variables from the .env file
    load_dotenv(os.path.join(BASE_DIR, '.env'))

    # Secure your Django Secret Key
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

    # --- ADD THESE NEW SECURITY LINES ---

    # # 1. Force cookies to only be sent over HTTPS
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    #
    # # 2. Tell Django to force HTTPS routing
    # SECURE_SSL_REDIRECT = True
    #
    # # 3. Enable Strict Transport Security (HSTS) for 1 year
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    #
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# =============== OTHER IMPORTANT SETTINGS ===============

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'menu')
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
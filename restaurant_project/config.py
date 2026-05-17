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
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # 2. Load the environment variables from the .env file
    load_dotenv(os.path.join(BASE_DIR, '.env'))

    # 3. Secure your Django Secret Key
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    DEBUG = False
    ALLOWED_HOSTS = ['infowavesandwings.co.uk', 'www.infowavesandwings.co.uk', '.infowavesandwings.co.uk', 'infowavesandwings']


# =============== OTHER IMPORTANT SETTINGS ===============

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'menu')
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
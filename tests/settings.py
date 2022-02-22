# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = False
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "d_80986zfpyi+wzj4xmk&^3oxas)ns-^ap^ev9gvs5a8#@$s#d"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = []

ALLOWED_HOSTS = [
    "thedude.abides.com",
    ".lebowski.biz",
]
ALLOWED_CIDR_NETS = [
    "192.168.1.0/24",
    "192.168.2.0/24",
]

SITE_ID = 1

MIDDLEWARE = ("allow_cidr.middleware.AllowCIDRMiddleware",)
if django.VERSION < (1, 10):
    MIDDLEWARE_CLASSES = MIDDLEWARE

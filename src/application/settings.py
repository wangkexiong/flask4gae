# -*- coding: utf-8 -*-

"""
Configuration for Flask app

Important: Place your keys in the secret_keys.py module,
           which should be kept out of version control.
"""

import os

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY

## Auto-set debug mode based on App Engine dev environ
DEBUG_MODE = False

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

## Set secret keys for CSRF protection
CSRF_ENABLED = True

SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_KEY = SESSION_KEY

## Cache Type
CACHE_TYPE = 'gaememcached'


## CDNJS default configuration
#JS_USE_MINIFIED = True
#JS_USE_CDN = True
#CDN_PREFER_SSL = True
#CDN_BASEURL = '//cdnjs.cloudflare.com/ajax/libs/'
GOOGLE_ANALYTICS_ACCOUNT = 'wangkexiong@gmail.com'

## Debug purpose
if DEBUG:
    JS_USE_MINIFIED = False
    JS_USE_CDN = False

    DEBUG_TB_PROFILER_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False

## Testing only

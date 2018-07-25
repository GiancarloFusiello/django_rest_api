"""
Settings file for prodution specific settings
"""
from .base import *

DEBUG = False

# In real life production, pass the values via an environment variable
ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost',
    'gfusiello.pythonanywhere.com'
]

REST_FRAMEWORK.update({
    # disable the browser api view
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
})

# Add production database settings here

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SERVER
HOST='0.0.0.0'
PORT=8001

SECRET_KEY='secret'

ALLOWED_HOSTS = [
    '*'
]

#List of all modules use in the app.
#Primarily used by celery to find all tasks.
INSTALLED_APPS = [
    'src.modules.hive_db'
]


try:
    from .local_settings import *
except ImportError:
    pass

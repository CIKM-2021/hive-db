import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SERVER
HOST='0.0.0.0'
PORT=8001

SECRET_KEY='WrrXP6szu06wlLQVfAM3b0FD8i4612zc'

ALLOWED_HOSTS = [
    '*'
]

#List of all modules use in the app.
#Primarily used by celery to find all tasks.
INSTALLED_APPS = [
    'src.modules.hive_db'
]

GOOGLE_KEY_FILE = '.env/Steemit-e706b5b8cead.json'

try:
    from .local_settings import *
except ImportError:
    pass

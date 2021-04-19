from google.oauth2 import service_account

from . import settings


def get_credentials():
    return service_account.Credentials.from_service_account_file(
            settings.GOOGLE_KEY_FILE,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

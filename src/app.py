import falcon

from falcon_cors import CORS
from logbook import Logger

from .middleware.permissions import APIPermission
from .conf import settings
from .hive_db.views.accounts import TestResourceView, AccountView


logger = Logger(__name__)


def create_app():
    cors = CORS(allow_origins_list=settings.ALLOWED_HOSTS)
    middlewares = [cors.middleware, APIPermission()]
    app = falcon.App(middleware=middlewares)
    app.add_route(f"/{settings.PREFIX}/test", TestResourceView())
    app.add_route(f"/{settings.PREFIX}/accounts", AccountView())
    return app


app = application = create_app()

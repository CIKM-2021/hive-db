import falcon
from falcon_cors import CORS
from logbook import Logger
# from apispec import APISpec
# from apispec.ext.marshmallow import MarshmallowPlugin
# from falcon_apispec import FalconPlugin
# from marshmallow import Schema, fields

from .middleware.permissions import APIPermission
from .conf import settings
from .hive_db.views.accounts import TestResourceView, AccountView
from .hive_db.views.blocks import BlockView
from .hive_db.views.comments import CommentView
from .hive_db.views.posts import PostView

logger = Logger(__name__)


def create_app():
    cors = CORS(allow_origins_list=settings.ALLOWED_HOSTS)
    middlewares = [cors.middleware, APIPermission()]
    app = falcon.API(middleware=middlewares)
    app.add_route(f"/{settings.PREFIX}/test", TestResourceView())
    app.add_route(f"/{settings.PREFIX}/accounts", AccountView())
    app.add_route(f"/{settings.PREFIX}/blocks", BlockView())
    app.add_route(f"/{settings.PREFIX}/comments", CommentView())
    app.add_route(f"/{settings.PREFIX}/posts", PostView())
    return app


app = application = create_app()

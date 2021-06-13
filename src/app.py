import falcon
from falcon_cors import CORS
from logbook import Logger
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend, TokenAuthBackend
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
from .hive_db.views.statistics import TopPostView, TopCommentView, TopWordView


logger = Logger(__name__)


# user_loader = lambda username, password: { 'username': username }
# auth_backend = TokenAuthBackend(None, auth_header_prefix='TOKEN')
# auth_middleware = FalconAuthMiddleware(auth_backend,
#                     exempt_routes=[f"/{settings.PREFIX}/top_posts"], exempt_methods=['HEAD'])
# api = falcon.API(middleware=[auth_middleware])



def create_app():
    cors = falcon.CORSMiddleware(allow_origins='*', allow_credentials='*')
    middlewares = [cors, APIPermission()]
    app = falcon.App(middleware=middlewares)
    app.add_route(f"/{settings.PREFIX}/test", TestResourceView())
    app.add_route(f"/{settings.PREFIX}/accounts", AccountView())
    app.add_route(f"/{settings.PREFIX}/blocks", BlockView())
    app.add_route(f"/{settings.PREFIX}/comments", CommentView())
    app.add_route(f"/{settings.PREFIX}/posts", PostView())
    app.add_route(f"/{settings.PREFIX}/top_posts", TopPostView())
    app.add_route(f"/{settings.PREFIX}/top_comments", TopCommentView())
    app.add_route(f"/{settings.PREFIX}/top_words", TopWordView())

    return app


app = application = create_app()

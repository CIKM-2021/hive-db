import falcon
import json
from logbook import Logger
from google.cloud import bigquery
from google.oauth2 import service_account

from ..queries import AccountQuery
from ...core.resource import BaseResource
from ...conf import settings
from ...conf.clients import get_credentials


logger = Logger(__name__)


class TestResourceView(BaseResource):
    def on_get(self, req, resp):
        q = req.get_param('q')
        print(type(req))
        logger.info('param in query {}', q)
        self.ok(resp, {'message': f'here on get {q}'})


class AccountView(BaseResource):

    def on_get(self, req, resp):
        query = AccountQuery()
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        sql = query.get_head()
        result = client.query(sql).to_dataframe().to_json()
        self.ok(resp, result)

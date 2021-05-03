import falcon
import json
from google.cloud import bigquery

from ...core.resource import BaseResource
from ...conf import settings

credentials = service_account.Credentials.from_service_account_file(
    settings.GOOGLE_KEY_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

class TestResourceView(BaseResource):

    def on_get(self, req, resp):
        self.ok(resp, {'message': 'here on get'})


class AccountView(BaseResource):

    def on_get(self, req, resp):
        client = bigquery.Client(credentials=settings.CREDENTIALS, project=settings.CREDENTIALS.project_id)
        sql = """
            WITH data AS (
            SELECT
                accounts.blog_history as blogs
            FROM `steemit-307308.hive.scrape`
            )
            SELECT blogs
            FROM data
            LIMIT 5
            """

        result = client.query(sql).to_dataframe().to_json()
        self.ok(resp, result)


class CommentView(BaseResource):
    pass


class PostView(BaseResource):
    pass

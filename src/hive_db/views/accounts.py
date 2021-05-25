import os
import falcon
import ujson
from logbook import Logger
from google.cloud import bigquery
from google.oauth2 import service_account

# from ..queries import AccountQuery
from ...core.resource import BaseResource
from ...conf import settings
from ...conf.clients import get_credentials


logger = Logger(__name__)


class TestResourceView(BaseResource):
    def on_get(self, req, resp):
        q = req.get_param('q')
        logger.info('param in query {}', q)
        # self.ok(resp, {'message': f'here on get {q}'})
        resp.text = f'here on get {q}'


class AccountView(BaseResource):
    def on_get(self, req, resp):
        # query = AccountQuery()
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        limit = req.get_param('limit')
        author = req.get_param('author')
        query = """
            WITH data AS (
            SELECT
                accounts.blog_history as blogs
            FROM `steemit-307308.hive.scrape`
            )
            SELECT blogs
            FROM data
            LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('limit', 'INT64', limit),
            ]
        )
        query_job = client.query(query, job_config=job_config)
        json_results = ujson.loads(query_job.to_dataframe().to_json())
        response = {'blog_history': []}
        if limit:
            logger.info('Filtering by limit params: {}'.format(limit))
            useful_fields = ['author', 'body', 'url', 'permlink', 'post_id']
            for row in range(int(limit)):
                temp_dict = {}
                for field in useful_fields:
                    temp_dict[field] = json_results['blogs']['0'][row][field]
                response['blog_history'].append(temp_dict)
        if author:
            logger.info('Filtering by author params: {}'.format(author))
            filtered_resp = []
            for blog in response['blog_history']:
                if blog['author'] == author:
                    filtered_resp.append(blog)
            response['blog_history'] = filtered_resp
        # for row in query_job:
        # json_results = client.query(query, job_config=job_config)
        self.ok(resp, response)

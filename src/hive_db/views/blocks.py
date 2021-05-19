from datetime import datetime

import pytz
import ujson
import pandas as pd
from logbook import Logger
from google.cloud import bigquery

# from ..queries import AccountQuery
from ...core.resource import BaseResource
from ...conf import settings
from ...conf.clients import get_credentials


logger = Logger(__name__)


class BlockView(BaseResource):
    def on_get(self, req, resp):
        # init client
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        # get params
        table = req.get_param('table')
        size = req.get_param('size')
        fields = req.get_param('fields')
        witnesses = req.get_param('witnesses')
        ids = req.get_param('ids')
        block_ids = req.get_param('block_ids')
        before = req.get_param('before')
        after = req.get_param('after')
        operations = req.get_param('operations')

        if fields is not None:
            columns = fields.split(',')
        else:
            columns = ['*']
        if size is None:
            size = 25
        if witnesses:
            witnesses = witnesses.split(',')
        if ids:
            ids = ids.split(',')
        if block_ids:
            block_ids = block_ids.split(',')
        if before and not after:
            if before.isnumeric():
                before = datetime.fromtimestamp(int(before), tz=pytz.UTC)
            after = datetime.fromtimestamp(0, tz=pytz.UTC)
        elif after and not before:
            if after.isnumeric():
                after = datetime.fromtimestamp(int(after), tz=pytz.UTC)
            before = datetime.now()
        elif after and before:
            if after.isnumeric():
                after = datetime.fromtimestamp(int(after), tz=pytz.UTC)
            if before.isnumeric():
                before = datetime.fromtimestamp(int(before), tz=pytz.UTC)
        elif operations:
            operations = operations.split(',')

        if witnesses:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308`.hive.block_01 AS blocks
                WHERE witness IN UNNEST(@witnesses)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ArrayQueryParameter("witnesses", "STRING", witnesses),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif ids:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308`.hive.block_01 AS blocks
                WHERE id IN UNNEST(@ids)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ArrayQueryParameter("ids", "INT64", ids),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif block_ids:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308`.hive.block_01 AS blocks
                WHERE block_id IN UNNEST(@block_ids)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ArrayQueryParameter("block_ids", "STRING", block_ids),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif after or before:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308`.hive.block_01 AS blocks
                WHERE timestamp >= @after AND timestamp <= @before
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter("after", "TIMESTAMP", after),
                    bigquery.ScalarQueryParameter("before", "TIMESTAMP", before),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif operations:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type IN UNNEST(@operations)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("operations", "STRING", operations),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        else:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308`.hive.block_01 AS blocks
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )



        print('table {}'.format(table))
        print('size {}'.format(size))
        print('columns {}'.format(columns))
        print('witnesses {}'.format(witnesses))
        print('ids {}'.format(ids))
        print('block_ids {}'.format(block_ids))
        print('after {}'.format(after))
        print('before {}'.format(block_ids))

        query_job = client.query(query_template, job_config=job_config)

        print(query_job.to_dataframe())
        df_results = query_job.to_dataframe()['f1_']
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)

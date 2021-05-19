import os
from datetime import datetime

import pytz
import ujson
import pandas as pd
from logbook import Logger
from google.cloud import bigquery

from ...core.resource import BaseResource
from ...conf import settings
from ...conf.clients import get_credentials


logger = Logger(__name__)

class CommentView(BaseResource):
    def on_get(self, req, resp):
        # init client
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        # get params
        table = req.get_param('table')
        size = req.get_param('size')
        fields = req.get_param('fields')
        ids = req.get_param('ids')
        block_ids = req.get_param('block_ids')
        witnesses = req.get_param('witnesses')

        before = req.get_param('before')
        after = req.get_param('after')
        authors = req.get_param('authors')
        permlinks = req.get_param('permlinks')
        search = req.get_param('search')

        if fields is not None:
            columns = fields.split(',')
        else:
            columns = ['*']
        if authors:
            authors = authors.split(',')
        if search:
            search = '|'.join(search.split(','))
        if block_ids:
            block_ids = block_ids.split(',')
        if permlinks:
            permlinks = permlinks.split(',')
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

        if witnesses:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type = 'comment_operation'
                    AND witness IN UNNEST(@witnesses)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("witnesses", "STRING", witnesses),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif ids:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type = 'comment_operation'
                    AND id IN UNNEST(@ids)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("ids", "INT64", ids),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif block_ids:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type = 'comment_operation'
                    AND id IN UNNEST(@block_ids)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("block_ids", "INT64", block_ids),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif authors:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE (operations_unnest.type = 'comment_operation')
                    AND (operations_unnest.value.author IN UNNEST(@authors))
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("authors", "STRING", authors),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif permlinks:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE (operations_unnest.type = 'comment_operation')
                    AND (operations_unnest.value.permlink IN UNNEST(@permlinks))
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ArrayQueryParameter("permlinks", "STRING", permlinks),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif search:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE (operations_unnest.type = 'comment_operation')
                    AND REGEXP_CONTAINS(operations_unnest.value.body, @words)
                LIMIT @limit
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("columns", "STRING", columns),
                    bigquery.ScalarQueryParameter('table', 'STRING', table),
                    bigquery.ScalarQueryParameter('words', 'STRING', search),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif after or before:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type = 'comment_operation'
                    AND timestamp >= @after AND timestamp <= @before
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
        else:
            query_template = """
                SELECT @columns, TO_JSON_STRING(blocks)
                FROM `steemit-307308.hive.block_01` AS blocks,
                    UNNEST (transactions) AS transaction_unnest,
                    UNNEST (transaction_unnest.operations) AS operations_unnest
                WHERE operations_unnest.type = 'comment_operation'
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
        print('authors {}'.format(authors))

        query_job = client.query(query_template, job_config=job_config)
        print(query_job.to_dataframe())
        df_results = query_job.to_dataframe()['f1_']
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)

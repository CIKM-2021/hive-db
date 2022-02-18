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
    def __init__(self):
        super().__init__()
        self.dataset = 'hive_zurich'
        self.table = settings.TABLES

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
        post_permlinks = req.get_param('post_permlinks')
        tags = req.get_param('tags')

        before = req.get_param('before')
        after = req.get_param('after')
        authors = req.get_param('authors')
        permlinks = req.get_param('permlinks')
        search = req.get_param('search')

        if fields is not None:
            columns = fields
        else:
            columns = '*'
        if size is None:
            size = 25
        if witnesses:
            witnesses = witnesses.split(',')
        if ids:
            ids = ids.split(',')
        if authors:
            authors = authors.split(',')
        if search:
            search = '|'.join(search.split(','))
        if block_ids:
            block_ids = block_ids.split(',')
        if permlinks:
            permlinks = permlinks.split(',')
        if post_permlinks:
            post_permlinks = permlinks.split(',')
        if tags:
            tags = tags.split(',')
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
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND witness IN UNNEST(@witnesses)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("witnesses", "STRING", witnesses),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif ids:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND id IN UNNEST(@ids)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("ids", "INT64", ids),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif block_ids:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND id IN UNNEST(@block_ids)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("block_ids", "INT64", block_ids),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif authors:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND operations.value.author IN UNNEST(@authors)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("authors", "STRING", authors),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif permlinks:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND operations.value.permlink IN UNNEST(@permlinks)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("permlinks", "STRING", permlinks),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif search:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND REGEXP_CONTAINS(operations.value.body, @words)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter('words', 'STRING', search),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif post_permlinks:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = "" 
                    AND operations.value.parent_permlink IN UNNEST(@post_permlinks)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("post_permlinks", "STRING", post_permlinks),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif tags:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND ARRAY_LENGTH(operations.value.json_metadata_dict.tags_list_str) = 0
                    AND operations.value.json_metadata_dict.tags_list_str[offset(0)] IN UNNEST(@tags)
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("tags", "STRING", tags),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        elif after or before:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                    AND timestamp >= @after AND timestamp <= @before
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("after", "TIMESTAMP", after),
                    bigquery.ScalarQueryParameter("before", "TIMESTAMP", before),
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )
        else:
            query_template = """
                SELECT {columns}
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN '42000001_43245905_01' AND '59567347_59805327_48'
                    AND operations.value.title = ""
                LIMIT @limit
            """.format(columns=columns, dataset=self.dataset, table=self.table)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter('limit', 'INT64', size),
                ]
            )

        query_job = client.query(query_template, job_config=job_config)
        query_job.result()
        df_results = query_job.to_dataframe()
        print(df_results)
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)

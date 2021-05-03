from jinjasql import JinjaSql


jquery = JinjaSql(param_style='named')


class BlockQuery():
    @staticmethod
    def get_head(table, size):
        data = {"table": table, "size": size}
        query_template = """
            SELECT *
            FROM `steemit-307308.hive.{{ table }}`
            LIMIT {{ size }}
        """
        query, bind_params = jquery.prepare_query(query_template, data)
        return query, bind_params


if __name__ == '__main__':
    bigquery = BlockQuery()
    query, bind_params = bigquery.get_head('minh', 10)
    print(query)
    print(bind_params)

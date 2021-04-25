
class AccountQuery():
    @classmethod
    def get_head(table, limit):
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
        return query

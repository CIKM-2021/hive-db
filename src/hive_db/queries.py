
class AccountQuery():
    @staticmethod
    def get_head():
        table = 'steemit-307308.hive.scrape'
        limit = 5
        sql = (
            "WITH data AS ("
            "SELECT accounts.blog_history as blogs"
            f"FROM {table}"
            ")"
            "SELECT blogs"
            "FROM data"
            f"LIMIT {5}"
        )
        return sql

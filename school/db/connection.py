import mysql.connector
from mysql.connector import MySQLConnection

class MySQLConnectionManager:
    def __init__(self, **db_config):
        self.db_config = db_config
        self._conn: MySQLConnection | None = None

    def __enter__(self) -> MySQLConnection:
        self._conn = mysql.connector.connect(**self.db_config)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()

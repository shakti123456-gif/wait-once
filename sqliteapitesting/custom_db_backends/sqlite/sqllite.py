from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper

class DatabaseWrapper(SQLiteDatabaseWrapper):
    def get_new_connection(self, conn_params):
        conn = super().get_new_connection(conn_params)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn
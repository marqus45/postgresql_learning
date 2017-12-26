from psycopg2 import pool


class Database:
    __connection_pool = None

    @staticmethod
    def initialize(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(1,
                                                               3,
                                                               **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def put_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.close_all()


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):  # exc - Exceptions type, value , trace
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.put_connection(self.connection)

		
import sqlite3
from sqlite3 import Connection, Cursor, Error

DB_FILE_PATH = './quiz.db'


class ConnectionManager(object):
    instance: 'ConnectionManager' = None
    connection: Connection = None

    def __new__(cls, *args, **kwargs) -> 'ConnectionManager':
        if not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instance.connection = sqlite3.connect(
                DB_FILE_PATH, check_same_thread=False)
            cls.instance.connection.isolation_level = None
        return cls.instance

    def create(self):
        # Ouvrez le fichier SQL
        with open('./data.db.sql', 'r') as f:
            # Exécutez le script SQL
            self.connection.executescript(f.read())

    def execute(self, query, *args) -> Cursor:
        cursor = self.connection.cursor()
        if not query.lower().startswith("select"):
            cursor.execute("begin")
        try:
            result: Cursor = cursor.execute(query, args)
            if not query.lower().startswith("select"):
                cursor.execute("commit")
            return result
        except:
            if not query.lower().startswith("select"):
                cursor.execute("rollback")
            raise

    def __del__(self):
        self.connection.close()
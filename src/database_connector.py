import psycopg2

class DatabaseConnector:

    def __init__(self):
        self.db_connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Read here on why this block needs 4 arguments: https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
        return False

    def load_conf(self, conf, database = 'DATABASE CONNECTION'):
        self.db_host = conf[database]['DB HOST']
        self.db_name = conf[database]['DB NAME']
        self.db_username = conf[database]['DB USERNAME']
        self.db_password = conf[database]['DB PASSWORD']
        self.db_port = conf[database]['DB PORT']

    def connect_to_db(self):
        self.db_connection = psycopg2.connect(
            host = self.db_host,
            dbname = self.db_name,
            user = self.db_username,
            password = self.db_password,
            port = self.db_port
            )
        self.cursor = self.db_connection.cursor()
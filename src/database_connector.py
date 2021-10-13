import psycopg2

class DatabaseConnector:

    def __init__(self):
        self.db_connection = None

    def load_conf(self, conf):
        self.db_host = conf['DATABASE CONNECTION']['DB HOST']
        self.db_name = conf['DATABASE CONNECTION']['DB NAME']
        self.db_username = conf['DATABASE CONNECTION']['DB USERNAME']
        self.db_password = conf['DATABASE CONNECTION']['DB PASSWORD']
        self.db_port = conf['DATABASE CONNECTION']['DB PORT']

    def connect_to_db(self):
        self.db_connection = psycopg2.connect(
            host = self.db_host,
            dbname = self.db_name,
            user = self.db_username,
            password = self.db_password,
            port = self.db_port
            )
        self.cursor = self.db_connection.cursor()
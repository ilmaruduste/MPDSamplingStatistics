import psycopg2

class DatabaseConnector:

    def __init__(self, conf):
        self.db_host = conf['DATABASE CONNECTION']['DB HOST']
        self.db_name = conf['DATABASE CONNECTION']['DB NAME']
        self.db_username = conf['DATABASE CONNECTION']['DB USERNAME']
        self.db_password = conf['DATABASE CONNECTION']['DB PASSWORD']
        self.db_port = conf['DATABASE CONNECTION']['DB PORT']
        self.db_connector = None

    

    
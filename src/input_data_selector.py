import pandas

class InputDataSelector:
    
    def __init__(self, conf):
        self.data_schemas = conf["INPUT DATA"]["DATA SCHEMAS"]
        self.data_types = conf["INPUT DATA"]["CORRESPONDING TYPES"]
        self.indicators = conf["INPUT DATA"]["INDICATORS"]

    def load_table_name(self, table_name):
        self.table_name = table_name          # We have one specific table name per InputDataSelector instance

    def create_sql_query(self):
        sql_query = ""

        for i, (schema, type) in enumerate(zip(self.data_schemas, self.data_types)):
            sql_query += '''SELECT *, '{ftype}' AS data_type FROM {fschema}.{ftablename}\n'''.format(fschema = schema, ftype = type, ftablename = self.table_name)

            if (i < len(self.data_schemas) - 1):
                sql_query += "UNION\n"

        self.query = sql_query

    def get_sql_query(self):
        return self.query

    def get_pandas_df_from_query(self, connection):
        return pandas.read_sql_query(self.query, connection.db_connection)

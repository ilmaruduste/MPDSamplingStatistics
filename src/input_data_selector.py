import pandas

class InputDataSelector:
    
    def __init__(self, data_schemas, data_types, table_names, indicators):
        self.data_schemas = data_schemas
        self.data_types = data_types
        self.table_names = table_names
        self.indicators = indicators
        self.table = None
        self.query = None

    def create_sql_query(self):
        return True

    def create_pandas_df_from_query(self):
        return False
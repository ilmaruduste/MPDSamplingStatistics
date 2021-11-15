import pandas

class InputDataSelector:
    
    def __init__(self, conf):
        self.data_schemas = conf["INPUT DATA"]["DATA SCHEMAS"]
        self.data_types = conf["INPUT DATA"]["CORRESPONDING TYPES"]
        self.indicators = conf["INPUT DATA"]["INDICATORS"]
        self.join_categories = conf["INPUT DATA"]["JOIN CATEGORIES"]
        self.group_name = conf["INPUT DATA"]["GROUP NAME"]

    def load_table_name(self, table_name):
        self.table_name = table_name          # We have one specific table name per InputDataSelector instance

    def create_sql_query(self):
        sql_query = ""

        for i, (schema, type) in enumerate(zip(self.data_schemas, self.data_types)):
            sql_query += '''SELECT {columns}, '{ftype}' AS data_type FROM {fschema}.{ftablename}\n'''.format(columns = self.return_all_columns_as_string(), fschema = schema, ftype = type, ftablename = self.table_name)

            if (i < len(self.data_schemas) - 1):
                sql_query += "UNION ALL\n"

        self.query = sql_query

    def get_sql_query(self):
        return self.query

    def get_pandas_df_from_query(self, connection, query = None):
        if query == None:
            query = self.query
        return pandas.read_sql_query(query, connection.db_connection)

    def create_separate_queries(self):
        sql_query_array = []

        for (schema, type) in zip(self.data_schemas, self.data_types):
            sql_query = '''SELECT *, '{ftype}' AS data_type FROM {fschema}.{ftablename}\n'''.format(fschema = schema, ftype = type, ftablename = self.table_name)
            sql_query_array.append(sql_query)
        
        return sql_query_array

    def return_all_columns_as_string(self):
        column_list = list(set([*self.join_categories, *self.indicators, *self.group_name]))
        column_list.sort()
        column_string = ""
        for col_index, col in enumerate(column_list):
            column_string += "'{column}'".format(column = col)
            if col_index < len(column_list) - 1:
                column_string += ", "

        return column_string

import pandas as pd
from . import input_data_selector
from . import results_row_creator

class ResultsProcessor:

    def __init__(self, conf, connection, second_connection = None):
        self.data_schemas = conf['INPUT DATA']['DATA SCHEMAS']
        self.data_types = conf['INPUT DATA']['CORRESPONDING TYPES']
        self.table_names = conf['INPUT DATA']['TABLE NAMES']
        self.indicators = conf['INPUT DATA']['INDICATORS']
        self.data_source = conf['INPUT DATA']['DATA SOURCE']
        self.join_categories = conf['INPUT DATA']['JOIN CATEGORIES']
        self.filter_name = conf['INPUT DATA']['FILTER NAME']
        self.filter_values = conf['INPUT DATA']['FILTER VALUES']
        self.coef_array = conf['INPUT DATA']['COEF VALUES']
        self.connection = connection
        self.second_connection = second_connection
        self.ids = input_data_selector.InputDataSelector(conf)

    def process_results(self):
        final_data_dict = {}
        for table_name in self.table_names:
            print(f"\n\tTABLE {table_name}")
            all_data = self.load_table_data(table_name)

            for i, data_type in enumerate(self.data_types[1:]):
                print(f"\t\tDATA TYPE {data_type}")
                original_data, comparison_data = self.get_orig_comp_data(all_data, data_type)

                for indicator in self.indicators:
                    print(f"\t\t\tINDICATOR {indicator}")
                    rrc = self.get_correct_rrc(original_data, comparison_data, self.coef_array[i+1])
                    final_data_dict = self.get_final_data(final_data_dict, table_name, data_type, indicator, rrc)
        
        return pd.DataFrame(final_data_dict)

    def get_orig_comp_data(self, all_data, data_type):
        original_data = all_data[all_data['data_type'] == self.data_types[0]].copy()
        comparison_data = all_data[all_data['data_type'] == data_type].copy()
        return original_data, comparison_data

    def get_correct_rrc(self, original_data, comparison_data, comparison_data_coef):
        if self.data_source == 'DomesticInbound':
            rrc = results_row_creator.DomInbResultsRowCreator(original_data, comparison_data, self.join_categories, comparison_data_coef)
        else:
            rrc = results_row_creator.OutbResultsRowCreator(original_data, comparison_data, self.join_categories, comparison_data_coef)
        return rrc

    def get_final_data(self, final_data_dict, table_name, data_type, indicator, rrc):
        if self.filter_name == "":  
            final_data_dict = self.merge_dict(
                            final_data_dict, 
                            rrc.get_row_of_statistics(table_name, data_type, indicator)
                            )
                        
        else:
            final_data_dict = self.merge_dict(
                            final_data_dict, 
                            rrc.get_row_of_statistics(table_name, data_type, indicator, self.filter_name, self.filter_values)
                            )
                
        return final_data_dict

    def load_table_data(self, table_name):
        if self.second_connection.db_connection == None:
            return self.load_table_data_from_schemas(table_name)
        else:
            return self.load_table_data_from_2_dbs(table_name)

    def load_table_data_from_schemas(self, table_name):
        self.ids.load_table_name(table_name)
        self.ids.create_sql_query()
        return self.ids.get_pandas_df_from_query(self.connection)

    def load_table_data_from_2_dbs(self, table_name):
        # NB! This assumes that when there are 2 database connections, there are also only 2 data types.
        self.ids.load_table_name(table_name)
        separate_queries = self.ids.create_separate_queries()
        separate_dataframes = [
            self.ids.get_pandas_df_from_query(self.connection, query = separate_queries[0]),
            self.ids.get_pandas_df_from_query(self.second_connection, query = separate_queries[1])
            ]

        return pd.concat(separate_dataframes, ignore_index = True)


    def merge_dict(self, dict1, dict2):
        ''' Merge dictionaries and keep values of common keys in list'''
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                    dict3[key] = [*value , *dict1[key]]
        return dict3
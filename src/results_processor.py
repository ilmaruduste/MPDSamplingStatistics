import pandas as pd
from . import input_data_selector
from . import results_row_creator

class ResultsProcessor:

    def __init__(self, conf, connection):
        self.data_schemas = conf['INPUT DATA']['DATA SCHEMAS']
        self.data_types = conf['INPUT DATA']['CORRESPONDING TYPES']
        self.table_names = conf['INPUT DATA']['TABLE NAMES']
        self.indicators = conf['INPUT DATA']['INDICATORS']
        self.data_source = conf['INPUT DATA']['DATA SOURCE']
        self.join_categories = conf['INPUT DATA']['JOIN CATEGORIES']
        self.filter_name = conf['INPUT DATA']['FILTER NAME']
        self.filter_values = conf['INPUT DATA']['FILTER VALUES']
        self.connection = connection
        self.ids = input_data_selector.InputDataSelector(conf)

    def process_results(self):
        final_data_dict = {}
        for table_name in self.table_names:
            all_data = self.load_table_data_from_schemas(table_name)

            for data_type in self.data_types[1:]:
                original_data = all_data[all_data['data_type'] == self.data_types[0]]
                comparison_data = all_data[all_data['data_type'] == data_type]

                for indicator in self.indicators:
                    if self.data_source == 'DomesticInbound':
                        rrc = results_row_creator.DomInbResultsRowCreator(original_data, comparison_data, self.join_categories)
                    else:
                        rrc = results_row_creator.OutbResultsRowCreator()
                    final_data_dict.update(rrc.get_row_of_statistics_long(table_name, data_type, indicator, self.filter_name, self.filter_values))
        
        return pd.DataFrame(final_data_dict)

    def load_table_data_from_schemas(self, table_name):
        self.ids.load_table_name(table_name)
        self.ids.create_sql_query()
        return self.ids.get_pandas_df_from_query(self.connection)
    

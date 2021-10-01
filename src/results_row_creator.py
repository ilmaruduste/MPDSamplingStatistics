import pandas

def get_len_filtered_data(data, filter_name, filter_value):
    return len(data[data[filter_name] == filter_value])

def get_division_of_lengths_filters(original_data, comparison_data, filter_name, filter_value):
    return get_len_filtered_data(comparison_data, filter_name, filter_value)/get_len_filtered_data(original_data, filter_name, filter_value)

class ResultsRowCreator:

    def __init__(self, original_data = None, comparison_data = None):
        self.original_data = original_data
        self.comparison_data = comparison_data

class DomInbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)

    def calculate_combination_coverage(self, filter_name, filter_value):
        return(round(get_division_of_lengths_filters(self.original_data, self.comparison_data, filter_name, filter_value), 4))

class OutbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)
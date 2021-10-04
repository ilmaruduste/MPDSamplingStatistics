import pandas
from scipy import stats
import pandas as pd

def get_len_filtered_data(data, filter_name, filter_value):
    return len(data[data[filter_name] == filter_value])

class ResultsRowCreator:

    def __init__(self, original_data = None, comparison_data = None):
        self.original_data = original_data
        self.comparison_data = comparison_data

    def get_filtered_orig_data(self, filter_name, filter_value):
        return self.original_data[self.original_data[filter_name] == filter_value]

    def get_division_of_lengths_filters(self, filter_name, filter_value):
        return get_len_filtered_data(self.comparison_data, filter_name, filter_value)/get_len_filtered_data(self.original_data, filter_name, filter_value)

    def calculate_combination_coverage(self, filter_name = None, filter_value = None, round_decimal_places = 4):
        if (filter_name == None and filter_value == None):
            return round(len(self.comparison_data)/len(self.original_data), 4)
        else:
            return(round(self.get_division_of_lengths_filters(filter_name, filter_value), round_decimal_places))

    def calculate_ks_test(self, indicator_name, filter_name = None, filter_value = None):
        # Returns a tuple. 
        # First value is the KS statistic (D)
        # Second value is the likelihood (p-value) that these two datas are from the same distribution
        if (filter_name == None and filter_value == None):
            return stats.kstest(self.original_data[indicator_name], self.comparison_data[indicator_name])
        else:
            return stats.kstest(self.get_filtered_orig_data(filter_name, filter_value)[indicator_name],
                                self.comparison_data[self.comparison_data[filter_name] == filter_value][indicator_name])

    def calculate_original_indicator_mean(self, indicator_name, filter_name = None, filter_value = None, round_decimal_places = 4):
        if (filter_name == None and filter_value == None):
            return round(self.original_data[indicator_name].mean(), round_decimal_places)
        else:
            return round(self.get_filtered_orig_data(filter_name, filter_value)[indicator_name].mean(), round_decimal_places)

    def calculate_original_indicator_mad(self, indicator_name, filter_name = None, filter_value = None, round_decimal_places = 4):
        if (filter_name == None and filter_value == None):
            return round(stats.median_abs_deviation(self.original_data[indicator_name]), round_decimal_places)
        else:
            return round(stats.median_abs_deviation(self.get_filtered_orig_data(filter_name, filter_value)[indicator_name]), round_decimal_places)

    def join_orig_comp_data(self, join_categories):
        self.joined_data = pd.merge(self.original_data, self.comparison_data, how = "inner", on = join_categories)

class DomInbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)


class OutbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)
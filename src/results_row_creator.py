from logging import log
import pandas
from scipy import stats
import pandas as pd
import numpy as np

def get_len_filtered_data(data, filter_name, filter_value):
    return len(data[data[filter_name] == filter_value])

class ResultsRowCreator:

    def __init__(self, original_data = None, comparison_data = None):
        self.original_data = original_data
        self.comparison_data = comparison_data

    def get_filtered_orig_data(self, filter_name, filter_value):
        return self.original_data[self.original_data[filter_name] == filter_value]

    def get_filtered_comp_data(self, filter_name, filter_value):
        return self.comparison_data[self.comparison_data[filter_name] == filter_value]

    def get_filtered_joined_data(self, filter_name, filter_value):
        return self.joined_data[self.joined_data[filter_name] == filter_value]

    def get_joined_data_indicators(self, indicator_name_x, indicator_name_y, filter_name = None, filter_value = None):
        if (filter_name == None and filter_value == None):
            return zip(self.joined_data[indicator_name_x], 
                        self.joined_data[indicator_name_y])
        else:
            return zip(self.get_filtered_joined_data(filter_name, filter_value)[indicator_name_x], 
                        self.get_filtered_joined_data(filter_name, filter_value)[indicator_name_y])

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
        # MAD - mean_absolute_deviation
        if (filter_name == None and filter_value == None):
            return round(stats.median_abs_deviation(self.original_data[indicator_name]), round_decimal_places)
        else:
            return round(stats.median_abs_deviation(self.get_filtered_orig_data(filter_name, filter_value)[indicator_name]), round_decimal_places)

    def join_orig_comp_data(self, join_categories):
        self.joined_data = pd.merge(self.original_data, self.comparison_data, how = "inner", on = join_categories)

    def calculate_absolute_percentage_error_metrics(self, indicator_name, filter_name = None, filter_value = None, round_decimal_places = 4):
        # This function assumes that self.joined_data exists (i.e. join_orig_comp_data() has been done)
        # The function returns an array
        # First value is MAPE - Mean Absolute Percentage Error
        # The second value is MAD - Median Absolute Deviation for the errors
        x, y = indicator_name + "_x", indicator_name + "_y"

        if (filter_name == None and filter_value == None):
            percentage_errors = np.array([abs(orig_ind - comp_ind)/orig_ind*100 for orig_ind, comp_ind in self.get_joined_data_indicators(x, y)])
        else:
            percentage_errors = np.array([abs(orig_ind - comp_ind)/orig_ind*100 for orig_ind, comp_ind in self.get_joined_data_indicators(x, y, filter_name, filter_value)])
        
        return np.round([percentage_errors.mean(), stats.median_abs_deviation(percentage_errors)], round_decimal_places)

    def calculate_absolute_logarithmic_error_metrics(self, indicator_name, filter_name = None, filter_value = None, round_decimal_places = 4):
        # This function assumes that self.joined_data exists (i.e. join_orig_comp_data() has been done)
        # The function returns an array
        # First value is MALE - Mean Absolute Logarithmic Error
        # The second value is MAD - Median Absolute Deviation for the errors
        x, y = indicator_name + "_x", indicator_name + "_y"

        if (filter_name == None and filter_value == None):
            logarithmic_errors = np.array([abs(np.log10((orig_ind + 1)/(comp_ind + 1))) for orig_ind, comp_ind in self.get_joined_data_indicators(x, y)])
        else:
            logarithmic_errors = np.array([abs(np.log10((orig_ind + 1)/(comp_ind + 1))) for orig_ind, comp_ind in self.get_joined_data_indicators(x, y, filter_name, filter_value)])
        
        return np.round([logarithmic_errors.mean(), stats.median_abs_deviation(logarithmic_errors)], round_decimal_places)


class DomInbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)


class OutbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data, comparison_data):
        super().__init__(original_data, comparison_data)
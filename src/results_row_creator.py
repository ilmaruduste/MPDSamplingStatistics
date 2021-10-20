from scipy import stats
import pandas as pd
import numpy as np

def get_len_filtered_data(data, filter_name, filter_value):
    return len(data[data[filter_name] == filter_value])

class ResultsRowCreator:

    def __init__(self, original_data = None, comparison_data = None, join_categories = None, comparison_data_coef = 1):
        self.original_data = original_data
        self.comparison_data = comparison_data
        self.join_categories = join_categories
        self.comparison_data_coef = comparison_data_coef

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
        try:
            return get_len_filtered_data(self.comparison_data, filter_name, filter_value)/get_len_filtered_data(self.original_data, filter_name, filter_value)
        except(ZeroDivisionError):
            return np.NaN

    def calculate_combination_coverage(self, filter_name = None, filter_value = None, round_decimal_places = 4):
        if (filter_name == None and filter_value == None):
            return round(len(self.comparison_data)/len(self.original_data), 4)
        else:
            return(round(self.get_division_of_lengths_filters(filter_name, filter_value), round_decimal_places))

    def calculate_ks_test(self, indicator_name, filter_name = None, filter_value = None):
        # Returns a tuple. 
        # First value is the KS statistic (D)
        # Second value is the likelihood (p-value) that these two datas are from the same distribution
        try:
            if (filter_name == None and filter_value == None):
                return stats.kstest(self.original_data[indicator_name], self.comparison_data[indicator_name])
            else:
                return stats.kstest(self.get_filtered_orig_data(filter_name, filter_value)[indicator_name],
                                    self.comparison_data[self.comparison_data[filter_name] == filter_value][indicator_name])
        except(ValueError):
            return (np.NaN, np.NaN)

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
        # print(f"self.joined_data: {self.joined_data}")

    def calculate_absolute_percentage_error_metrics(self, indicator_name, filter_name = None, filter_value = None, round_decimal_places = 4):
        # This function assumes that self.joined_data exists (i.e. join_orig_comp_data() has been done)
        # The function returns an array
        # First value is MAPE - Mean Absolute Percentage Error
        # The second value is MAD - Median Absolute Deviation for the errors
        # self.fill_joined_data_if_needed()

        x, y = indicator_name + "_x", indicator_name + "_y"

        if (filter_name == None and filter_value == None):
            percentage_errors = np.array([self.calculate_percentage_error(orig_ind, comp_ind) for orig_ind, comp_ind in self.get_joined_data_indicators(x, y)])
        else:
            percentage_errors = np.array([self.calculate_percentage_error(orig_ind, comp_ind) for orig_ind, comp_ind in self.get_joined_data_indicators(x, y, filter_name, filter_value)])
        
        return np.round([np.nanmean(percentage_errors), stats.median_abs_deviation(percentage_errors[~np.isnan(percentage_errors)])], round_decimal_places)

    def calculate_percentage_error(self, orig_ind, comp_ind):
        try:
            return abs(orig_ind - comp_ind)/orig_ind*100
        except(ZeroDivisionError):
            return np.NaN

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

    def multiply_comp_with_coef(self, indicator_name):
        self.comparison_data[indicator_name] = self.comparison_data.loc[:, indicator_name].multiply(self.comparison_data_coef)

class DomInbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data = None, comparison_data = None, join_categories = None, comparison_data_coef = 1):
        super().__init__(original_data, comparison_data, join_categories)

    def get_row_of_statistics_wide(self, table_name, data_type, indicator_name, filter_name):
        self.multiply_comp_with_coef(indicator_name)
        self.join_orig_comp_data(self.join_categories)
        combination_coverage_array = [self.calculate_combination_coverage(filter_name, lau_level_int) for lau_level_int in range(1,4)]
        ks_test_array = [self.calculate_ks_test(indicator_name) for lau_level_int in range(1,4)]
        indicator_mean_array = [self.calculate_original_indicator_mean(indicator_name) for lau_level_int in range(0,4)]
        indicator_mad_array = [self.calculate_original_indicator_mad(indicator_name) for lau_level_int in range(0,4)]
        ape_metrics_array = np.array([self.calculate_absolute_percentage_error_metrics(indicator_name) for lau_level_int in range(0,4)]).T
        ale_metrics_array = np.array([self.calculate_absolute_logarithmic_error_metrics(indicator_name) for lau_level_int in range(0,4)]).T
        
        results_dict = {
            'table_name':table_name
            , 'data_type': data_type
            , 'indicator': indicator_name
            , 'combination_coverage_mean': np.array(combination_coverage_array).mean()
            , 'cc_lau1': combination_coverage_array[0]
            , 'cc_lau2': combination_coverage_array[1]
            , 'cc_lau3': combination_coverage_array[2]
            , 'ks_test_p_general': self.calculate_ks_test(indicator_name)[1]
            , 'ks_test_D_general': self.calculate_ks_test(indicator_name)[0]
            , 'ks_test_p_lau1': ks_test_array[0][0]
            , 'ks_test_p_lau2': ks_test_array[1][0]
            , 'ks_test_p_lau3': ks_test_array[2][0]
            , 'indicator_mean_lau0': indicator_mean_array[0]
            , 'indicator_mad_lau0': indicator_mad_array[0]
            , 'indicator_mean_lau1': indicator_mean_array[1]
            , 'indicator_mad_lau1': indicator_mad_array[1]
            , 'indicator_mean_lau2': indicator_mean_array[2]
            , 'indicator_mad_lau2': indicator_mad_array[2]
            , 'indicator_mean_lau3': indicator_mean_array[3]
            , 'indicator_mad_lau3': indicator_mad_array[3]
            , 'APE_mean' : np.array(ape_metrics_array[0]).mean()
            , 'APE_mad' : np.array(ape_metrics_array[1]).mean()
            , 'APE_mean_lau0': np.array(ape_metrics_array[0][0])
            , 'APE_mad_lau0': np.array(ape_metrics_array[1][0])
            , 'APE_mean_lau1': np.array(ape_metrics_array[0][1])
            , 'APE_mad_lau1': np.array(ape_metrics_array[1][2])
            , 'APE_mean_lau2': np.array(ape_metrics_array[0][2])
            , 'APE_mad_lau2': np.array(ape_metrics_array[1][2])
            , 'APE_mean_lau3': np.array(ape_metrics_array[0][3])
            , 'APE_mad_lau3': np.array(ape_metrics_array[1][3])
            , 'ALE_mean' : np.array(ale_metrics_array[0]).mean()
            , 'ALE_mad' : np.array(ale_metrics_array[1]).mean()
            , 'ALE_mean_lau0': np.array(ale_metrics_array[0][0])
            , 'ALE_mad_lau0': np.array(ale_metrics_array[1][0])
            , 'ALE_mean_lau1': np.array(ale_metrics_array[0][1])
            , 'ALE_mad_lau1': np.array(ale_metrics_array[1][2])
            , 'ALE_mean_lau2': np.array(ale_metrics_array[0][2])
            , 'ALE_mad_lau2': np.array(ale_metrics_array[1][2])
            , 'ALE_mean_lau3': np.array(ale_metrics_array[0][3])
            , 'ALE_mad_lau3': np.array(ale_metrics_array[1][3])
        }

        return results_dict

    def get_row_of_statistics_long(self, table_name, data_type, indicator_name, filter_name, lau_level_array):
        self.multiply_comp_with_coef(indicator_name)
        self.join_orig_comp_data(self.join_categories)
        combination_coverage_array = [self.calculate_combination_coverage(filter_name, lau_level_int) for lau_level_int in lau_level_array]
        ks_test_array = [self.calculate_ks_test(indicator_name, filter_name, lau_level_int) for lau_level_int in lau_level_array]
        indicator_mean_array = [self.calculate_original_indicator_mean(indicator_name, filter_name, lau_level_int) for lau_level_int in lau_level_array]
        indicator_mad_array = [self.calculate_original_indicator_mad(indicator_name, filter_name, lau_level_int) for lau_level_int in lau_level_array]
        ape_metrics_array = np.array([self.calculate_absolute_percentage_error_metrics(indicator_name, filter_name, lau_level_int) for lau_level_int in lau_level_array]).T
        ale_metrics_array = np.array([self.calculate_absolute_logarithmic_error_metrics(indicator_name, filter_name, lau_level_int) for lau_level_int in lau_level_array]).T

        results_dict = {
            'table_name': np.repeat([table_name], len(lau_level_array))
            , 'data_type': np.repeat([data_type], len(lau_level_array))
            , 'indicator': np.repeat([indicator_name], len(lau_level_array))
            , 'lau_level': lau_level_array
            , 'combination_coverage': combination_coverage_array
            , 'ks_test_D': np.array(ks_test_array).T[0]
            , 'ks_test_p': np.array(ks_test_array).T[1]
            , 'indicator_mean': indicator_mean_array
            , 'indicator_mad': indicator_mad_array
            , 'APE_mean': ape_metrics_array[0]
            , 'APE_mad': ape_metrics_array[1]
            , 'ALE_mean': ale_metrics_array[0]
            , 'ALE_mad': ale_metrics_array[1]
        }

        return results_dict

class OutbResultsRowCreator(ResultsRowCreator):

    def __init__(self, original_data = None, comparison_data = None, join_categories = None, comparison_data_coef = 1):
        super().__init__(original_data, comparison_data, join_categories)

    def get_row_of_statistics_long(self, table_name, data_type, indicator_name):
        self.multiply_comp_with_coef(indicator_name)
        self.join_orig_comp_data(self.join_categories)
        combination_coverage_array = self.calculate_combination_coverage()
        ks_test_array = self.calculate_ks_test(indicator_name)
        indicator_mean = self.calculate_original_indicator_mean(indicator_name)
        indicator_mad = self.calculate_original_indicator_mad(indicator_name)
        ape_metrics_array = np.array(self.calculate_absolute_percentage_error_metrics(indicator_name))
        ale_metrics_array = np.array(self.calculate_absolute_logarithmic_error_metrics(indicator_name))

        results_dict = {
            'table_name': [table_name]
            , 'data_type': [data_type]
            , 'indicator': [indicator_name]
            , 'combination_coverage': [combination_coverage_array]
            , 'ks_test_D': [np.array(ks_test_array)[0]]
            , 'ks_test_p': [np.array(ks_test_array)[1]]
            , 'indicator_mean': [indicator_mean]
            , 'indicator_mad': [indicator_mad]
            , 'APE_mean': [ape_metrics_array[0]]
            , 'APE_mad': [ape_metrics_array[1]]
            , 'ALE_mean': [ale_metrics_array[0]]
            , 'ALE_mad': [ale_metrics_array[1]]
        }

        return results_dict
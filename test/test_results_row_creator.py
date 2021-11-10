# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/

from src import results_row_creator
import unittest
import pandas as pd
import numpy as np


class TestResultsRowCreator(unittest.TestCase):
    def setUp(self):
        original_df = pd.DataFrame(
                {'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-01-01','2021-02-01','2021-01-01'],
                'dummy_category':[1,1,1,1,2,2,3], 
                'dummy_indicator':[10,20,30,40,50,60,70]})

        comparison_df = pd.DataFrame(
                {'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01', '2021-01-01','2021-02-01'],
                'dummy_category':[1,1,1,2,2],
                'dummy_indicator': [10,20,30,50,70]})

        self.rrc = results_row_creator.ResultsRowCreator(
            original_data = original_df,
            comparison_data = comparison_df)
        self.dirrc = results_row_creator.DomInbResultsRowCreator(
            original_data = original_df,
            comparison_data = comparison_df)
        self.outbrrc = results_row_creator.OutbResultsRowCreator(
            original_data = original_df,
            comparison_data = comparison_df)

        join_categories = ['dummy_date', 'dummy_category']
        result = pd.DataFrame({
            'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01','2021-01-01','2021-02-01'],
            'dummy_category':[1,1,1,2,2], 
            'dummy_indicator_x':[10,20,30,50,60],
            'dummy_indicator_y':[10,20,30,50,70]})
        self.rrc.join_orig_comp_data(join_categories)

    def test_combination_coverage_without_group(self):
        self.assertEqual(self.rrc.calculate_combination_coverage(), round(5/7, 4))

    def test_combination_coverage_with_group_1(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 1), 0.75)

    def test_combination_coverage_with_group_2(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 2), 1)

    def test_combination_coverage_with_group_3(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 3), 0)

    def test_ks_test_0(self):
        self.rrc.comparison_data['dummy_indicator'] = 0
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 0, places = 2)

    def test_ks_test_1(self):
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 1, places = 2)

    def test_ks_test_1_group(self):
        self.rrc.comparison_data['dummy_indicator'] = [10,20,30,0,0]
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator', group_name='dummy_category', group_value=1)[1], 1, places = 2)

    def test_original_indicator_mean(self):
        self.assertEqual(self.rrc.calculate_original_indicator_mean('dummy_indicator'), 40)

    def test_original_indicator_mean_group(self):
        self.assertEqual(self.rrc.calculate_original_indicator_mean('dummy_indicator', group_name = 'dummy_category', group_value = 1), 25)

    def test_original_indicator_mad(self):
        self.assertEqual(self.rrc.calculate_original_indicator_mad('dummy_indicator'), 20)

    def test_mean_absolute_percentage_error_0(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,30,50,60]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[0], 0)

    def test_mean_absolute_percentage_error_50(self):
        self.rrc.joined_data['dummy_indicator_y'] = [5,10,15,25,30]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[0], 50)

    def test_mean_absolute_percentage_error_100(self):
        self.rrc.joined_data['dummy_indicator_y'] = [0,0,0,0,0]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[0], 100)

    def test_mean_absolute_percentage_error_50_group(self):
        self.rrc.joined_data['dummy_indicator_y'] = [5,10,15,50,60]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', group_name = 'dummy_category', group_value = 1)[0], 50)

    def test_mean_absolute_percentage_error_200_group(self):
        self.rrc.joined_data['dummy_indicator_y'] = [5,10,15,150,180]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', group_name = 'dummy_category', group_value = 2)[0], 200)

    def test_mad_absolute_percentage_error_0(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,30,50,60]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[1], 0)

    def test_mad_absolute_percentage_error_50(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,15,100,120]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[1], 50)

    def test_mad_absolute_percentage_error_0_group(self):
        # This test works since it's MEDIAN and not MEAN absolute deviation
        self.rrc.joined_data['dummy_indicator_y'] = [4,20,30,100,120]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', group_name = 'dummy_category', group_value = 1)[1], 0)

    def test_mean_ale_0(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,30,50,60]
        self.assertEqual(self.rrc.calculate_absolute_logarithmic_error_metrics('dummy_indicator')[0], 0)
    
    def test_mean_ale_1(self):
        self.rrc.joined_data['dummy_indicator_x'] = [9,19,29,49,59]
        self.rrc.joined_data['dummy_indicator_y'] = [99,199,299,499,599]
        self.assertEqual(self.rrc.calculate_absolute_logarithmic_error_metrics('dummy_indicator')[0], 1)
    
    def test_mad_ale_05(self):
        self.rrc.joined_data['dummy_indicator_x'] = [9,19,29,49,59]
        self.rrc.joined_data['dummy_indicator_y'] = [9,19,93,499,599]
        self.assertAlmostEqual(self.rrc.calculate_absolute_logarithmic_error_metrics('dummy_indicator')[1], 0.5, places = 2)

    def test_coef_multiplication(self):
        self.rrc.comparison_data_coef = 2
        self.rrc.multiply_comp_with_coef('dummy_indicator')
        self.assertTrue(np.array_equal(self.rrc.comparison_data['dummy_indicator'], [20,40,60,100,140], equal_nan=True))

    def test_dominb_statistics(self):
        join_categories = ['dummy_date', 'dummy_category']

        original_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-01-01','2021-02-01','2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,1,2,2,3,3], 
            'dummy_indicator':[5,10,20,30,40,50,60,70,80]})

        comparison_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-01-01','2021-02-01', '2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,2,2,3,3],
            'dummy_indicator': [5,10,20,30,50,70,80, 90]})
        
        lau_level_array = [0,1,2,3]

        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_df, comparison_df, join_categories)
        print(self.dirrc.get_row_of_statistics('dummy_table', 'dummy_data', 'dummy_indicator', 'dummy_category', lau_level_array))

    def test_dominb_without_group_statistics(self):
        join_categories = ['dummy_date', 'dummy_category']

        original_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-01-01','2021-02-01','2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,1,2,2,3,3], 
            'dummy_indicator':[5,10,20,30,40,50,60,70,80]})

        comparison_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-01-01','2021-02-01', '2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,2,2,3,3],
            'dummy_indicator': [5,10,20,30,50,70,80, 90]})

        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_df, comparison_df, join_categories)
        print(self.dirrc.get_row_of_statistics('dummy_table', 'dummy_data', 'dummy_indicator'))
    
    def test_outb_statistics(self):
        join_categories = ['dummy_date', 'dummy_category']

        original_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-01-01','2021-02-01','2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,1,2,2,3,3], 
            'dummy_indicator':[5,10,20,30,40,50,60,70,80]})

        comparison_df = pd.DataFrame(
            {'dummy_date':['2021-01-01', '2021-01-01', '2021-02-01', '2021-03-01', '2021-01-01','2021-02-01', '2021-01-01', '2021-02-01'],
            'dummy_category':[0,1,1,1,2,2,3,3],
            'dummy_indicator': [5,10,20,30,50,70,80, 90]})

        self.orrc = results_row_creator.OutbResultsRowCreator(original_df, comparison_df, join_categories)
        print(self.orrc.get_row_of_statistics('dummy_table', 'dummy_data', 'dummy_indicator'))



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    # runner.run(suite())

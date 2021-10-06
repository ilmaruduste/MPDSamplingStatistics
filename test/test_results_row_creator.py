# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/

from src import results_row_creator
import unittest
import pandas as pd


class TestResultsRowCreator(unittest.TestCase):
    def setUp(self):
        self.rrc = results_row_creator.ResultsRowCreator(
            original_data = pd.DataFrame(
                {'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-01-01','2021-02-01','2021-01-01'],
                'dummy_category':[1,1,1,1,2,2,3], 
                'dummy_indicator':[10,20,30,40,50,60,70]}),
            comparison_data = pd.DataFrame(
                {'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01', '2021-01-01','2021-02-01'],
                'dummy_category':[1,1,1,2,2],
                'dummy_indicator': [10,20,30,50,70]}))
        self.dirrc = results_row_creator.DomInbResultsRowCreator(None, None)
        self.outbrrc = results_row_creator.OutbResultsRowCreator(None, None)

        join_categories = ['dummy_date', 'dummy_category']
        result = pd.DataFrame({
            'dummy_date':['2021-01-01', '2021-02-01', '2021-03-01','2021-01-01','2021-02-01'],
            'dummy_category':[1,1,1,2,2], 
            'dummy_indicator_x':[10,20,30,50,60],
            'dummy_indicator_y':[10,20,30,50,70]})
        self.rrc.join_orig_comp_data(join_categories)

    def test_combination_coverage_without_filter(self):
        self.assertEqual(self.rrc.calculate_combination_coverage(), round(5/7, 4))

    def test_combination_coverage_with_filter_1(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 1), 0.75)

    def test_combination_coverage_with_filter_2(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 2), 1)

    def test_combination_coverage_with_filter_3(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 3), 0)

    def test_ks_test_0(self):
        self.rrc.comparison_data['dummy_indicator'] = 0
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 0, places = 2)

    def test_ks_test_1(self):
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 1, places = 2)

    def test_ks_test_1_filter(self):
        self.rrc.comparison_data['dummy_indicator'] = [10,20,30,0,0]
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator', filter_name='dummy_category', filter_value=1)[1], 1, places = 2)

    def test_original_indicator_mean(self):
        self.assertEqual(self.rrc.calculate_original_indicator_mean('dummy_indicator'), 40)

    def test_original_indicator_mean_filter(self):
        self.assertEqual(self.rrc.calculate_original_indicator_mean('dummy_indicator', filter_name = 'dummy_category', filter_value = 1), 25)

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

    def test_mean_absolute_percentage_error_50_filter(self):
        self.rrc.joined_data['dummy_indicator_y'] = [5,10,15,50,60]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', filter_name = 'dummy_category', filter_value = 1)[0], 50)

    def test_mean_absolute_percentage_error_200_filter(self):
        self.rrc.joined_data['dummy_indicator_y'] = [5,10,15,150,180]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', filter_name = 'dummy_category', filter_value = 2)[0], 200)

    def test_mad_absolute_percentage_error_0(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,30,50,60]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[1], 0)

    def test_mad_absolute_percentage_error_50(self):
        self.rrc.joined_data['dummy_indicator_y'] = [10,20,15,100,120]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator')[1], 50)

    def test_mad_absolute_percentage_error_0_filter(self):
        # This test works since it's MEDIAN and not MEAN absolute deviation
        self.rrc.joined_data['dummy_indicator_y'] = [4,20,30,100,120]
        self.assertEqual(self.rrc.calculate_absolute_percentage_error_metrics('dummy_indicator', filter_name = 'dummy_category', filter_value = 1)[1], 0)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    # runner.run(suite())

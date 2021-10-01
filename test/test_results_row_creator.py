# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/

from src import results_row_creator
import unittest
import pandas as pd

class TestResultsRowCreator(unittest.TestCase):
    def setUp(self):
        self.rrc = results_row_creator.ResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2,3]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))
        self.dirrc = results_row_creator.DomInbResultsRowCreator(None, None)
        self.outbrrc = results_row_creator.OutbResultsRowCreator(None, None)

    def test_combination_coverage_without_filter(self):
        self.assertEqual(self.rrc.calculate_combination_coverage(), round(5/7, 4))

    def test_combination_coverage_with_filter_1(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 1), 0.75)

    def test_combination_coverage_with_filter_2(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 2), 1)

    def test_combination_coverage_with_filter_3(self):
        self.assertEqual(self.rrc.calculate_combination_coverage('dummy_category', 3), 0)

    def test_ks_test_0(self):
        self.rrc.original_data['dummy_indicator'] = [10,20,30,40,50,60,70]
        self.rrc.comparison_data['dummy_indicator'] = 0
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 0, places = 2)

    def test_ks_test_1(self):
        self.rrc.original_data['dummy_indicator'] = [10,20,30,40,50,60,70]
        self.rrc.comparison_data['dummy_indicator'] = [10,20,30,50,70]
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator')[1], 1, places = 2)

    def test_ks_test_1_filter(self):
        self.rrc.original_data['dummy_indicator'] = [10,20,30,40,50,60,70]
        self.rrc.comparison_data['dummy_indicator'] = [10,20,30,0,0]
        self.assertAlmostEqual(self.rrc.calculate_ks_test('dummy_indicator', filter_name='dummy_category', filter_value=1)[1], 1, places = 2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestResultsRowCreator('setUp'))

    suite.addTest(TestResultsRowCreator('test_combination_coverage_without_filter'))
    suite.addTest(TestResultsRowCreator('test_combination_coverage_with_filter_1'))
    suite.addTest(TestResultsRowCreator('test_combination_coverage_with_filter_2'))
    suite.addTest(TestResultsRowCreator('test_combination_coverage_with_filter_3'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

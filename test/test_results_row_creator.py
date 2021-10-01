# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/

from src import results_row_creator
import unittest
import pandas as pd

class TestResultsRowCreator(unittest.TestCase):
    def setUp(self):
        self.rrc = results_row_creator.ResultsRowCreator(None, None)
        self.dirrc = results_row_creator.DomInbResultsRowCreator(None, None)
        self.outbrrc = results_row_creator.OutbResultsRowCreator(None, None)

    def test_combination_coverage_without_filter(self):
        self.outbrrc = results_row_creator.OutbResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2,3]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))

        self.assertEqual(self.outbrrc.calculate_combination_coverage(), round(5/7, 4))

    def test_combination_coverage_with_filter_1(self):
        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2,3]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))

        self.assertEqual(self.dirrc.calculate_combination_coverage('dummy_category', 1), 0.75)

    def test_combination_coverage_with_filter_2(self):
        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2,3]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))
        
        self.assertEqual(self.dirrc.calculate_combination_coverage('dummy_category', 2), 1)

    def test_combination_coverage_with_filter_3(self):
        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2,3]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))

        self.assertEqual(self.dirrc.calculate_combination_coverage('dummy_category', 3), 0)

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

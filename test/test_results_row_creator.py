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

    def test_combination_coverage_with_filter_1(self):
        self.dirrc = results_row_creator.DomInbResultsRowCreator(original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2]}),
                                                                comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]}))
        # self.dirrc.original_data = pd.DataFrame({'dummy_category':[1,1,1,1,2,2]})
        # self.dirrc.comparison_data = pd.DataFrame({'dummy_category':[1,1,1,2,2]})

        self.assertEquals(self.dirrc.calculate_combination_coverage('dummy_category', 1), 0.75)
        # self.assertEquals(self.dirrc.calculate_combination_coverage('dummy_category', 2), 1)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestResultsRowCreator('setUp'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

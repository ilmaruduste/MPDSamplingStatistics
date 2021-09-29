# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/

from src import results_processor
import unittest

class TestInputDataSelection(unittest.TestCase):
    def setUp(self):
        self.rp = results_processor.ResultsProcessor()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestInputDataSelection('setUp'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

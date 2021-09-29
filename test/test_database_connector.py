# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/


from src import database_connector
import unittest
import yaml
import time

class TestDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.dc = database_connector.DatabaseConnector()

    def test_load_config(self):
        with yaml.safe_load(open("./test/configs/test_database_connector_conf.yaml", "r")) as conf:
           self.dc.load_conf(conf)
        self.assertEqual(self.dc.db_host, "localhost")
        self.assertEqual(self.dc.db_name, "dummy_name")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDatabaseConnector('setUp'))
    suite.addTest(TestDatabaseConnector('test_load_config'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

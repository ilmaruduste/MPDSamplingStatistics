# Read up on unittests: https://docs.python.org/3/library/unittest.html
# https://realpython.com/python-testing/


from src import input_data_selector
import unittest
import yaml
import time

class TestInputDataSelection(unittest.TestCase):
    def setUp(self):
        with open("./test/configs/test_input_data_selection_conf.yaml", "r") as file:
            conf = yaml.safe_load(file)
            self.ids = input_data_selector.InputDataSelector(conf)

    def test_load_tblname(self):
        self.ids.load_table_name("dummy")
        self.assertEqual(self.ids.table_name, "dummy")

    def test_query_1_schema(self):
        self.ids.data_schemas = ["dummy_schema"]
        self.ids.data_types = ["100% data"]
        self.ids.table_name = "dummy_table"

        correct_query = '''SELECT *, "100% data" AS data_type FROM dummy_schema.dummy_table\n'''

        self.ids.create_sql_query()
        self.assertEqual(self.ids.query, correct_query)

    def test_query_2_schemas(self):
        self.ids.data_schemas = ["dummy_schema1", "dummy_schema2"]
        self.ids.data_types = ["100% data", "5% data"]
        self.ids.table_name = "dummy_table"

        correct_query = '''SELECT *, "100% data" AS data_type FROM dummy_schema1.dummy_table\nUNION\nSELECT *, "5% data" AS data_type FROM dummy_schema2.dummy_table\n'''

        self.ids.create_sql_query()
        self.assertEqual(self.ids.query, correct_query)

    def test_query_multiple_schemas(self):
        self.ids.data_schemas = ["dummy_schema1", "dummy_schema2", "dummy_schema3"]
        self.ids.data_types = ["100% data", "5% data", "1% data"]
        self.ids.table_name = "dummy_table"        

        correct_query = '''SELECT *, "100% data" AS data_type FROM dummy_schema1.dummy_table\nUNION\nSELECT *, "5% data" AS data_type FROM dummy_schema2.dummy_table\nUNION\nSELECT *, "1% data" AS data_type FROM dummy_schema3.dummy_table\n'''

        self.ids.create_sql_query()
        self.assertEqual(self.ids.query, correct_query)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestInputDataSelection('setUp'))
    suite.addTest(TestInputDataSelection('test_load_config'))
    suite.addTest(TestInputDataSelection('test_load_tblname'))
    suite.addTest(TestInputDataSelection('test_query_1_schema'))
    suite.addTest(TestInputDataSelection('test_query_2_schemas'))
    suite.addTest(TestInputDataSelection('test_query_multiple_schemas'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

import pandas

class ResultsProcessor:

    def __init__(self, input_data = None):
        self.data = input_data

    def load_data(self, input_data):
        self.data = input_data
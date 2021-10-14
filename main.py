# TODO: Implement functionality to choose config, defaulting to config.yaml

import os
from time import gmtime, strftime
from src import results_processor
from src import database_connector
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', 
    '--config', 
    action = "store", 
    help = "The relative or absolute path of the config (yaml file) that contains the arguments to run this program.",
    dest = "config_path"
    )
args = parser.parse_args()

print("Opening config...")
with open(args.config_path, "r") as file:
    conf = yaml.safe_load(file)
print("Config opened!")

current_time = strftime("%Y%m%d_%H%M%S", gmtime())
filename = current_time + conf['OUTPUT DATA']['FILENAME']
output_path = os.path.join(conf['OUTPUT DATA']['FOLDER'], filename)

print(f"Connecting to database {conf['DATABASE CONNECTION']['DB NAME']}...")
connection = database_connector.DatabaseConnector()
connection.load_conf(conf)
connection.connect_to_db()
print("Connection to database established!")

print("Processing results...")
results_processor = results_processor.ResultsProcessor(conf, connection)
final_data = results_processor.process_results()

print("Results processed!")
print(f"Outputting results comparison .csv file to {output_path}.")
final_data.to_csv(output_path, sep = ';')
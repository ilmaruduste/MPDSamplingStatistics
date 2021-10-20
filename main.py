# TODO: Implement functionality to choose config, defaulting to config.yaml

import os
from time import localtime, strftime
from src import results_processor
from src import database_connector
import argparse
import yaml

start_time = localtime()
print(f"{strftime('%Y-%m-%d %H:%M:%S', start_time)} STARTING RESULTS COMPARISON SCRIPT")

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

current_time = strftime("%Y%m%d_%H%M%S", localtime())
filename = current_time + "_" + conf['OUTPUT DATA']['FILENAME']
output_path = os.path.join(conf['OUTPUT DATA']['FOLDER'], filename)

print(f"Connecting to database {conf['DATABASE CONNECTION']['DB NAME']}...")
with database_connector.DatabaseConnector() as connection, database_connector.DatabaseConnector() as second_connection:
    connection.load_conf(conf, 'DATABASE CONNECTION')
    connection.connect_to_db()
    print("Connection to database established!")

    try:
        second_connection.load_conf(conf, 'DATABASE CONNECTION 2')
        second_connection.connect_to_db()
        print("Connection to second database established!")

    except:
        print("Connection to second database NOT established!")

    print("Processing results...")
    results_processor = results_processor.ResultsProcessor(conf, connection, second_connection)
    final_data = results_processor.process_results()

    print("Results processed!")
    print(f"Outputting results comparison .csv file to {output_path}.")
    final_data.to_csv(output_path, sep = ';', index = False)

end_time = localtime()
print(f"{strftime('%Y-%m-%d %H:%M:%S', end_time)} ENDING RESULTS COMPARISON SCRIPT")
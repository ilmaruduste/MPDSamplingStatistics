# MPDSamplingStatistics
This program is a tool to compare different MPD based results between eachother, conduct statistical tests and output a .csv file with different statistical indicators.

## Running
To run the program, navigate to the project directory in your terminal and run the following command:

    python main.py -c ./configs/your_config_name_here.yaml

This will produce an output file with a path that is specified in the config. <b>NB!</b> You will have to create your own config, as every database connection and setup is different. 

## Testing
To run the tests for this program, navigate to the main directory and run the following:
        
    python -m unittest

...or if you want it with a more verbose output, add a "-v" to the end of the command.
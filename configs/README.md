The .yaml config consists of 3 main categories: Database Connection, Input Data and Output Data.

Two examples are provided in the downloadable repository. One is for multiple schema, one database use (`config.yaml`) and the other is for 2 databases, 2 schema use (`config_2_databases.yaml`).

<b>NB!</b> You have to take the example configs and tune them to your own particular use case.

## Database Connection
    DB HOST: 'localhost'
    DB NAME: 'dummy_database'
    DB USERNAME: 'dummy_user'
    DB PASSWORD: 'dummy_password'
    DB PORT: '5432'

This category specifies the PSQL database that the script connects to and pulls the data from. In the case of 2 databases, there will also be DATABASE CONNECTION2 to specify the other database.

## Input Data

    DATA SCHEMAS: ['du_dummy_results', 'du_dummy_results_sampled']
    CORRESPONDING TYPES: ['100% data', '5% data'] 
    TABLE NAMES: ['dummy_results_table', 'dummy_results_table_2']
    INDICATORS: ['unique_visitor_cnt', 'trip_present_cnt'] 
    DATA SOURCE: 'DomesticInbound' 
    JOIN CATEGORIES: ['lau_id', 'lau_level','period']
    GROUP NAME: ['lau_level']
    COEF VALUES: [1,20]  

This category specifies the format of the input data.

<b>DATA SCHEMAS:</b> The first element of this array is the database schema of the baseline results that every other set of results will be compared to. The other elements in the array are the schemas of the results that are compared to the first one.

<b>CORRESPONDING TYPES:</b> Each element here corresponds to a schema in DATA SCHEMAS. If this array only has 2 elements like in the example, then the output file will have just 1 data type, 5% data, since it's compared to 100% data.

<b>TABLE NAMES:</b> The names of the tables in each schema. For n tables in the array, there should be n tables in each schema as well. So the example above would lead to `du_dummy_results.dummy_results_table` and `du_dummy_results.dummy_results_table_2` (100% data) being compared to `du_dummy_results_sampled.dummy_results_table` and `du_dummy_results_sampled.dummy_results_table_2` (5% data).

<b>INDICATORS:</b> These are the data columns in the tables that will be compared. The values in these indicator columns need to be numeric, otherwise the percentage and logarithmic error metrics won't work.

<b>DATA SOURCE:</b> 'DomesticInbound' or 'Outbound'. The former uses extra grouping values to generate extra columns/breakdowns in output and the latter doesn't (see GROUP NAME).

<b>JOIN CATEGORIES:</b> The columns by which compared tables will be joined together. If there aren't enough categories here, then the script might create too many breakdowns, so the join categories need to be as specific and thorough as possible.

<b>GROUP NAME:</b> This array houses all the columns that the user wishes to see a detailed breakdown of in the output in addition to table name, data type and indicator.

<b>COEF VALUES:</b> If your indicators need to be multiplied by some number in order to match the baseline data, then use this (e.g. your comparable data is 5% sampled, then you can multiply every indicator by 20 to match the baseline results). This has as many elements as schemas in DATA SCHEMAS and each coef is applied to each corresponding DATA SCHEMA.

## Output Data
    FOLDER: './output'
    FILENAME: 'dummy_statistics.csv'
    TYPE: ['long']   

This category specifies the format and location of output data.

<b>FOLDER:</b> The path of the folder where output results are saved to.

<b>FILENAME:</b> The name of the output file saved when the script finishes. The filename also has a YYYYMMDD_HHmmss in front of the name, so if you were to run the example config on the 3rd of Dec 2021 3PM, then the resulting file would be `20211203_150334_dummy_statistics.csv`.

<b>TYPE:</b> Format of the output results. Currently the only possible choice is 'long', although future plans include having a 'wide' setting as well.
import pandas as pd
from pyspark.sql import SparkSession
from data_cleaning import clean_data
from database_handler import store_data_in_database
from data_analysis import perform_graph_analysis


# Read data from CSV file
data = pd.read_csv('/Users/saimasharleen/PycharmProjects/pythonProject1/email-EuAll.txt', sep='\t')

# Replace 'your_database_name', 'your_username', 'your_password' with your actual credentials
# and 'email_table' with your desired table name
store_data_in_database(data, table_name='email_table')

# Display the column names
print(data.columns)

# Data Cleaning using the clean_data function from data_cleaning.py
data = clean_data(data)
# Create a SparkSession
spark = SparkSession.builder \
    .appName("EmailAnalysis") \
    .config("spark.jars", "/System/Volumes/Data/Users/saimasharleen/PycharmProjects/pythonProject1/graphframes-0.8.2-spark2.4-s_2.11.jar") \
    .getOrCreate()

# Replace table_name with your actual table name
table_name = 'data_table'
perform_graph_analysis(table_name)

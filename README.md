### Network Science Investigation on Social Dynamics

---
***Abstract***

The project is a big data system to examine and represent email conversation records and extract meaningful observations from patterns, through a number of technologies, namely the Gmail API, PostgreSQL, SQLite, Kafka, Apache Spark and the Girvan-Newman algorithm.

---

##### Functionalities

- Data retrieval from a pre-existing email dataset
  
- Data retrieval through the Gmail API and assignation of a unique identifier to each sender and receiver

- Data pre-processing through Kafka
  
- Creation and population of a database either in PostgreSQL or SQLite, depending on the desidered features and resources constraints

- Analysis of the networks resulting from communication logs

- Interactive visualization

---

##### Technologies

+ Gmail API
+ Kafka
+ PostgreSQL
+ SQLite
+ Apache Spark


---
Web Hosts:

+ Cloud Karafka
+ PythonAnywhere
  
---
Prerequisites:

+ Python >= 3.7
+ Spark >= 3.0.3
+ Python packages: confluent_kafka, json, random, pyspark, flask, csv, mysql.connector, psycopg2, networkx, pyspark
---
##### Architecture

![pipeline](https://github.com/saimasharleen/BDT2023-Group11/assets/126952273/088d3381-ed7b-45de-984f-215619070062)

---

##### Project files

> Dataset related
> 
> 1. `email-EuAll.txt`: basic dataset to run the code
> 2. `restful_api.py`: retrieves data thanks to the Gmail API and stores it in a PostgreSQL database
> 3. `data_producer.py`: reads data from the dataset and sends it to Kafka

> Data cleaning and storage
>
> 1. `data_cleaning.py`: connects to PostgreSQL and stores data in a table
> 2. `SQLite.py`: provides an alternative method of storage to PostgreSQL

> Preprocessing and analysis
>
> 1. `preprocessing.py`: retrieves data, preprocesses it and computes metrics for analysis
> 2. `data_analysis_spark.py`: performs data analysis through Apache Spark

> Folders:
> `Data`
> `Visualization`

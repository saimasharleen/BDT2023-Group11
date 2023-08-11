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
> 4. `email-En-core.json`: contain data in JSON format representing a directed graph. Each object in the "nodes" array represents a node in the graph, and it contains information about the node's label and ID.
> 5. `email-Eu-core-department-labels.txt`: file contains node labels associated with nodes in a graph. Each line in the file represents a node and its corresponding label.

> Data cleaning and storage
>
> 1. `data_cleaning.py`: connects to PostgreSQL and stores data in a table
> 2. `SQLite.py`: provides an alternative method of storage to PostgreSQL

> Preprocessing and analysis
>
> 1. `preprocessing.py`: retrieves data, preprocesses it and computes metrics for analysis
> 2. `data_analysis_spark.py`: performs data analysis through Apache Spark

> Folders:
> 
> `data`: Files related to datasets
> 
> `visualization`: Graphs, and other visual representations of the data and findings.
> 
> `code`:Files related to data analysis, such as scripts, and intermediate results.
> 
> `Report`: Here you can find overview of the project results included key findings, limitations, conclusions, and visualizations that represent the core outcomes. Also, the terminal commands of the project.
> 
> `Results`: Due to report pages limitation, we are putting all our project results in this folder.
---
##### How to run the project
+ run the "main.py"
python3 main.py
+ You can run a simple python2 HTTP server with this command:
  python3 -m http.server
+ Then you can navigate to any of the following files to see some visualizations:
  localhost:8000/low.html
  localhost:8000/low-node.html
  localhost:8000/high.html
  localhost:8000/high-node.html
The files labelled as "low" retained objects with the lowest centrality, whereas the files labelled as "high" retained things with the highest centrality. The files labelled as "node" contained the nodes exhibiting the highest or lowest centrality, whereas the files lacking visualisation focused solely on the edges.


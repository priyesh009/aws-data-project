#  Airflow Data Engineering Project:
In this readme file, I have shared my experience while creating this project, setup instructions, and thoughts.

## Senario

Implement an Airflow ([Apache Airflow](https://airflow.apache.org/)) DAG to process data from two separate sources and merge it into a single output file.  The DAG should run on a daily basis.  For the purpose of the exercise, both input and output can use the local file system.

Folders `Aitflow_Project\airflow\datasources\src1` and `Aitflow_Project\airflow\datasources\src2` will contain the input data. 
You can assume that a new file will appear daily in each of those folders, with the filename specifying the date of the data it contains. 
Source 1 data is expected to arrive between 1-3am the following day, in JSON format, while Source 2 data is expected to arrive between 4-5am, in CSV format (e.g. data_20210125.json will appear in the folder on January 26th between 1am and 3am, and engagement_20210125.csv will appear on January 26th between 4am and 5am).

The DAG should write to a CSV file the following: date, post id, shares, comments, and likes. All other fields should be ignored.  

Although the sample files are small, your program should be designed such that it could be used in the future to merge large files.

## Architecture Diagram
![Architecture Diagram](https://github.com/priyesh009/aws-data-project/blob/master/Azure_Databricks_Project/docs/DatabricksProject.jpg?raw=true)

## Some important project files locations
Inside airflow directory.
- **Airflow Dags:**  airflow/dags/dag_csv.py, airflow/dags/dag_json.py, airflow/dags/dag_merge.py
- **Merge logic python file:**  airflow/dags/utils/process_utils.py
- **Final Merged CSV file:** airflow/processed/final_data/*.csv 
- **Source files:** airflow/datasources/src*

## Quick Airflow Setup Steps
- Setup and start t2.large AWS EC2 instance.
- Login to the instance via putty and Install python, airflow, pandas, etc
- Modify airflow.cfg file if required 
- Create directories for source files and processed files and copy the source files.
- Create airflow dag (cn_dag.py) and python callable (cn_data_ing.py)and put it in dags directory.
- Instantiate airflow DB, run airflow scheduler and the airflow webserver command in putty.

## Project Development experience

In this project I have used python, pandas and airflow.  

- First, I started to work on the logic to merge to source files in my local using pandas, python, and Pycharm IDE and created **airflow/dags/utils/process_utils.py.py**. 
- I used pandas as I believe it can process large files efficiently.
- **Processing JSON:** While working on processing JSON files I noticed src1 JSON files were invalid JSON files. so I found a workaround using readlines method and read them as files and iterated over each row and processed the data.  
- I also used the String IO module to get rid of "ValueError: Protocol not known" error in one of the source JSON file
- **Processing CSV:** processing csv was straightforward. 
- I build the logic in such a way that it will process all existing files in the source folder.
- Luckily I already had an EC2 instance in my AWS account with airflow set up so I made use of the same for this exercise(which saved my time in setup) and added cn_data_ing.py in the **airflow/dags** folder.
- **Airflow Dags:** Then I started working on the airflow dags **airflow/dags/dag_csv.py**  Here I have created 3 tasks. task1 and task2 are the checks if the source files exist using BashOperator and task3 uses PythonOperator to execute the python callable. Task 3 deletes the source files. Similarly I am processing the json source files.
- schedule interval is set to daily and the start date for all tasks is 26th Jan 2021 in such a way that the task starts only after we receive files in both sources.
- Then I created multiple folders under **airflow/processed/** to store source and processed files. 
- At the end dag was successfully executed and the final result is stored in **airflow/processed/final_data/final_{Date on which file was processed}.csv**

## Pending Enhancements

In future I am planning to implement following things to improve the code and try to make it production-ready and scalable.

- The source files could be moved to another folder after processing in parquet format to save space.
- Celery executor can be used in airflow.cfg to handle large workflows with ability to scale infinitely. 
- Postgres or MySql for Airflow Metadata DB.
- As per my understanding schdule_interval applies at Dag level so, I would have created 3 Dags. one to process JSON files and moved processed file in some archive folder in parquet format with appropriate schedule interval, similarly for CSV files and 3rd Dags to merge files which will have a dependency on first two Dags.    
- Logic to process only CSV and JSON files and ignore other files from the source folder,  some data quality checks, more focus on data cleansing.
- Error handling, logging module, testing scripts and would have used Xcom, Sub-dags, etc if it makes sense. 
- use file sensor instead of bash and of make use of external sensors to trigger the merge dag after successful execution of previous dags instead of scheduling it.
- I will do more reserch on airflow and optimised the code.

# Data Engineering Project using Airflow, python and pandas


## Senario

Implement an Airflow ([Apache Airflow](https://airflow.apache.org/)) DAG to process data from two separate sources and merge it into a single output file.  The DAG should run on a daily basis.  For the purpose of the exercise, both input and output can use the local file system.

Folders `C:\Users\priye\Documents\Github\codingtest\airflow\cn_files\src1` and `C:\Users\priye\Documents\Github\codingtest\airflow\cn_files\src2` will contain the input data. 
You can assume that a new file will appear daily in each of those folders, with the filename specifying the date of the data it contains. 
Source 1 data is expected to arrive between 1-3am the following day, in JSON format, while Source 2 data is expected to arrive between 4-5am, in CSV format (e.g. data_20210125.json will appear in the folder on January 26th between 1am and 3am, and engagement_20210125.csv will appear on January 26th between 4am and 5am).

The DAG should write to a CSV file the following: date, post id, shares, comments, and likes. All other fields should be ignored.  

Although the sample files are small, your program should be designed such that it could be used in the future to merge large files.
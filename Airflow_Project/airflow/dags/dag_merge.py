#import the required libraries
import json
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators import BashOperator
from airflow.operators import PythonOperator
from process_utils import merge_csv_json_data, delete_files
#from airflow.contrib.sensors.file_sensor import FileSensor

with open('/home/ubuntu/airflow/config/config.json','r') as configFile:
    config_data = json.load(configFile)


json_processed_dir = config_data.get('processed')[0].get('json_processed_dir')
csv_processed_dir = config_data.get('processed')[0].get('csv_processed_dir')
merge_dir = config_data.get('merge_dir')
py_args = [json_processed_dir,csv_processed_dir,merge_dir]

#Defining the default arguments dictionary
args = {
	'owner': 'airflow',
	'start_date': datetime(2021,01,26,6,0),
	'retries': 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG('csv_json_merge', default_args=args, schedule_interval='@daily', catchup=False)

task1 = BashOperator(task_id='processed_csv_check', bash_command='shasum ~/airflow/processed/csv_data/csv*',retires=2, retry_delay = timedelta(seconds=15), dag=dag)

task2 = BashOperator(task_id='processed_json_check', bash_command='shasum ~/airflow/processed/json_data/json*',retires=2, retry_delay = timedelta(seconds=15), dag=dag)

#task3 is to process the source files
task3 = PythonOperator(task_id='merge_csv_json', python_callable=merge_csv_json_data, op_args=py_args, dag=dag)

#Task4 Delete files from source
task4 = PythonOperator(task_id='csv_processed_src_cleanup', python_callable=delete_files, op_args=[csv_processed_dir], dag=dag)

#Task5 Delete files from source
task5 = PythonOperator(task_id='json_processed_src_cleanup', python_callable=delete_files, op_args=[json_processed_dir], dag=dag)

#Task Dependencies
[task1 , task2] >> task3 >> [task4 , task5]

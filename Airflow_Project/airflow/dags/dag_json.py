#import the required libraries
import json
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators import BashOperator
from airflow.operators import PythonOperator
from process_utils import process_json,delete_files
#from airflow.contrib.sensors.file_sensor import FileSensor

with open('/home/ubuntu/airflow/config/config.json','r') as configFile:
    config_data = json.load(configFile)


json_source_dir = config_data.get('source')[0].get('json_source_dir')
json_processed_dir = config_data.get('processed')[0].get('json_processed_dir')
archive_dir = config_data.get('archive_dir')

py_args = [json_source_dir,json_processed_dir,None]

#Defining the default arguments dictionary
args = {
	'owner': 'airflow',
	'start_date': datetime(2021,01,26,5,0),
	'retries': 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG('json_data_ingesation', default_args=args, schedule_interval='@daily', catchup=False)

# #task1 is to check file exist in json src1
# task1 = FileSensor(
#                  task_id="json_file_check",
#                  filepath="/home/ubuntu/airflow/datasources/src1/",
#                  #fs_conn_id="fs_default" # default one, commented because not needed
#                  poke_interval= 20,
#                  dag=dag
#               )
#task1 is to check file exist in src1
task1 = BashOperator(task_id='json_file_check', bash_command='shasum ~/airflow/datasources/src1/data*',retires=2, retry_delay = timedelta(seconds=15), dag=dag)

#task3 is to merge the source files
task2 = PythonOperator(task_id='process_json', python_callable=process_json, op_args=py_args, dag=dag)

#TASK3 Delete files from source
task3 = PythonOperator(task_id='json_src_cleanup', python_callable=delete_files, op_args=[json_source_dir], dag=dag)

#Task Dependencies
task1 >> task2 >> task3
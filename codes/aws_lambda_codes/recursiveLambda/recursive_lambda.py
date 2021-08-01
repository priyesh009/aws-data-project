"Extract data from Database"
import os
import json
from utilities.utils import process_data#, put_data_s3
from lambda_layers import put_data_s3
from utilities.processor import Processor
#from notification library import notifunc
s3_bucket = os.environ.get('targetS3Bucket')
secret=os.environ.get('DBsecret')
target_file_location=os.environ.get('TargetLoc') 

def lambda_handler(event, context):
  '''Main Lambda function used to open the config file, connect to heroku postgresql and get the data.
    we can also enable service now notification
  '''
  try:
    print(f'Lambda Context: {context}')
    with open('config/table_sql.json') as data:
       jsondata = json.load(data)
      
    processor = Processor(event)
    return processor.process(context, jsondata.get('Tables'), process_data,s3_bucket,target_file_location,put_data_s3,secret)
  except Exception as e:
    print(e)


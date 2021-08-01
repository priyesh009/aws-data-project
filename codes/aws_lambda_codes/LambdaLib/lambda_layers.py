import time
import json
from urllib import parse

from botocore.exceptions import ClientError
import boto3

class Timer: 
    def __init__(self, function): 
        self.function = function 
      
    def __call__(self,*args,**kwargs): 
        start = time.time() 
        result = self.function(*args,**kwargs) 
        time_lapse = (time.time()-start)
        print(f'time taken for {self.function.__name__} to run is : {time_lapse} secs')
        return result


@Timer
def generic_retrieve_secret(secretid=''):
  '''Generic function to retrieve secrets. Takes secret id as parameter
  Returns the secret string as a dictionary'''
  sm = boto3.client("secretsmanager", region_name="us-east-2")
  "Retrive temporty user password from Secrets Manager"
  user_secret_id = secretid
  try:
    user_secret = sm.get_secret_value(SecretId=user_secret_id)
    user_creds = json.loads(user_secret['SecretString'])
    user_creds['password'] = parse.quote_plus(user_creds['password'])
    return user_creds
  except ClientError as err:
    print('Unable to Retrieve user password: ERROR', err)
    return 'password'

@Timer
def put_data_s3(payload,op_file_name,target_s3_bucket):
    '''Generic function to put the Data in Json format in S3 bucket'''
    "This function takes python dictionary and writes json file in s3 bucket."
    s3 = boto3.resource('s3')
    s3object = s3.Object(target_s3_bucket, op_file_name)
    s3object.put(
    Body=(bytes(json.dumps(payload).encode('UTF-8')))
    )
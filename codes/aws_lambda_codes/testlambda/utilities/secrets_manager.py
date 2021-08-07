import json
import boto3
from botocore.exceptions import ClientError
#from urllib import parse

sm = boto3.client("secretsmanager", region_name="ap-south-1")

def retrieve_postgres_secret(secretid=''):
  try:
    db_secret = sm.get_secret_value(SecretId=secretid)
    db_creds = json.loads(db_secret['SecretString'])
    return 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(**db_creds)

  except ClientError as err:
    print('Unable to Retrieve user password: ERROR', err)
    return 'password'
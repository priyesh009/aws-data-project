import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from utilities.secrets_manager import retrieve_postgres_secret


class Processor:
  def __init__(self, event):
    self.event = event

  def process(self, context, items, process_data,s3_bucket,path,put_s3,secret):
    "This method Processes the Data and puts it in S3"
    if self.event.get('detail-type') == "Scheduled Event":
      print('This function is invoked by scheduled event')
      try:
        db_conn_str = retrieve_postgres_secret(secret)
        for item in items:
          s3_key= path + item.get('table_name') + '/data/inbox/' + item.get('table_name') + '_data.json'
          payload = {
          "s3_path": s3_key,
          "sql_query" : item.get('sql_query'),
          "conn":db_conn_str,
          "table_name": item.get('table_name')
          }
          self._make_recursive_call(context,payload)
        return 'Successfully invoked lambda function for all source tables'
      except Exception as exp:
        print('Exception', exp)
        raise

    else:
      try:
        print('This function is invoked by recursive lambda function.')
        s3_path=self.event.get('s3_path')
        table_nm=self.event.get('table_name')
        print(f'Processing data from else block for Table: {table_nm}')
        sql_query=self.event.get('sql_query')
        conn = self.event.get('conn')
        engine = create_engine(conn)
        data,no_rows=process_data(engine,sql_query)
        print(f'Data successfully extracted for Source Table: {table_nm}. Number of rows are: {no_rows}')
        if data:
          put_s3(data, s3_path ,s3_bucket)
          print(f'S3 put succeeded for Table: {table_nm}')
        else:
          print(f'Empty Source Table: {table_nm}. Therefore not loading data in S3')
        return f'Successfully processed {table_nm}'
      except SQLAlchemyError as err:
        err_msg = 'Lambda SQL ERROR:'
        print(err_msg, err)
        raise
      except Exception as exp:
        print('Exception', exp)
        raise



  def _make_recursive_call(self, context,payload):
    "This method invokes the lambda functions for each source table"
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName=context.function_name,
                          InvocationType='Event',
                          Payload=json.dumps(payload))
    return

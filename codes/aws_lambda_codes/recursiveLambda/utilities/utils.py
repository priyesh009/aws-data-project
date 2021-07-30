import boto3
import json

s3 = boto3.resource('s3')

def put_data_s3(payload,op_file_name,target_s3_bucket):
    "This function takes python dictionary and writes json file in s3 bucket."
    s3object = s3.Object(target_s3_bucket, op_file_name)
    s3object.put(
    Body=(bytes(json.dumps(payload).encode('UTF-8')))
    )
    

def process_data(engine,sql):
    "This function takes SQLAlchemy's postgres DB engine and the SQL Query to extract the data from source and return the data in form of python dictionary."
    with engine.connect():
        res = engine.execute(sql)

    headers= res.keys()
    data =res.fetchall()
    final_dict = {}
    dict_list=[]
    for row in data:
        string_row = [str(e) for e in row]
        rec = dict(zip(headers, string_row))
        dict_list.append(rec)

    final_dict['Results'] = dict_list
    if final_dict['Results']:
      return final_dict, len(data)
    else:
      return None,0

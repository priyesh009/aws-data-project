# Extract Data from database using recursive Lambda function

## Introduction 
This document talks about the process to on board from a database to aws S3 bucket using lambda function in a recursive fashion.
This is the most innovative thing which I developed recently. The Idea was to on-board data in a serverless fashion and land it in to Amazon S3 bucket in a cost effective manner.

So, in this process I am taking advantage of AWS lambda function's concurrent execution capability and Invoking it recursively for each table which needs to be on-boarded in S3. In simple words if we have 50 source tables then we would invoke this lambda function 50 times parallely to extract the data from the database tables. In this we get 15min for lambda execution time for each source table without creating 50 lambda functions for each table. This is much better that having single lambda invocation trying to extract data from 50 source tables which might lead to lambda execution timeout error.

## How did it make a difference to the business or the organization
This process helped my team to save cost and introduce new way of on-boarding data which helped us to reidesign few other existing boarding processes and save cost.

## Techinical Design


### Architecture and Flow
![Architecture Diagram](https://github.com/priyesh009/aws-data-project/blob/master/codes/aws_lambda_codes/recursiveLambda/docs/rec_lambda.png?raw=true)
### Considerations
The following points were considered before on-boarding the Lilly Play data:

As the Volume of the data was very high in the source DB therefore, the decision to onboard the data with AWS Recursive Lambda was finalized.
The Data will only land in S3 if the source tables are not empty. 

### Technical Details

#### AWS Services 
- AWS Lambda Function
- Amazon S3
- AWS Secrets Manager
- AWS CloudFormation
- AWS Event Bridge

####  Python libraries
- SQLAlchemy

**Recursive Lambda Function**
A lambda function edb_iris_land_lilly_play_in_s3raw is created in edb via CloudFormation in sam_template.yml.
- recursive_lambda.py
The recursive_lambda.py acts as our AWS lambda function's handler. This is the driving file of data extraction process landing process and performs the below functions.

Imports Processor Class, python functions from utils and load the table_name.json from config directory.

lambda_handler is used to connect to the DB and fetches the data per table by iterating over the table list and its corresponding SQL Query mentioned in the config file. This function passes the event along with parameters like S3 bucket name, S3 Key, DB string, and data processing python function to the process method of Processor Class.

We could also making use of some notification utility to send email or alert in case on failure.

- table_name_list.json
The config/table_name_list.json is the config file. It contains the list of tables and their corresponding SQL query which helps to extract data from the source.

Each record in this file contains two keys the source table names and the SQL query to extract data from Database.

- utils.py
Ths utils.py has the python function which helps us to set up the objects in S3. The functions are explained as follows.

process_data function takes DB connection and the SQL query as input and connects to the DB. It gets the header and the rows and stores them in form of a python dictionary in the 'Result' key.
- processor.py
Ths utils.py has the Class Processor and its methods which helps us to make the recursive calls and invoke a lambda per table. The functions are explained as follows.

- init method is used to initialize the event.
process method takes lambda context, tables_names, process_data function,s3_bucket,s3_key,put_s3 function, and DB Connection as input. Then it checks if the event is a scheduled event. If it is a scheduled event then it iterates over the table list defined in the config file and for each table, it will invoke the lambda function again which eventually calls the _make_recursive_call method with parameters containing table name, S3 key, DB connections and SQL query.
Else it will execute the process_data function and finally calls the S3 put function to load data in target S3 bucket.

So, if there are 30 source tables then there would be 31 invocations. one would be to iterate over the table list and the other 30 to process individual tables.

- _make_recursive_call method takes the lambda context and lambda event as input and invokes the lambda function with the help of boto3 SDK.
secrets_manager.py
Ths secrets_manager.py has the python function which helps us to get the objects from the secrets manager. The functions are explained as follows.

generic_retrieve_secret function is used to retrieve the L DB connection details which are manually entered through AWS console or in case we can also attach the secret with the Database if it resides in AWS.




they wanted to go with fargate approcah but data was less so i suggested to go with lmbda utilizing lambda's cncurreny  funtinality

it saved business costs

s3 reouer vs s3 client for copying
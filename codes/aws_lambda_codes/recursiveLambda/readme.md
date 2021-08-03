# Data On-Boarding using Recursive AWS Lambda

## Introduction 
This document talks about the process to on-board data from any relational database to AWS S3 bucket using lambda function in a recursive fashion.
This is my idea and one of the most innovative things which I developed recently. The Idea was to on-board data in a **serverless fashion** and land it in to Amazon S3 bucket in a **cost effective manner**.

So, in this process I am taking advantage of AWS lambda function's concurrent execution capability and Invoking it recursively for each table which needs to be on-boarded in S3. In simple words if we have 100 source tables then we would invoke this lambda function 100 times parallely to extract the data from the database tables. In this we get 15min for lambda execution time for each source table without creating 100 lambda functions for each table. This is much better that having single lambda invocation trying to extract data from 100 source tables which might lead to lambda execution timeout error.

## How did it make a difference to the business or the organization
- This process helped our team to save cost as the data processing is Serverless 
- It introduced a new way of on-boarding data which helped us to redesign few other existing data on-boarding processes and save money.
- Previously we were planning to use ECS to on-board the data which would have added complexity, more management and cost. By going with this approcah we save cost, time and resource. With this I was able to complete more tasks than planned.

## Technical Design


### Architecture and Data Flow
![Architecture Diagram](https://github.com/priyesh009/aws-data-project/blob/master/codes/aws_lambda_codes/recursiveLambda/docs/rec_lambda.png?raw=true)
### Considerations
The following points were considered before on-boarding the data:

- As the Volume of the data was not very high in the source DB therefore, the decision to onboard the data with AWS Recursive Lambda was finalized.
- As per the test I performed with the Lambda function. I was able to copy more than 5-6 GBs od data before erroring out with 15min timeout. So, basically we can easily copy data from source table even if it is around 5-6 GB. 

- In case we get terabytes of data per table then I would make sense to pivot to ECS fargate for data on-boarding. 

- The Data will only land in S3 if the source tables are not empty. 
- The Lambda Function can be invoked on a desired frequency with the help of Event Bridge Rules.
- 

### Technical Details
 
#### AWS Services 
- AWS Lambda Function
- Amazon S3
- AWS Secrets Manager
- AWS CloudFormation
- AWS Event Bridge

####  Programming languages and Libraries
- SQLAlchemy
- Python
- SQL
- YAML and JSON

**Recursive Lambda Function**:
A lambda function RecursiveLambda is created in my personal AWS account via CI/CD setup configure with this GitHub Repository.     

CloudFormation YAML code for this lambda setup is at this location in Resources section with resource name **RecursiveLambda**: https://github.com/priyesh009/aws-data-project/blob/master/samTemplate.yaml 

#### **recursive_lambda.py**
The recursive_lambda.py acts as our AWS lambda function's handler. This is the driving file of data extraction process landing process and performs the below functions. Location: https://github.com/priyesh009/aws-data-project/blob/master/codes/aws_lambda_codes/recursiveLambda/recursive_lambda.py

- Imports Utilities: Processor Class from processor.py and python functions from utils.py. 
- Imports s3_put function from **lambda layers**. In Lambda Layers I am alos making use of Timer Class to keep a track of method execution time. Location: https://github.com/priyesh009/aws-data-project/blob/master/codes/aws_lambda_codes/LambdaLib/python/lambda_layers.py
- Loads the table_sql.json from config directory. 

lambda_handler is used to connect to the DB and fetches the data per table by iterating over the table list and its corresponding SQL Query mentioned in the config file. This function passes the event along with parameters like S3 bucket name, S3 Key, DB string, and data processing python function to the process method of Processor Class.

We could also making use of some notification utility to send email or alert in case on failure.

#### **config/table_sql.json**
The config/table_sql.json is the config file. It contains the list of tables and their corresponding SQL query which helps to extract data from the source. Location: https://github.com/priyesh009/aws-data-project/tree/master/codes/aws_lambda_codes/recursiveLambda/config

Each record in this file contains two keys the source table names and the SQL query to extract data from Database.

#### **utils.py**
The utils.py has the python function which helps us to set up the objects in S3. The functions are explained as follows. Location: https://github.com/priyesh009/aws-data-project/tree/master/codes/aws_lambda_codes/recursiveLambda/utilities

- **process_data** function takes DB connection and the SQL query as input and connects to the DB. It gets the header and the rows and stores them in form of a python dictionary in the 'Result' key.
#### **processor.py**
Ths utils.py has the Class Processor and its methods which helps us to make the recursive calls and invoke a lambda per table. The functions are explained as follows.

- **Dunder __init__** method is used to initialize the event.
process method takes lambda context, tables_names, process_data function,s3_bucket,s3_key,put_s3 function, and DB Connection as input. Then it checks if the event is a scheduled event. If it is a scheduled event then it iterates over the table list defined in the config file and for each table, it will invoke the lambda function again which eventually calls the _make_recursive_call method with parameters containing table name, S3 key, DB connections and SQL query.
Else it will execute the process_data function and finally calls the S3 put function to load data in target S3 bucket.

So, if there are 30 source tables then there would be 31 invocations. one would be to iterate over the table list and the other 30 to process individual tables.

- **_make_recursive_call** method takes the lambda context and lambda event as input and invokes the lambda function with the help of boto3 SDK.
#### **secrets_manager.py**: The secrets_manager.py has the python function which helps us to get the objects from the secrets manager. The functions are explained as follows.

- **generic_retrieve_secret** function is used to retrieve the DB connection details which are manually entered through AWS console or in case we can also attach the secret with the Database if it resides in AWS. However, if the Database resides in the AWS then is possible to configure the secret's manager with RDS and also enable the secrets rotation lambda.

#### test_lambda_handler.py
Unitest test cases for the lambda_handler function

### Pending Enhancements

In future I am planning to implement following things to improve the code.

- enable logging module
- wirte more unittest cases
- install python dependencies in the requirements.txt in the code build phase.

## You may also check my other projects which I have implemented at my free time

- **Data Engineering Project using Airflow**: https://github.com/priyesh009/aws-data-project/tree/master/Airflow_Project
- **Data Engineering Project using Azure Databricks**: https://github.com/priyesh009/aws-data-project/tree/master/Azure_Databricks_Project
- **Data Engineering Project using Kinesis Data Stream and Firehose**: TBA 
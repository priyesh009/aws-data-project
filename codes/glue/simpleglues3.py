
#########################################
### IMPORT LIBRARIES AND SET VARIABLES
#########################################
 
#Import python modules
from datetime import datetime

#Import pyspark modules
from pyspark.context import SparkContext
import pyspark.sql.functions as f
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Test').getOrCreate()

#Import glue modules
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

#Initialize contexts and session
spark_context = SparkContext.getOrCreate()
glue_context = GlueContext(spark_context)
session = glue_context.spark_session

#Parameters
# glue_db = "edureka_db"
# glue_tbl = "read"
# s3_write_path = "s3://glueedurekatest/write" 
s3_read_location = ""
s3_write_location = ""
#########################################
### EXTRACT (READ DATA)
#########################################

dt_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Glue009 job EXE ","Start time:", dt_start)

#Read movie data to Glue dynamic frame
# dynamic_frame_read = glue_context.create_dynamic_frame.from_catalog(database = glue_db, table_name = glue_tbl)

dynamic_frame_read = glue_context.create_dynamic_frame_from_options(connection_type="s3", 
                                                                    connection_options = {'paths': [s3_read_location]},
                                                                    format="csv",
                                                                    format_options={"withHeader": True}
                                                                    )
                                       


#Convert dynamic frame to data frame to use standard pyspark functions
data_frame = dynamic_frame_read.toDF()

#########################################
### TRANSFORM (MODIFY DATA)
#########################################
data_frame.createOrReplaceTempView('people') 
data_frame.show(5)

# data_frame_aggregated=spark.sql("select int(year/10)*10 as decade, count(movie_title) as movie_count,avg(rating) as rating_mean from People  group by decade")

# data_frame_aggregated.show() 


#########################################
### LOAD (WRITE DATA)
#########################################


# #Create just 1 partition, because there is so little data
# data_frame_aggregated = data_frame_aggregated.repartition(1)

#Convert back to dynamic frame
dynamic_frame_write = DynamicFrame.fromDF(data_frame, glue_context, "dynamic_frame_write")



#Write data back to S3
glue_context.write_dynamic_frame.from_options(
frame = dynamic_frame_write,
connection_type = "s3",
connection_options = {"path": s3_write_location},format = "parquet"
)
 
#Log end time
dt_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start time:", dt_end)

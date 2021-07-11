// Databricks notebook source
import org.apache.spark.sql.types._
val depSchema = StructType(
  List(
              StructField("Department_id", IntegerType, true),
              StructField("Name", StringType, true)
              
	)
  
)

val dfD = spark.read
.option("header","true")
.schema(depSchema)
.csv("/mnt/landing/Department.csv")

// COMMAND ----------

dfD.write.mode(SaveMode.Append).format("delta").saveAsTable("datawarehousedb.department")  

// COMMAND ----------



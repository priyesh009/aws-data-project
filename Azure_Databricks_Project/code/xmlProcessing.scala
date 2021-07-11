// Databricks notebook source

import com.databricks.spark.xml._
val df = spark.read
    .option("rootTag","dataset").option("rowTag","record")
    .xml("/mnt/landing/SourceC*.xml")

// COMMAND ----------

val dfFlat = df
                .select(
                  "Employee_id"
                  ,"Age"
                  ,"Customer.First_Name"
                  ,"Customer.Last_Name"
                  ,"Gender"
                  ,"Salary"
                ,"Date_Of_Birth"
                ,"Age"
                ,"Country"
                ,"Department_id"
                ,"Date_Of_Joining"
                ,"Manager_id"
                ,"Currency"
                ,"End_Date"
                )


// COMMAND ----------

dfFlat.createOrReplaceTempView("EMP")

// COMMAND ----------

val dfCast = spark.sql("select cast(Employee_id as int),cast(Age as int),First_Name,Last_Name,Gender,cast(Salary as int),Date_Of_Birth,Country,cast(Department_id as int),Date_Of_Joining,cast(Manager_id as int),Currency,End_Date from EMP")

// COMMAND ----------

Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
val jdbcUsername = dbutils.secrets.get(scope = "jdbc", key = "username")
val jdbcPassword = dbutils.secrets.get(scope = "jdbc", key = "password")
val jdbcHostname = "pridb.database.windows.net"
val jdbcPort = 1433
val jdbcDatabase = "datawarehousedb"

// Create the JDBC URL without passing in the user and password parameters.
val jdbcUrl = s"jdbc:sqlserver://${jdbcHostname}:${jdbcPort};database=${jdbcDatabase}"

// Create a Properties() object to hold the parameters.
import java.util.Properties
val connectionProperties = new Properties()

connectionProperties.put("user", s"${jdbcUsername}")
connectionProperties.put("password", s"${jdbcPassword}")
val driverClass = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
connectionProperties.setProperty("Driver", driverClass)

// COMMAND ----------

dfCast
.write
.mode(SaveMode.Append) 
.jdbc(jdbcUrl,"datawarehousedb.employee",connectionProperties)


// COMMAND ----------

dfCast.write.mode(SaveMode.Append).format("delta").saveAsTable("datawarehousedb.employee") 

// COMMAND ----------



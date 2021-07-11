// Databricks notebook source
val containerName = "landing" 
val storageAccountName = "datavowelstorage9" 
val sas = "sp=racwdl&st=2021-07-10T03:25:55Z&se=2021-07-10T11:25:55Z&spr=https&sv=2020-08-04&sr=c&sig=rliwk8NQZASANKiXjnIopkzQ%2FG3q%2F3v8Ou8Vmzs5HU8%3D" 
val url = "wasbs://" + containerName + "@" + storageAccountName + ".blob.core.windows.net/" 
var config = "fs.azure.sas." + containerName + "." + storageAccountName + ".blob.core.windows.net"

// COMMAND ----------

// COMMAND ----------

dbutils.fs.mount( source = url, mountPoint = "/mnt/landing", extraConfigs = Map(config -> sas))



// COMMAND ----------

val containerName = "archive" 
val storageAccountName = "datavowelstorage9" 
val sas = "+R1ha/roIfJeyDsJdSHnDplxuXPGxL/WukHlc+f+a8zlp2ebX0EN/ZyvOlroD8ht8smp+PZOWQU4Tr2pvzjtRQ==" 
val url = "wasbs://" + containerName + "@" + storageAccountName + ".blob.core.windows.net/" 
var config = "fs.azure.sas." + containerName + "." + storageAccountName + ".blob.core.windows.net"

// COMMAND ----------

// COMMAND ----------

dbutils.fs.mount( source = url, mountPoint = "/mnt/archive", extraConfigs = Map(config -> sas))


// COMMAND ----------

// MAGIC %sql
// MAGIC Create database if not exists DatawarehouseDB

// COMMAND ----------

// MAGIC %scala
// MAGIC val df = spark.read
// MAGIC .option("header","true")
// MAGIC .csv("/mnt/landing/SourceA*.csv")

// COMMAND ----------

dbutils.fs.unmount("/mnt/landing")

// COMMAND ----------



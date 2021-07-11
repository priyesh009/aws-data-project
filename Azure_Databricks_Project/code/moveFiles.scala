// Databricks notebook source
val fileNmA = dbutils.fs.ls("/mnt/landing").map(_.name).filter(r => r.startsWith("SourceA"))(0)
val fileLocA = "dbfs:/mnt/landing/" + fileNmA
dbutils.fs.mv(fileLocA, "dbfs:/mnt/archive")

// COMMAND ----------

val fileNmB = dbutils.fs.ls("/mnt/landing").map(_.name).filter(r => r.startsWith("SourceB"))(0)
val fileLocB = "dbfs:/mnt/landing/" + fileNmB
dbutils.fs.mv(fileLocB, "dbfs:/mnt/archive")

// COMMAND ----------

val fileNmC = dbutils.fs.ls("/mnt/landing").map(_.name).filter(r => r.startsWith("SourceC"))(0)
val fileLocC = "dbfs:/mnt/landing/" + fileNmC
dbutils.fs.mv(fileLocC, "dbfs:/mnt/archive")

// COMMAND ----------



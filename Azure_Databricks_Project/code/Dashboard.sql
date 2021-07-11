-- Databricks notebook source
SELECT * FROM 
(SELECT
E.department_id
,Name
,employee_id
,ROW_NUMBER() OVER(PARTITION BY E.department_id ORDER BY salary DESC )rw
,salary
FROM datawarehousedb.employee E 
LEFT JOIN
datawarehousedb.department d
ON E.department_id = d.Department_id
WHERE E.department_id IS NOT NULL AND d.name IS NOT NULL) WHERE rw < 6

-- COMMAND ----------

SELECT
CASE 

    WHEN country = "Australia" THEN "AUS"  ----- ISO 3166-1 alpha-3 code
    WHEN country = "Brazil" THEN "BRA"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "Canada" THEN "CAN"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "China" THEN "CHN"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Denmark" THEN "DNK"    ----- ISO 3166-1 alpha-3 code
    WHEN country = "Germany" THEN "DEU"    ----- ISO 3166-1 alpha-3 code
    WHEN country = "India" THEN "IND"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Japan" THEN "JPN"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Sweden" THEN "SWE"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "UAE" THEN "ARE"        ----- ISO 3166-1 alpha-3 code
    WHEN country = "USA" THEN "USA"        ----- ISO 3166-1 alpha-3 code
  END AS code
 , SUM(salary)/1000000 AS cost_of_department_in_million
FROM datawarehousedb.employee E 
LEFT JOIN
datawarehousedb.department d
ON E.department_id = d.Department_id
WHERE Name IS NOT NULL
GROUP BY 
code

-- COMMAND ----------

SELECT
CASE 

    WHEN country = "Australia" THEN "AUS"  ----- ISO 3166-1 alpha-3 code
    WHEN country = "Brazil" THEN "BRA"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "Canada" THEN "CAN"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "China" THEN "CHN"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Denmark" THEN "DNK"    ----- ISO 3166-1 alpha-3 code
    WHEN country = "Germany" THEN "DEU"    ----- ISO 3166-1 alpha-3 code
    WHEN country = "India" THEN "IND"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Japan" THEN "JPN"      ----- ISO 3166-1 alpha-3 code
    WHEN country = "Sweden" THEN "SWE"     ----- ISO 3166-1 alpha-3 code
    WHEN country = "UAE" THEN "ARE"        ----- ISO 3166-1 alpha-3 code
    WHEN country = "USA" THEN "USA"        ----- ISO 3166-1 alpha-3 code
  END AS code
 , SUM(salary)/1000000 AS cost_of_department_in_million
FROM datawarehousedb.employee E 
LEFT JOIN
datawarehousedb.department d
ON E.department_id = d.Department_id
WHERE Name IS NOT NULL
GROUP BY 
code

-- COMMAND ----------

SELECT
name, country
 , SUM(salary)/1000000 AS cost_of_department_in_million
FROM datawarehousedb.employee E 
LEFT JOIN
datawarehousedb.department d
ON E.department_id = d.Department_id
WHERE Name IS NOT NULL
GROUP BY 
name, country

-- COMMAND ----------

SELECT D.Name, 
         AVG(salary) AS avg_salary,
         Min(salary) AS min_salary,
         MAX(salary) AS max_salary 
  FROM datawarehousedb.employee E  
  LEFT JOIN datawarehousedb.department D on E.Department_id = D.Department_id WHERE D.Name IS NOT NULL
  GROUP BY D.Name

-- COMMAND ----------



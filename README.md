# **Log Analysis**
***
 The tool **LogAnalysis.py** uses information from a newspaper website database to discover what kind of articles the site's readers like. It provides an informative summary about site's user activity.
 

## **To Run Tool**
---
**LogAnalysis.py** tool can be run from command-line by giving following command
```
python LogAnalysis.py
```

## **Prerequisite**
---
User needs to import schema and data to the news database prior to running the python script.
Following steps need to be followed:
* Download newsdata.sql file from path : https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
* Unzip the folder and copy newsdata.sql file to the directory where python script is loacated.
* Populate the databse with data by giving the command ```psql -d news -f newsdata.sql```

## **Requirements**
---
Following software are required for this script to work
* Python version 2 - Install it from https://www.python.org/downloads/
* PostgreSQL - Install it from https://www.postgresql.org/download/
* psycopg2 - Install it using command ``` pip install psycopg2 ```

## **Code Design**
---
* A connection is established to the database "news".
* Cursor object is obtained.
* Two functions are defined executeQuery and printQueryResults.
	* executeQuery executes given sql query and returns results.
	* printQueryResults prints the results in a proper format.
* Three SQL Queries are executed to obtain follwing information and results are displayed. executeQuery and printQueryResults are used for these.
	* Most popular articles of all time
	* Most popular article authors of all time
	* Days where more than 1% of requests led to errors.
* Database connection is closed.

## Sample Output
---
```
LOG ANALYSIS RESULTS
====================

Top 3 most popular articles of all time
---------------------------------------
1. Candidate is jerk, alleges rival - 338647 views
2. Bears love berries, alleges bear - 253801 views
3. Bad things gone, say good people - 170098 views


Most popular article authors of all time
----------------------------------------
1. Ursula La Multa - 507594 views
2. Rudolf von Treppenwitz - 423457 views
3. Anonymous Contributor - 170098 views
4. Markoff Chaney - 84557 views


Days where more than 1% request led to errors
---------------------------------------------
1. Jul 17, 2016 - 2.26 % errors
```



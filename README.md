# Udacity-Log-Analysis-Project
Solution to the Log Analysis Project in the Full Stack Web Developer Nano Degree.

The objective of this assignment is to gain an understanding of SQL and how to interact with an SQL database using python. The data needed in order to complete this assignment, *i.e.* the **News database**, was provided by Udacity.

**Python 3** has been used for this assignment. The data is stored in a **PostgreSQL** database and the DBAPI used to connect and query this database using python was **psycopg2**. The other package dependency we have is **Flask**, which has been used as a server to display the results in a web-page.

This repo consists of two files:
- The "log_analysis_db.py" file contains all the commands used to retrieve data from the SQL database. 
- The "log_analysis_server.py" file calls functions from the previous file and servers the results into an HTML file. 

Please note that three *Views* have been created in the PostgreSQL database in order to complete this assignment. Here are SQL queries used to create those views: 

*From question 2*
```
CREATE VIEW author_article AS
SELECT au.name, art.slug
FROM authors as au, articles as art
WHERE au.id = art.author;
```
*From question 3*
```
CREATE VIEW all_date AS
SELECT date(log.time), COUNT(*) AS all
FROM log GROUP BY date(log.time);
```
```
CREATE VIEW bad_date AS
SELECT date(log.time), COUNT(*) AS bad
FROM log WHERE log.status LIKE '%404%'
GROUP BY date(log.time);
```
Instructions to run this program:

**NOTE:** These instruction assume that python3, psql, and any other dependencies are already installed. I have run this program in Ubuntu on a Virtual Machine created using **Vagrant**.  

- Step 1: *Set up the **news** database*: 
    - <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip"> Download the data </a>
    - Import the *newsdata.sql* file and use the following command to generate the database: `psql -d news -f newsdata.sql`
   
- Step 2: *Run the python script to serve the data*:
    - `cd` into the folder that contains the two above mentioned python files 
    - Type `python log_analysis_server.py` to run the python server script
    - Open a browser and go to http://localhost:8000 in order to view the output


Here is what the served results page looks like: 

![Results](/screenshot.PNG)


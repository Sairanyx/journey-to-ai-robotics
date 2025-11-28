# HW10 – Connection to Databases with Python

This project connects a Python script to a PostgreSQL database running in Docker.  
Using `psycopg2` and `pandas`, the script:

- Creates three tables: `students`, `courses`, and `grades`
- Reads data from `students.csv`, `courses.csv`, and `grades.csv`
- Inserts the data into PostgreSQL
- Runs SQL queries to:
  - List all students with their courses and grades  
  - Find students who received grade 5  
  - Calculate and display an additional summary (e.g. average grade per course)

## What I learned

- How to run PostgreSQL in Docker and connect to it from Python  
- How to use `psycopg2` to create tables and execute SQL queries  
- How to load CSV data into a database using `pandas`  
- How to debug common database connection issues (ports, users, passwords)

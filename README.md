# Python SQL - Assignment #3

## Task
Python SQL

You are given two files:
- students.json
- rooms.json

Your task is to write a Python script that:
- Loads data from both files
- Using MySQL, create a database schema that corresponds to the given files (many-to-one relationship).
- Insert the data into the database
- Retrieve the following data using SQL queries (all calculations should be done at the database level)
    - List of rooms and the number of students in each.
    - Top 5 rooms with the smallest average student age
    - Top 5 rooms with the largest age difference among students
    - List of rooms where students of different sexes live together
- Suggest optimizations for the queries using indexes

Note: Follow SOLID principles. Do not use ORM (raw SQL must be used).

## Installing dependencies and MySQL database

```bash
uv lock
sudo apt install mysql-server -y
sudo service mysql start
```

## Usage
You just need to set yp mysql service and then config it to be accessible by the script.

Everything else like, initializing the schema, inserting the data, indexing and querying is done by the script.
```bash
python main.py
```

## Explanation
I took the JSON reader from the previous project. Created MySQLConnectionManager class that handles the db connection.
Created the db schema in schema.sql, tasked queries in queries.sql, and indexing queries in indexing.sql.
Then I wrote the MySQL service that basically handels all the db operations through python scipt.

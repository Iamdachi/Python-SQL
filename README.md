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
Create Database schema.
```bash
mysql -u {username} -p < schema.sql
```

Run the script to read files and write into the database:
```bash
mysql -u {username} -p < queries.sql
```

Query the database:
```bash
mysql -u {username} -p < indexing.sql
```
Index the database for optimization:

## Explanation
I took the JSON reader from the previous project. Created the schema in schema.sql,
tasked queries in queries.sql, and indexing queries in indexing.sql. Right now you
can directly run then through mysql.
TODO: run those queries fom python script.
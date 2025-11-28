# HW - Connection to Databases with Python

import psycopg2
import pandas as pd

# Postgresql settings

conn = psycopg2.connect(
    dbname="hwdb",
    user="hwuser",
    password="eddie",
    host="localhost",
    port=5432,
)

cur = conn.cursor()

cur = conn.cursor()

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS grades;")
cur.execute("DROP TABLE IF EXISTS courses;")
cur.execute("DROP TABLE IF EXISTS students;")

# 1. Making tables

cur.execute("""
    CREATE TABLE students (
        student_id   INTEGER PRIMARY KEY,
        name         TEXT,
        age          INTEGER
    );
""")

cur.execute("""
    CREATE TABLE courses (
        course_id    VARCHAR(20) PRIMARY KEY,
        course_name  TEXT,
        credits      INTEGER
    );
""")

cur.execute("""
    CREATE TABLE grades (
        student_id   INTEGER REFERENCES students(student_id),
        course_id    VARCHAR(20) REFERENCES courses(course_id),
        grade        INTEGER,
        PRIMARY KEY (student_id, course_id)
    );
""")

conn.commit()

print("Tables created.\n")


# 2. Inserting the data from the csv files


for _, row in students_df.iterrows():
    cur.execute(
        "INSERT INTO students (student_id, name, age) VALUES (%s, %s, %s);",
        (row["student_id"], row["name"], int(row["age"]))
    )

for _, row in courses_df.iterrows():
    cur.execute(
        "INSERT INTO courses (course_id, course_name, credits) VALUES (%s, %s, %s);",
        (row["course_id"], row["course_name"], int(row["credits"]))
    )

for _, row in grades_df.iterrows():
    cur.execute(
        "INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s);",
        (int(row["student_id"]), row["course_id"], int(row["grade"]))
    )

conn.commit()

print("Data inserted.\n")


# 3. Making the queries

# List all students and their enrolled courses with grades

print("All students and their courses with grades:")

cur.execute("""
    SELECT s.student_id,
           s.name,
           c.course_id,
           c.course_name,
           g.grade
    FROM grades g
    JOIN students s ON g.student_id = s.student_id
    JOIN courses c  ON g.course_id = c.course_id
    ORDER BY s.student_id, c.course_id;
""")

rows = cur.fetchall()

for r in rows:
    print(f"{r[0]} - {r[1]} | {r[2]} - {r[3]} | grade: {r[4]}")
print()

# Find students who received a grade of 5 in any course

print("Students who received grade 5 in any course:")

cur.execute("""
    SELECT DISTINCT s.student_id, s.name
    FROM grades g
    JOIN students s ON g.student_id = s.student_id
    WHERE g.grade = 5
    ORDER BY s.student_id;
""")

rows = cur.fetchall()

for r in rows:
    print(f"{r[0]} - {r[1]}")
print()

# Make ANY OTHER query from database and show the results

print("Average grade per course:")

cur.execute("""
    SELECT c.course_id,
           c.course_name,
           ROUND(AVG(g.grade)::numeric, 2) AS avg_grade
    FROM grades g
    JOIN courses c ON g.course_id = c.course_id
    GROUP BY c.course_id, c.course_name
    ORDER BY c.course_id;
""")

rows = cur.fetchall()

for r in rows:
    print(f"{r[0]} - {r[1]} | average grade: {r[2]}")
print()

cur.close()
conn.close()

print("Done.")

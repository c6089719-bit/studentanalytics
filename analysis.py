import mysql.connector
import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9896844",
    database="student_analytics"
)

print("MySQL connected successfully!")
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9896844",
    database="student_analytics"
)

query = """
SELECT
    s.name,
    s.gender,
    s.department,
    s.year,
    sub.subject_name,
    m.marks
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN subjects sub
    ON m.subject_id = sub.subject_id;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]

df = pd.DataFrame(rows, columns=columns)

print(df.head())
import pandas as pd

query = """
SELECT
    s.name,
    s.gender,
    s.department,
    s.year,
    sub.subject_name,
    m.marks
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN subjects sub
    ON m.subject_id = sub.subject_id;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]

df = pd.DataFrame(rows, columns=columns)

print(df.head())
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())
subject_average = df.groupby("subject_name")["marks"].mean()

print("\nSubject-wise Average Marks:")
print(subject_average)
student_average = (
    df.groupby("name")["marks"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nStudent-wise Average Marks:")
print(student_average)
top_3_students = student_average.head(3)

print("\nTop 3 Students:")
print(top_3_students)
print("\nOverall Statistics:")

print("Average Marks:", round(df["marks"].mean(), 2))
print("Highest Marks:", df["marks"].max())
print("Lowest Marks:", df["marks"].min())
print("Total Marks:", df["marks"].sum())
df["result"] = np.where(df["marks"] >= 50, "Pass", "Fail")

print("\nPass/Fail Count:")
print(df["result"].value_counts())
pass_percentage = (
    (df["result"] == "Pass").mean() * 100
)

print("\nPass Percentage:", round(pass_percentage, 2), "%")
subject_avg = df.groupby("subject_name")["marks"].mean()

plt.figure(figsize=(8, 5))
subject_avg.plot(kind="bar")

plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()
student_avg = (
    df.groupby("name")["marks"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
student_avg.plot(kind="bar")

plt.title("Student-wise Average Marks")
plt.xlabel("Student")
plt.ylabel("Average Marks")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
top_3 = (
    df.groupby("name")["marks"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
    .head(3)
)

print("\n🏆 Top 3 Students:")
print(top_3)
total_students = df["name"].nunique()
average_marks = round(df["marks"].mean(), 2)
highest_score = df["marks"].max()
pass_rate = round((df["result"] == "Pass").mean() * 100, 2)

print("\n📊 Dashboard KPI:")
print("Total Students:", total_students)
print("Average Marks:", average_marks)
print("Highest Score:", highest_score)
print("Pass Rate:", pass_rate, "%")
from flask import Flask, render_template
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)


@app.route("/")
def home():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password= os.getenv("MYSQL_password"),
        database="student_analytics"
    )

    cursor = conn.cursor()

    # 1. Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # 2. Average Marks
    cursor.execute("SELECT AVG(marks) FROM marks")
    average_marks = round(cursor.fetchone()[0], 2)

    # 3. Highest Score
    cursor.execute("SELECT MAX(marks) FROM marks")
    highest_score = cursor.fetchone()[0]

    # 4. Pass Rate
    cursor.execute("""
        SELECT
        (SUM(CASE WHEN marks >= 50 THEN 1 ELSE 0 END) / COUNT(*)) * 100
        FROM marks
    """)
    pass_rate = round(cursor.fetchone()[0], 2)

    # 5. Subject-wise Average
    cursor.execute("""
        SELECT sub.subject_name, AVG(m.marks)
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        GROUP BY sub.subject_name
    """)
    subject_data = cursor.fetchall()

    # 6. Top 3 Students
    cursor.execute("""
        SELECT s.name, AVG(m.marks)
        FROM students s
        JOIN marks m
        ON s.student_id = m.student_id
        GROUP BY s.student_id, s.name
        ORDER BY AVG(m.marks) DESC
        LIMIT 3
    """)
    top_students = cursor.fetchall()

    # 7. Student-wise Average Marks
    cursor.execute("""
        SELECT s.name, AVG(m.marks)
        FROM students s
        JOIN marks m
        ON s.student_id = m.student_id
        GROUP BY s.student_id, s.name
        ORDER BY AVG(m.marks) DESC
    """)
    student_data = cursor.fetchall()

    # 8. Marks Distribution
    cursor.execute("""
        SELECT
            CASE
                WHEN marks < 60 THEN '50-59'
                WHEN marks < 70 THEN '60-69'
                WHEN marks < 80 THEN '70-79'
                WHEN marks < 90 THEN '80-89'
                ELSE '90-100'
            END AS mark_range,
            COUNT(*)
        FROM marks
        GROUP BY mark_range
        ORDER BY mark_range
    """)
    marks_distribution = cursor.fetchall()

    # 9. Pass / Fail
    cursor.execute("""
        SELECT
            CASE
                WHEN marks >= 50 THEN 'Pass'
                ELSE 'Fail'
            END AS result,
            COUNT(*) AS total
        FROM marks
        GROUP BY result
    """)
    pass_fail_data = cursor.fetchall()

    # 10. Subject Highest / Lowest
    cursor.execute("""
        SELECT
            sub.subject_name,
            MAX(m.marks) AS highest_marks,
            MIN(m.marks) AS lowest_marks
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        GROUP BY sub.subject_name
    """)
    subject_high_low = cursor.fetchall()

    # 11. Top 5 Students
    cursor.execute("""
        SELECT
            s.name,
            s.department,
            AVG(m.marks) AS avg_marks
        FROM students s
        JOIN marks m
        ON s.student_id = m.student_id
        GROUP BY s.student_id, s.name, s.department
        ORDER BY avg_marks DESC
        LIMIT 5
    """)
    top_5_students = cursor.fetchall()

    # Close database
    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        average_marks=average_marks,
        highest_score=highest_score,
        pass_rate=pass_rate,
        subject_data=subject_data,
        top_students=top_students,
        student_data=student_data,
        marks_distribution=marks_distribution,
        pass_fail_data=pass_fail_data,
        subject_high_low=subject_high_low,
        top_5_students=top_5_students
    )


if __name__ == "__main__":
    app.run(debug=True)
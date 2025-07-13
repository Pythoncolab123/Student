pip install mysql-connector-python
import mysql.connector
UG=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
                             user="31CJB1UZRWYNAok.root",
                             password='EXpTVqVAmtIV7SY8',
                             port=4000)
Udhay=UG.cursor()
Udhay.execute("show databases")
pip install Faker
from faker import Faker
import mysql.connector
import re

fake = Faker()

# Connect to TiDB Cloud
UG = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)

Udhay = UG.cursor()

# Loop to insert 500 students, one by one
for i in range(500):
    student_id = i + 1  # Skip this if student_id is auto-increment in DB
    name = fake.name().replace("'", "''")
    age = fake.random_int(min=18, max=25)
    gender = fake.random_element(elements=('Male', 'Female', 'Other'))
    email = fake.email().replace("'", "''")

    # Clean phone number to avoid "Data too long" errors
    phone_raw = fake.phone_number()
    phone = re.sub(r'\D', '', phone_raw)[:15]

    enrollment_year = fake.random_int(min=2018, max=2024)
    course_batch = fake.bothify(text='Batch-##')
    city = fake.city().replace("'", "''")
    graduation_year = enrollment_year + 4

    SQL = f"""
    INSERT INTO Students 
    (student_id, name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
    VALUES 
    ({student_id}, '{name}', {age}, '{gender}', '{email}', '{phone}', {enrollment_year}, '{course_batch}', '{city}', {graduation_year});
    """

    try:
        Udhay.execute(SQL)
        UG.commit()  # commit each row immediately
        print(f"[{i+1}/500] Inserted: {name}")
    except Exception as e:
        print(f"[{i+1}/500] ❌ Error inserting {name}: {e}")
        UG.rollback()  # rollback only this query

# Close connection
Udhay.close()
UG.close()
from faker import Faker
import mysql.connector
import random

fake = Faker()

# Connect to TiDB Cloud
UG = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)

Udhay = UG.cursor()

# Insert 500 rows into Programming table
for i in range(500):
    programming_id = i + 1  # if it's not auto-increment
    student_id = i + 1      # assuming 1-to-1 mapping with Students table
    language = fake.random_element(elements=["Python", "Java", "C++", "JavaScript", "SQL", "Go", "Ruby"])
    problems_solved = random.randint(10, 500)
    assessments_completed = random.randint(0, 10)
    mini_projects = random.randint(0, 5)
    certifications_earned = random.randint(0, 3)
    latest_project_score = round(random.uniform(40, 100), 2)

    SQL = f"""
    INSERT INTO Programming 
    (programming_id, student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
    VALUES 
    ({programming_id}, {student_id}, '{language}', {problems_solved}, {assessments_completed}, {mini_projects}, {certifications_earned}, {latest_project_score});
    """

    try:
        Udhay.execute(SQL)
        UG.commit()
        print(f"[{i+1}/500] Inserted Programming data for student_id={student_id}")
    except Exception as e:
        print(f"[{i+1}/500] ❌ Error inserting for student_id={student_id}: {e}")
        UG.rollback()

# Close connection
Udhay.close()
UG.close()
from faker import Faker
import mysql.connector
import random

fake = Faker()

# Connect to TiDB Cloud
UG = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)

Udhay = UG.cursor()

# Insert 500 rows into SoftSkills table
for i in range(500):
    soft_skill_id = i + 1
    student_id = i + 1  # must match the same student_id in Students table

    communication = random.randint(40, 100)
    teamwork = random.randint(40, 100)
    presentation = random.randint(40, 100)
    leadership = random.randint(40, 100)
    critical_thinking = random.randint(40, 100)
    interpersonal_skills = random.randint(40, 100)

    SQL = f"""
    INSERT INTO SoftSkills 
    (soft_skill_id, student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
    VALUES 
    ({soft_skill_id}, {student_id}, {communication}, {teamwork}, {presentation}, {leadership}, {critical_thinking}, {interpersonal_skills});
    """

    try:
        Udhay.execute(SQL)
        UG.commit()
        print(f"[{i+1}/500] Inserted SoftSkills for student_id={student_id}")
    except Exception as e:
        print(f"[{i+1}/500] ❌ Error inserting for student_id={student_id}: {e}")
        UG.rollback()

# Close connection
Udhay.close()
UG.close()
from faker import Faker
import mysql.connector
import random

fake = Faker()

# Connect to TiDB Cloud
UG = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)

Udhay = UG.cursor()

# Insert 500 rows into Placements table
for i in range(500):
    placement_id = i + 1
    student_id = i + 1  # Match to existing student_id

    mock_interview_score = random.randint(40, 100)
    internships_completed = random.randint(0, 3)
    placement_status = random.choice(['Ready', 'Not Ready', 'Placed'])

    # Only assign a company if placed
    company_name = fake.company().replace("'", "''") if placement_status == 'Placed' else 'NULL'

    if company_name == 'NULL':
        company_field = 'NULL'
    else:
        company_field = f"'{company_name}'"

    SQL = f"""
    INSERT INTO Placements 
    (placement_id, student_id, mock_interview_score, internships_completed, placement_status, company_name)
    VALUES 
    ({placement_id}, {student_id}, {mock_interview_score}, {internships_completed}, '{placement_status}', {company_field});
    """

    try:
        Udhay.execute(SQL)
        UG.commit()
        print(f"[{i+1}/500] Inserted Placement record for student_id={student_id}")
    except Exception as e:
        print(f"[{i+1}/500] ❌ Error inserting for student_id={student_id}: {e}")
        UG.rollback()

# Close connection
Udhay.close()
UG.close()
pip install streamlit
pip install pandas
pip install streamlit pyngrok
pip install streamlit mysql-connector-python pandas
import streamlit as st
import pandas as pd
import mysql.connector

# --- DB Config ---
db = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="31CJB1UZRWYNAok.root",
    password="EXpTVqVAmtIV7SY8",
    port=4000,
    database="UG"
)
cursor = db.cursor(dictionary=True)

# --- Query helper ---
def run_query(query):
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall())

# --- Sidebar filters ---
st.sidebar.title("🎛 Filters")
batch = st.sidebar.text_input("Batch (e.g. Batch-21)")
city = st.sidebar.text_input("City")

# --- Header ---
st.title("🎓 Student Placement Dashboard")

# --- Students ---
student_query = "SELECT * FROM Students"
if batch:
    student_query += f" WHERE course_batch = '{batch}'"
elif city:
    student_query += f" WHERE city = '{city}'"

students_df = run_query(student_query)
st.subheader("👥 Students")
st.dataframe(students_df)

# --- Programming Data ---
st.subheader("💻 Programming Stats")
prog_df = run_query("""
    SELECT s.student_id, s.name, p.language, p.problems_solved, p.latest_project_score
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
""")
st.dataframe(prog_df)

# --- Soft Skills ---
st.subheader("🧠 Soft Skills")
skills_df = run_query("""
    SELECT s.student_id, s.name, ss.communication, ss.teamwork, ss.leadership
    FROM Students s
    JOIN SoftSkills ss ON s.student_id = ss.student_id
""")
st.dataframe(skills_df)

# --- Placements ---
st.subheader("🏢 Placement Status")
placement_df = run_query("""
    SELECT s.student_id, s.name, p.placement_status, p.company_name
    FROM Students s
    JOIN Placements p ON s.student_id = p.student_id
""")
st.dataframe(placement_df)

# --- Clean up ---
cursor.close()
db.close()

# streamlit_app.py
import streamlit as st
import pandas as pd
import mysql.connector

# --- Database Connection ---
def get_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="31CJB1UZRWYNAok.root",
        password="EXpTVqVAmtIV7SY8",
        port=4000,
        database="UG"
    )

# --- Query Execution Helper ---
def run_query(query):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    results = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close()
    return results

# --- Streamlit UI ---
st.set_page_config(page_title="UG Placement Dashboard", layout="wide")
st.title("🎓 UG Student Placement Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Students")
batch = st.sidebar.text_input("Batch (e.g. Batch-21)")
city = st.sidebar.text_input("City")

# --- Students Table ---
students_query = "SELECT * FROM Students"
if batch:
    students_query += f" WHERE course_batch = '{batch}'"
elif city:
    students_query += f" WHERE city = '{city}'"

students_df = run_query(students_query)
st.subheader("👥 Student Info")
st.dataframe(students_df, use_container_width=True)

# --- Programming Table ---
st.subheader("💻 Programming Performance")
prog_df = run_query("""
    SELECT s.student_id, s.name, p.language, p.problems_solved, 
           p.assessments_completed, p.mini_projects, 
           p.certifications_earned, p.latest_project_score
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
""")
st.dataframe(prog_df, use_container_width=True)

# --- Soft Skills Table ---
st.subheader("🧠 Soft Skills Scores")
skills_df = run_query("""
    SELECT s.student_id, s.name, ss.communication, ss.teamwork, 
           ss.presentation, ss.leadership, ss.critical_thinking, ss.interpersonal_skills
    FROM Students s
    JOIN SoftSkills ss ON s.student_id = ss.student_id
""")
st.dataframe(skills_df, use_container_width=True)

# --- Placement Table ---
st.subheader("🏢 Placement Status")
placement_df = run_query("""
    SELECT s.student_id, s.name, p.mock_interview_score, 
           p.internships_completed, p.placement_status, p.company_name
    FROM Students s
    JOIN Placements p ON s.student_id = p.student_id
""")
st.dataframe(placement_df, use_container_width=True)

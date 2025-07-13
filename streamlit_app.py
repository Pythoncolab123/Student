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

# --- SQL Query Runner ---
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(data)

# --- Streamlit App Config ---
st.set_page_config(page_title="UG Student Placement Dashboard", layout="wide")
st.title("🎓 UG Student Placement Dashboard")

# --- Filters ---
st.sidebar.header("🔍 Filters")
batch = st.sidebar.text_input("Batch (e.g. Batch-21)")
city = st.sidebar.text_input("City")
language = st.sidebar.text_input("Programming Language")
placement_status = st.sidebar.text_input("Placement Status")
search_name = st.sidebar.text_input("Search by Name")
search_email = st.sidebar.text_input("Search by Email")

# --- Student Info ---
student_query = "SELECT * FROM Students"
conditions = []

if batch:
    conditions.append(f"course_batch = '{batch}'")
if city:
    conditions.append(f"city = '{city}'")
if search_name:
    conditions.append(f"name LIKE '%{search_name}%'")
if search_email:
    conditions.append(f"email LIKE '%{search_email}%'")

if conditions:
    student_query += " WHERE " + " AND ".join(conditions)

students_df = run_query(student_query)
st.subheader("👥 Students")
st.dataframe(students_df, use_container_width=True)

# --- Programming Info ---
prog_query = """
    SELECT s.student_id, s.name, p.language, p.problems_solved,
           p.assessments_completed, p.mini_projects,
           p.certifications_earned, p.latest_project_score
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
"""
if language:
    prog_query += f" WHERE p.language = '{language}'"

prog_df = run_query(prog_query)
st.subheader("💻 Programming Performance")
st.dataframe(prog_df, use_container_width=True)

# --- Soft Skills Info ---
skills_df = run_query("""
    SELECT s.student_id, s.name, ss.communication, ss.teamwork,
           ss.presentation, ss.leadership, ss.critical_thinking, ss.interpersonal_skills
    FROM Students s
    JOIN SoftSkills ss ON s.student_id = ss.student_id
""")
st.subheader("🧠 Soft Skills")
st.dataframe(skills_df, use_container_width=True)

# --- Placement Info ---
placement_query = """
    SELECT s.student_id, s.name, p.mock_interview_score,
           p.internships_completed, p.placement_status, p.company_name
    FROM Students s
    JOIN Placements p ON s.student_id = p.student_id
"""
if placement_status:
    placement_query += f" WHERE p.placement_status = '{placement_status}'"

placement_df = run_query(placement_query)
st.subheader("🏢 Placement Overview")
st.dataframe(placement_df, use_container_width=True)

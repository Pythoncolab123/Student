import streamlit as st
import pandas as pd
import mysql.connector
import os

# --- DB Config ---
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=int(os.getenv("DB_PORT", 4000)),
        database=os.getenv("DB_NAME")
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    st.error(f"❌ Database connection failed: {err}")
    st.stop()

# --- Query helper ---
def run_query(query):
    try:
        cursor.execute(query)
        return pd.DataFrame(cursor.fetchall())
    except mysql.connector.Error as err:
        st.error(f"❌ Query failed: {err}")
        return pd.DataFrame()

# --- Sidebar filters ---
st.sidebar.title("🎛 Filters")
batch = st.sidebar.text_input("Batch (e.g. Batch-21)")
city = st.sidebar.text_input("City")

# --- Header ---
st.title("🎓 Student Placement Dashboard")

# --- Students ---
student_query = "SELECT * FROM Students"
filters = []
if batch:
    filters.append(f"course_batch = '{batch}'")
if city:
    filters.append(f"city = '{city}'")
if filters:
    student_query += " WHERE " + " AND ".join(filters)

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

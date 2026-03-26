import streamlit as st
import PyPDF2
import pandas as pd

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

skills_db = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "machine learning",
    "data science",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "excel",
    "power bi",
    "communication",
    "teamwork"
]

job_roles = {
    "Data Scientist": ["python", "machine learning", "data science", "sql"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Software Engineer": ["java", "c++", "python", "sql"]
}

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    st.subheader("Extracted Resume Text:")
    st.write(text)

    detected_skills = []

    text_lower = text.lower()

    for skill in skills_db:
        if skill in text_lower:
            detected_skills.append(skill)

    st.subheader("Detected Skills:")

    if detected_skills:
        for skill in detected_skills:
            st.success(skill)
    else:
        st.warning("No skills detected")

    # Resume Score
    score = len(detected_skills) * 5
    if score > 100:
        score = 100

    st.subheader("Resume Score:")
    st.progress(score)
    st.write(score, "/ 100")

    # Job Role Matching
    st.subheader("Job Role Matching")

    selected_role = st.selectbox(
        "Select a Job Role",
        list(job_roles.keys())
    )

    required_skills = job_roles[selected_role]

    matched = []

    for skill in required_skills:
        if skill in text_lower:
            matched.append(1)
        else:
            matched.append(0)

    match_score = int((sum(matched) / len(required_skills)) * 100)

    st.write("Match Score:", match_score, "%")

    # GRAPH VISUALIZATION PART
    st.subheader("Skill Match Visualization")

    skill_chart = pd.DataFrame({
        "Skills": required_skills,
        "Match (1 = Yes, 0 = No)": matched
    })

    st.bar_chart(skill_chart.set_index("Skills"))
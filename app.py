import streamlit as st
import PyPDF2
import pandas as pd
import requests
from openai import OpenAI
import json

# ================= OPENAI CONFIG =================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_interview_questions(job_role, skills):
    """
    Generate categorized AI interview questions for a job role based on candidate skills.
    Returns a dictionary with keys: Technical, Behavioral, Scenario.
    """
    prompt = f"""
    Generate 12 interview questions for a {job_role} role based on the following skills:
    {skills}

    Please categorize them into:
    1. Technical
    2. Behavioral
    3. Scenario-based

    Return the output in JSON format like this:
    {{
        "Technical": ["question1", "question2", ...],
        "Behavioral": ["question1", ...],
        "Scenario": ["question1", ...]
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        questions_json = json.loads(response.choices[0].message.content)
    except:
        # Fallback if AI returns plain text
        questions_json = {"Technical": [], "Behavioral": [], "Scenario": []}
    
    return questions_json

# ================= API CONFIG =================
APP_ID = st.secrets["APP_ID"]
APP_KEY = st.secrets["APP_KEY"]

# ================= JOB FETCH FUNCTION =================
def fetch_jobs(role):
    try:
        search_role = role + " developer"
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&what={search_role}&results_per_page=10"
        response = requests.get(url)
        return response.json()
    except:
        return {}

# ================= STREAMLIT TITLE =================
st.title("AI Resume Analyzer")

# ================= FILE UPLOADER =================
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# ================= SKILLS DATABASE =================
skills_db = [
    "python","java","c","c++","sql","machine learning","data science",
    "html","css","javascript","react","node.js",
    "excel","power bi","communication","teamwork",
    "deep learning","nlp","tensorflow","pandas","numpy",
    "aws","azure","docker","kubernetes",
    "photoshop","illustrator","autocad",
    "tally","accounting","marketing","sales",
    "cybersecurity","networking"
]

# ================= JOB ROLE MATCHING =================
job_roles = {
    "Data Scientist": ["python","machine learning","data science","sql"],
    "Web Developer": ["html","css","javascript","react"],
    "Software Engineer": ["java","c++","python","sql"]
}

# ================= MAIN EXECUTION BLOCK =================
if uploaded_file is not None:
    # -------- EXTRACT PDF TEXT --------
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()

    st.subheader("Extracted Resume Text:")
    st.write(text)

    # -------- SKILL DETECTION --------
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

    # -------- CAREER FIELD DETECTION --------
    career_field = "General"
    if any(skill in detected_skills for skill in ["python","machine learning","data science"]):
        career_field = "Data Science"
    elif any(skill in detected_skills for skill in ["java","c++","c","sql"]):
        career_field = "Software Engineering"
    elif any(skill in detected_skills for skill in ["html","css","javascript","react"]):
        career_field = "Web Development"
    elif "autocad" in detected_skills:
        career_field = "Mechanical Engineering"
    elif any(skill in detected_skills for skill in ["tally","accounting"]):
        career_field = "Accounting"
    elif any(skill in detected_skills for skill in ["photoshop","illustrator"]):
        career_field = "Graphic Design"
    elif any(skill in detected_skills for skill in ["marketing","sales"]):
        career_field = "Business & Marketing"

    st.subheader("Detected Career Field:")
    st.success(career_field)

    # -------- LIVE JOB SEARCH --------
    st.subheader("Live Job Openings For You")
    job_data = fetch_jobs(career_field)
    if "results" in job_data and len(job_data["results"]) > 0:
        for job in job_data["results"]:
            st.markdown(f"### {job['title']}")
            st.write("Company:", job["company"]["display_name"])
            st.write("Location:", job["location"]["display_name"])
            st.write("Apply here:", job["redirect_url"])
    else:
        st.warning("No jobs found from API")

    # -------- AI-POWERED CATEGORIZED INTERVIEW QUESTIONS --------
    st.subheader("AI Interview Practice Questions")
    try:
        if career_field != "General" and detected_skills:
            with st.spinner("Generating AI-based interview questions..."):
                ai_questions = generate_interview_questions(career_field, ", ".join(detected_skills))

            for category in ["Technical", "Behavioral", "Scenario"]:
                st.markdown(f"**{category} Questions:**")
                if ai_questions.get(category):
                    for q in ai_questions[category]:
                        st.write("•", q)
                else:
                    st.write("No questions generated in this category.")
        else:
            st.info("Not enough information to generate AI interview questions. Detected skills: " + ", ".join(detected_skills))
    except Exception as e:
        st.error(f"Failed to generate AI interview questions: {e}")

    # -------- RESUME SCORE --------
    score = min(len(detected_skills) * 5, 100)
    st.subheader("Resume Score:")
    st.progress(score)
    st.write(score, "/ 100")

    # -------- CAREER READINESS --------
    if score >= 80:
        st.success("Career Readiness Level: HIGH")
    elif score >= 50:
        st.warning("Career Readiness Level: MEDIUM")
    else:
        st.error("Career Readiness Level: LOW – Improve skills using suggested courses")

    # -------- COURSE SUGGESTIONS --------
    if score < 60:
        st.subheader("Recommended Courses")
        course_suggestions = {
            "python": "Python Programming – Coursera",
            "machine learning": "Machine Learning – Andrew Ng",
            "sql": "SQL for Data Analysis – Coursera",
            "html": "Frontend Development – Udemy",
            "javascript": "JavaScript Bootcamp – Udemy",
            "communication": "Professional Communication Skills"
        }
        for skill in course_suggestions:
            if skill not in detected_skills:
                st.write("•", course_suggestions[skill])

    # -------- JOB ROLE MATCHING --------
    st.subheader("Job Role Matching")
    selected_role = st.selectbox("Select a Job Role", list(job_roles.keys()))
    required_skills = job_roles[selected_role]

    matched = []
    for skill in required_skills:
        if skill in text_lower:
            matched.append(1)
        else:
            matched.append(0)

    match_score = int((sum(matched) / len(required_skills)) * 100)
    st.write("Match Score:", match_score, "%")

    # -------- GRAPH VISUALIZATION --------
    st.subheader("Skill Match Visualization")
    skill_chart = pd.DataFrame({
        "Skills": required_skills,
        "Match": matched
    })
    st.bar_chart(skill_chart.set_index("Skills"))

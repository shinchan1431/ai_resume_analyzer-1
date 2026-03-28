import streamlit as st
import PyPDF2
import pandas as pd
import requests
APP_ID = "af561ba6"
APP_KEY = "9499bc677cd60eb3d0644ebaa115e9ad"
def fetch_jobs(role):

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&what={role}&results_per_page=10"

    response = requests.get(url)

    return response.json()

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

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

    # Career Field Detection
    career_field = "General"

    if any(skill in detected_skills for skill in ["python","machine learning","data science"]):
        career_field = "Data Science"

    elif any(skill in detected_skills for skill in ["html","css","javascript","react"]):
        career_field = "Web Development"

    elif any(skill in detected_skills for skill in ["java","c++","sql"]):
        career_field = "Software Engineering"

    elif any(skill in detected_skills for skill in ["autocad"]):
        career_field = "Mechanical Engineering"

    elif any(skill in detected_skills for skill in ["tally","accounting"]):
        career_field = "Accounting"

    elif any(skill in detected_skills for skill in ["photoshop","illustrator"]):
        career_field = "Graphic Design"

    elif any(skill in detected_skills for skill in ["marketing","sales"]):
        career_field = "Business & Marketing"


    st.subheader("Detected Career Field:")
    st.success(career_field)


    # Job Suggestions
    st.subheader("Live Job Openings For You")

job_data = fetch_jobs(career_field)

if "results" in job_data:

    for job in job_data["results"]:

        st.markdown(f"### {job['title']}")
        st.write("Company:", job["company"]["display_name"])
        st.write("Location:", job["location"]["display_name"])
        st.write("Apply here:", job["redirect_url"])

else:

    st.write("No jobs found")

    job_suggestions = {

        "Data Science": [
            "Data Analyst",
            "Machine Learning Engineer",
            "AI Engineer",
            "Business Intelligence Analyst"
        ],

        "Web Development": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer"
        ],

        "Software Engineering": [
            "Software Engineer",
            "Python Developer",
            "System Engineer"
        ]
    }

    if career_field in job_suggestions:
        for job in job_suggestions[career_field]:
            st.write("•", job)


    # Interview Questions
    st.subheader("AI Interview Practice Questions")

    interview_questions = {

        "Data Science": [
            "Explain supervised vs unsupervised learning",
            "What is overfitting?",
            "Explain regression models"
        ],

        "Web Development": [
            "Difference between HTML and HTML5",
            "Explain CSS Flexbox",
            "What is React?"
        ],

        "Software Engineering": [
            "Explain OOP concepts",
            "Difference between list and tuple",
            "What is API?"
        ]
    }

    if career_field in interview_questions:
        for question in interview_questions[career_field]:
            st.write("•", question)


    # Resume Score
    score = len(detected_skills) * 5
    if score > 100:
        score = 100

    st.subheader("Resume Score:")
    st.progress(score)
    st.write(score, "/ 100")


    # Career Readiness Badge
    if score >= 80:
        st.success("Career Readiness Level: HIGH")

    elif score >= 50:
        st.warning("Career Readiness Level: MEDIUM")

    else:
        st.error("Career Readiness Level: LOW – Improve skills using suggested courses")


    # Course Suggestions
    if score < 60:

        st.subheader("Recommended Courses to Improve Your Profile")

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


    # Graph Visualization
    st.subheader("Skill Match Visualization")

    skill_chart = pd.DataFrame({
        "Skills": required_skills,
        "Match (1 = Yes, 0 = No)": matched
    })

    st.bar_chart(skill_chart.set_index("Skills"))
   

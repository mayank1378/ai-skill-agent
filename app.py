import streamlit as st
import pdfplumber
import docx
from core import (
    extract_and_rank_skills,
    extract_resume_skills,
    get_resources,
    generate_mcqs,
    evaluate_mcqs
)

st.set_page_config(page_title="AI Skill Agent", layout="wide")

st.title(" AI Skill Assessment System")

# ---------- File Upload ----------
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"])


# ---------- Extract Text ----------
def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])


# ---------- Main Flow ----------
if st.button("Analyze"):

    if resume_file and jd_file:

        resume_text = extract_text(resume_file)
        jd_text = extract_text(jd_file)

        st.subheader("🔍 Extracting Skills...")

        jd_data = extract_and_rank_skills(jd_text)
        resume_skills = extract_resume_skills(resume_text)

        jd_skills = jd_data.get("all_skills", [])
        top_skills = jd_data.get("top_skills", [])

        missing = list(set(jd_skills) - set(resume_skills))
        top_missing = missing[:3]

        st.subheader("⭐ Top Skills Required")
        st.write(top_skills)

        st.subheader("❌ Top Missing Skills")
        st.write(top_missing)

        # ---------- Resources ----------
        st.subheader("📚 Learning Resources")
        for skill in top_missing:
            res = get_resources(skill)
            st.write(f"### {skill}")
            st.write(res)

        # ---------- MCQ ----------
        st.subheader("🧠 Skill Assessment Test")

        mcqs = generate_mcqs(top_skills)

        st.session_state["mcqs"] = mcqs

# ---------- MCQ Answer Section ----------
if "mcqs" in st.session_state:

    answers = []

    for i, q in enumerate(st.session_state["mcqs"]):
        st.write(f"Q{i+1}: {q.get('question', '')}")

        options = q.get("options", [])

        # Handle both dict and list formats
        if isinstance(options, dict):
            option_keys = list(options.keys())
            option_values = list(options.values())
        else:
            option_values = options
            option_keys = [chr(65 + j) for j in range(len(options))]

        selected = st.radio(
            "Choose:",
            option_values,
            key=f"q_{i}"
        )

        # Map selected value → option key (A/B/C/D)
        selected_key = None
        for k, v in zip(option_keys, option_values):
            if v == selected:
                selected_key = k

        answers.append(selected_key)

    if st.button("Submit Test"):

        # Only score internally, do NOT show correct answers
        score = evaluate_mcqs(st.session_state["mcqs"], answers)

        st.subheader("📊 Result")
        st.success(f"Score: {score}/10")

        if score >= 8:
            st.success("Level: Strong 💪")
        elif score >= 5:
            st.warning("Level: Moderate ⚡")
        else:
            st.error("Level: Needs Improvement 📉")

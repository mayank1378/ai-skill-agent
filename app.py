import streamlit as st
import pdfplumber
import docx
from core import *

st.set_page_config(page_title="AI Skill Agent", layout="wide")

st.title("🤖 AI Skill Assessment System")

# ---------- Upload ----------
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"])

# ---------- Extract ----------
def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    else:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

# ---------- Analyze ----------
if st.button("Analyze"):

    if resume_file and jd_file:

        resume_text = extract_text(resume_file)
        jd_text = extract_text(jd_file)

        jd_data = extract_and_rank_skills(jd_text)
        resume_skills = extract_resume_skills(resume_text)

        jd_skills = jd_data.get("all_skills", [])
        top_skills = jd_data.get("top_skills", [])

        missing = list(set(jd_skills) - set(resume_skills))[:3]

        st.subheader("⭐ Top Skills Required")
        for i, s in enumerate(top_skills, 1):
            st.write(f"{i}. {s}")

        st.subheader("❌ Top Missing Skills")
        for i, s in enumerate(missing, 1):
            st.write(f"{i}. {s}")

        st.subheader("📚 Learning Resources")
        for s in missing:
            st.write(f"### {s}")
            st.write(get_resources(s))

        st.subheader("🧠 Skill Test")
        mcqs = generate_mcqs(top_skills + missing)

        st.session_state["mcqs"] = mcqs

# ---------- MCQ ----------
if "mcqs" in st.session_state:

    st.info("Answer all questions. Correct answers will NOT be shown.")

    answers = []

    for i, q in enumerate(st.session_state["mcqs"]):
        st.write(f"Q{i+1}: {q['question']}")

        options = q["options"]
        values = list(options.values())
        keys = list(options.keys())

        selected = st.radio("Choose:", values, key=i)

        selected_key = None
        for k, v in zip(keys, values):
            if v == selected:
                selected_key = k

        answers.append(selected_key)

    if st.button("Submit Test"):

        score = evaluate_mcqs(st.session_state["mcqs"], answers)

        st.subheader("📊 Result")
        st.success(f"Score: {score}/10")

        if score >= 8:
            st.success("Level: You are a very good fit for the job ")
        elif score >= 5:
            st.warning("Level: You need a litle bit improvement")
        else:
            st.error("Level: Go through the suggestions and prepare properly")

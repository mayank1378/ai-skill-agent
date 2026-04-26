import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------- API SETUP ----------
key = os.getenv("GROQ_API_KEY")
print("DEBUG KEY:", key)

if not key:
    raise ValueError("API key not found. Check your .env file.")

client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1"
)

# ---------- CHAT FUNCTION (FIXED) ----------
def _chat(prompt):
    models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "llama3-8b-8192"
    ]

    for m in models:
        try:
            res = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"Model {m} failed:", e)

    return "{}"

# ---------- JSON CLEANER ----------
def _clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except:
        # Try extracting JSON inside text
        match = re.search(r"\{.*\}|\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return {}

# ---------- Skill Extraction + Ranking ----------
def extract_and_rank_skills(jd_text):
    prompt = f"""
    Extract all skills and top 5 important skills from this job description.

    Return JSON:
    {{
      "all_skills": [],
      "top_skills": []
    }}

    JD:
    {jd_text}
    """
    return _clean_json(_chat(prompt))


def extract_resume_skills(resume_text):
    prompt = f"""
    Extract all skills from this resume.

    Return JSON list.
    """
    return _clean_json(_chat(prompt))


# ---------- Learning Resources ----------
def get_resources(skill):
    prompt = f"""
    Suggest best resources to learn {skill}.

    Return JSON:
    {{
      "youtube": "",
      "docs": "",
      "practice": ""
    }}
    """
    return _clean_json(_chat(prompt))


# ---------- MCQ Generator ----------
def generate_mcqs(skills):
    prompt = f"""
    Generate 10 MCQs based on these skills: {skills}

    Each question must have:
    - question
    - options (A,B,C,D)
    - answer (correct option)

    Return JSON list.
    """
    return _clean_json(_chat(prompt))


# ---------- Evaluation ----------
def evaluate_mcqs(questions, user_answers):
    score = 0

    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            score += 1

    return score
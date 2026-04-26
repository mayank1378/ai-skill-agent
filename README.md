# AI Skill Assessment System

## What this project does

This is a simple web app that helps you understand how well your skills match a job.

You upload your **resume** and a **job description**, and the app:

* extracts skills from both
* shows what skills are important for the job
* highlights what you're missing
* suggests how to learn those skills
* tests you with a short MCQ quiz

The goal is to go beyond just reading a resume and actually **check your understanding**.

---

## How it works

1. Upload your resume (PDF or DOCX)
2. Upload a job description
3. Click **Analyze**

After that, you’ll see:

* top skills required for the job
* skills you’re missing
* learning resources for those missing skills

Then you can take a **10-question MCQ test** based on those skills.

Finally, you get a score and a rough idea of your level.

---

## Features

* Upload resume and JD (PDF / DOCX)
* Skill extraction using AI
* Top skills ranking
* Missing skills detection
* Learning resource suggestions
* MCQ-based assessment (no answers shown)
* Simple scoring system

---

## Tech used

* Python
* Streamlit (for UI)
* Groq API (for AI)
* pdfplumber (PDF parsing)
* python-docx (DOCX parsing)
* python-dotenv

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it (Windows)

```bash
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install streamlit openai pdfplumber python-docx python-dotenv
```

---

## API Key

Create a `.env` file in the project folder and add:

```bash
GROQ_API_KEY=your_api_key_here
```

---

## Run the app

```bash
streamlit run app.py
```

---

## Notes

* Make sure your API key is valid
* Don’t push your `.env` file to GitHub
* Sometimes AI output can be inconsistent, so minor formatting issues can happen

---

## What could be improved

* Better UI/UX
* More accurate skill ranking
* Adaptive difficulty in MCQs
* Detailed feedback instead of just score

---

## Why I built this

Most tools just compare keywords in resumes.
I wanted something that actually **checks understanding**, even if it's in a basic way.

---

## Author

Built as part of a hackathon project.

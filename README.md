# AI Resume Screening System

## Overview

This project is an AI-powered resume screening system that evaluates and ranks candidates based on how well their resumes match a given job description.

It combines semantic understanding using a pretrained NLP model with rule-based skill matching to produce a balanced and explainable evaluation.

---

## Features

* Upload multiple resumes (PDF, DOCX)
* Semantic similarity using Sentence Transformers
* Skill-based matching and gap analysis
* Hybrid scoring system (semantic + skills)
* Candidate ranking based on final score
* Strengths and gaps identification
* Recommendation (Strong Fit / Moderate Fit / Not Fit)
* Download results as CSV

---

## Tech Stack

* Python
* Streamlit
* Sentence Transformers (NLP)
* Scikit-learn
* PyMuPDF (PDF parsing)
* python-docx (DOCX parsing)
* Pandas

---

## Project Structure

```
ai-resume-screening/
│
├── app.py
├── requirements.txt
├── README.md
│
└── src/
    ├── __init__.py
    ├── parser.py
    ├── embedder.py
    └── analyzer.py
```

---

## How It Works

1. Resumes and job description are converted into text.
2. A pretrained sentence transformer model generates embeddings.
3. Cosine similarity computes semantic match between resume and JD.
4. Skills are extracted using keyword-based matching.
5. Final score is calculated using a hybrid approach:

   * 70% semantic similarity
   * 30% skill match
6. Candidates are ranked and analyzed with strengths, gaps, and recommendations.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-resume-screening.git
cd ai-resume-screening
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## Notes

* On first run, the sentence-transformers model will be downloaded, which may take some time.
* Ensure resumes are in PDF or DOCX format.

---

## Limitations

* Skill extraction is rule-based and depends on predefined keywords.
* Semantic scoring is based on a general-purpose model, not domain-specific.
* Does not currently support real-time learning or feedback.

---

## Future Improvements

* Dynamic skill extraction using NLP/NER
* LLM-based explanation generation
* Advanced UI/dashboard
* Deployment as a web application

---

## Author

Snehil Rai

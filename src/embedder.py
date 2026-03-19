from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Cache model so it loads only once (important for deployment)
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# Empirical cosine similarity bounds
_MIN_COSINE = 0.20
_MAX_COSINE = 0.95


def _normalize_score(raw: float) -> float:
    """
    Normalize cosine similarity to 0–100 range.
    """
    clamped = max(_MIN_COSINE, min(_MAX_COSINE, raw))
    scaled = (clamped - _MIN_COSINE) / (_MAX_COSINE - _MIN_COSINE)
    return round(scaled * 100, 2)


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Returns normalized semantic similarity score (0–100).
    """

    # basic validation
    if not resume_text or not jd_text:
        return 0.0

    if len(resume_text.split()) < 5 or len(jd_text.split()) < 5:
        return 0.0

    # generate embeddings
    resume_emb = model.encode(resume_text, convert_to_numpy=True)
    jd_emb = model.encode(jd_text, convert_to_numpy=True)

    # cosine similarity
    raw_score = cosine_similarity([resume_emb], [jd_emb])[0][0]

    return _normalize_score(float(raw_score))

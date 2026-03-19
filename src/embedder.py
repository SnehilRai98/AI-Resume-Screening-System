from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once at import time
_model = SentenceTransformer("all-MiniLM-L6-v2")

# Empirical cosine-similarity bounds for this model on resume/JD pairs.
# Raw cosine for completely unrelated texts ≈ 0.20
# Raw cosine for near-identical texts       ≈ 0.95
_MIN_COSINE = 0.20
_MAX_COSINE = 0.95


def _normalize_score(raw: float) -> float:
    """
    Re-scale raw cosine similarity from [_MIN_COSINE, _MAX_COSINE]
    to a human-readable 0–100 range so scores feel intuitive.
    """
    clamped = max(_MIN_COSINE, min(_MAX_COSINE, raw))
    scaled = (clamped - _MIN_COSINE) / (_MAX_COSINE - _MIN_COSINE)
    return round(scaled * 100, 2)


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Returns a normalised 0-100 semantic similarity score.
    Returns 0.0 if either input is empty/too short.
    """
    if not resume_text or not jd_text:
        return 0.0

    if len(resume_text.split()) < 5 or len(jd_text.split()) < 5:
        return 0.0

    resume_emb = _model.encode(resume_text, convert_to_numpy=True)
    jd_emb = _model.encode(jd_text, convert_to_numpy=True)

    raw = cosine_similarity([resume_emb], [jd_emb])[0][0]
    return _normalize_score(float(raw))

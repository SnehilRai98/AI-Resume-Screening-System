import streamlit as st
import pandas as pd

from src.parser import extract_text
from src.embedder import compute_similarity
from src.analyzer import analyze_resume, skill_match_score, get_recommendation

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="",
    layout="wide",
)

st.title(" AI Resume Screening System")
st.caption("Paste a Job Description and upload resumes to rank and analyse candidates.")

# ── Inputs ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    jd = st.text_area(
        " Job Description",
        height=300,
        placeholder="Paste the full job description here…",
    )

with col_right:
    uploaded_files = st.file_uploader(
        "📎 Upload Resumes (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )

st.divider()

# ── Analysis ──────────────────────────────────────────────────────────────────
if st.button(" Analyse Resumes", use_container_width=True):

    if not jd.strip():
        st.warning("  Please paste a Job Description before analysing.")
        st.stop()

    if not uploaded_files:
        st.warning("  Please upload at least one resume.")
        st.stop()

    results = []

    with st.spinner("Analysing resumes…"):
        for file in uploaded_files:
            resume_text = extract_text(file)

            if not resume_text:
                st.error(f"❌  **{file.name}** could not be read or appears empty.")
                continue

            # Scores
            semantic_score = compute_similarity(resume_text, jd)
            skill_score    = skill_match_score(resume_text, jd)

            # Hybrid score: 70% semantic + 30% skill keyword overlap
            final_score = round((0.7 * semantic_score) + (0.3 * skill_score), 2)

            # Strengths / gaps
            strengths, gaps = analyze_resume(resume_text, jd)

            # Recommendation (aligned with spec: Strong Fit / Moderate Fit / Not Fit)
            recommendation = get_recommendation(final_score)

            # Human-readable insight
            strengths_str = ", ".join(strengths) if strengths else "no matched skills"
            gaps_str      = ", ".join(gaps)      if gaps      else "none identified"
            explanation = (
                f"The candidate shows proficiency in **{strengths_str}**, "
                f"but is missing **{gaps_str}** from the job requirements. "
                f"Based on semantic context and skill alignment, "
                f"this profile is rated **{recommendation}**."
            )

            results.append({
                "Name":           file.name,
                "Semantic Score": semantic_score,
                "Skill Score":    skill_score,
                "Final Score":    final_score,
                "Strengths":      strengths,
                "Gaps":           gaps,
                "Recommendation": recommendation,
                "Explanation":    explanation,
            })

    if not results:
        st.error("No resumes could be processed. Please check your files.")
        st.stop()

    # Sort by Final Score descending
    results.sort(key=lambda x: x["Final Score"], reverse=True)

    # ── Results ───────────────────────────────────────────────────────────────
    st.subheader(" Results")

    top = results[0]
    st.success(f"🏆 Top Candidate: **{top['Name']}** — {top['Final Score']:.1f}% Final Score")

    # Recommendation colour map
    REC_COLOR = {
        "Strong Fit":   "🟢",
        "Moderate Fit": "🟡",
        "Not Fit":      "🔴",
    }

    for i, r in enumerate(results, start=1):
        icon = REC_COLOR.get(r["Recommendation"], "⚪")

        with st.expander(
            f"#{i}  {icon}  {r['Name']}  —  {r['Final Score']:.1f}%  |  {r['Recommendation']}",
            expanded=(i == 1),
        ):
            c1, c2, c3 = st.columns(3)
            c1.metric(" Semantic",  f"{r['Semantic Score']:.1f}%")
            c2.metric("  Skill",     f"{r['Skill Score']:.1f}%")
            c3.metric(" Final",     f"{r['Final Score']:.1f}%")

            total_skills   = len(r["Strengths"]) + len(r["Gaps"])
            matched_skills = len(r["Strengths"])
            coverage_pct   = int((matched_skills / total_skills * 100) if total_skills else 0)

            st.progress(coverage_pct / 100, text=f"Skill Coverage: {matched_skills}/{total_skills} ({coverage_pct}%)")

            st.write(f" **Strengths:** {', '.join(r['Strengths']) if r['Strengths'] else 'None'}")
            st.write(f"  **Gaps:**      {', '.join(r['Gaps']) if r['Gaps'] else 'None'}")
            st.markdown(f" **Insight:** {r['Explanation']}")

    st.divider()

    # ── Download ──────────────────────────────────────────────────────────────
    export_rows = [
        {
            "Rank":           i + 1,
            "Name":           r["Name"],
            "Semantic Score": r["Semantic Score"],
            "Skill Score":    r["Skill Score"],
            "Final Score":    r["Final Score"],
            "Strengths":      ", ".join(r["Strengths"]),
            "Gaps":           ", ".join(r["Gaps"]),
            "Recommendation": r["Recommendation"],
            "Explanation":    r["Explanation"],
        }
        for i, r in enumerate(results)
    ]

    df = pd.DataFrame(export_rows)

    st.download_button(
        label="  Download Results as CSV",
        data=df.to_csv(index=False),
        file_name="screening_results.csv",
        mime="text/csv",
        use_container_width=True,
    )

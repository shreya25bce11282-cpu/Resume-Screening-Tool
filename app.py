import streamlit as st
import pandas as pd
import os

# Sidebar controls
st.sidebar.header("Scoring Weights")

SKILL_WEIGHT = st.sidebar.slider(
    "Skill Match Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.7
)

EXPERIENCE_WEIGHT = st.sidebar.slider(
    "Experience Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.3
)

THRESHOLD = st.sidebar.slider(
    "Minimum Match Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.3
)

# Imports from your modules
from resume_parser import (
    extract_text_from_pdf,
    clean_text,
    normalize_synonyms,
    apply_skill_weighting,
    extract_years_of_experience
)
from vectorizer import vectorize_texts
from matcher import calculate_similarity
from skills import SKILL_LIST

st.title("AI-Powered Resume Screening Tool")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area("Paste Job Description")

if uploaded_files and job_description:

    resume_texts = []
    resume_names = []
    experience_years = []

    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())

        raw_text = extract_text_from_pdf(file.name)
        cleaned_text = clean_text(raw_text)
        normalized_text = normalize_synonyms(cleaned_text)
        weighted_text = apply_skill_weighting(normalized_text, SKILL_LIST)
        
        years = extract_years_of_experience(raw_text)

        resume_texts.append(weighted_text)
        resume_names.append(file.name)
        experience_years.append(years)

        os.remove(file.name)

    max_experience = max(experience_years) if experience_years else 1
    if max_experience == 0:
        max_experience = 1  # avoid division by zero

    normalized_experience = [years / max_experience for years in experience_years]

    all_texts = resume_texts + [job_description]
    vectors = vectorize_texts(all_texts)
    jd_vector = vectors[-1]

    scores = []
    final_scores = []

    for i in range(len(resume_texts)):
        similarity = calculate_similarity(vectors[i], jd_vector)
        scores.append(similarity)

        final_score = (
            SKILL_WEIGHT * similarity +
            EXPERIENCE_WEIGHT * normalized_experience[i]
        )
        final_scores.append(final_score)

    explanations = []

    for i in range(len(scores)):
        explanations.append({
            "Resume": resume_names[i],
            "Skill Match Score": round(scores[i], 3),
            "Experience (Years)": experience_years[i],
            "Normalized Experience": round(normalized_experience[i], 3),
            "Skill Contribution": round(scores[i] * SKILL_WEIGHT, 3),
            "Experience Contribution": round(normalized_experience[i] * EXPERIENCE_WEIGHT, 3),
            "Final Score": round(final_scores[i], 3)
        })

    results_df = pd.DataFrame(explanations)

    # Filter by threshold on Final Score
    results_df = results_df[results_df["Final Score"] >= THRESHOLD]

    # Reorder columns explicitly
    columns_order = [
        "Resume",
        "Skill Match Score",
        "Experience (Years)",
        "Normalized Experience",
        "Skill Contribution",
        "Experience Contribution",
        "Final Score"
    ]
    results_df = results_df[columns_order]

    results_df = results_df.sort_values(by="Final Score", ascending=False).reset_index(drop=True)

    st.subheader("Ranked Candidates")
    st.dataframe(results_df)

    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="ranked_resumes.csv",
        mime="text/csv"
    )

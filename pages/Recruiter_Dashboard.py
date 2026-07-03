from utils.parser import ResumeParser
from utils.preprocessing import TextPreprocessor
from utils.skill_extractor import SkillExtractor
from utils.similarity import ResumeSimilarity
import streamlit as st

@st.cache_resource
def load_models():
    return (
        ResumeParser(),
        TextPreprocessor(),
        SkillExtractor(),
        ResumeSimilarity()
    )

parser, preprocessor, extractor, similarity = load_models()

st.set_page_config(
    page_title="Recruiter Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 AI Recruitment Dashboard")

st.markdown("### 📄 Job Description")

job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

st.markdown("### 📂 Upload Candidate Resumes")

uploaded_files = st.file_uploader(
    "Upload PDF Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"✅ {len(uploaded_files)} resumes uploaded.")

    st.subheader("Uploaded Candidates")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

if st.button("🚀 Analyze Candidates"):

    if not job_description:
        st.warning("Please enter a Job Description.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload resumes.")
        st.stop()

    results = []

    clean_job = preprocessor.clean_text(job_description)
    job_skills = extractor.extract_skills(clean_job)

    progress = st.progress(0)

    for index, file in enumerate(uploaded_files):

        # Extract Resume
        resume_text = parser.extract_text(file)

        # Clean Resume
        clean_resume = preprocessor.clean_text(resume_text)

        # Extract Skills
        resume_skills = extractor.extract_skills(clean_resume)

        # Calculate Similarity
        score = similarity.calculate_similarity(
            clean_resume,
            clean_job
        )

        matched = len(
            set(resume_skills).intersection(job_skills)
        )

        if score >= 85:
            status = "🟢 Hire"
        elif score >= 45:
            status = "🟡 Shortlist"
        else:
            status = "🔴 Reject"

        results.append({
            "Candidate": file.name,
            "Score": round(score, 2),
            "Resume Skills": len(resume_skills),
            "Matched Skills": matched,
            "Status": status
        })

        progress.progress((index + 1) / len(uploaded_files))

    # ---------------- Sort Results ----------------

    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    for i, row in enumerate(results):
        row["Rank"] = i + 1

    st.success("✅ Analysis Completed!")

    # ---------------- Dashboard ----------------

    top_score = results[0]["Score"]

    avg_score = round(
        sum(r["Score"] for r in results) / len(results),
        2
    )

    total_candidates = len(results)

    hire_count = len(
        [r for r in results if "Hire" in r["Status"]]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏆 Top Score",
            f"{top_score}%"
        )

    with col2:
        st.metric(
            "📈 Average Score",
            f"{avg_score}%"
        )

    with col3:
        st.metric(
            "👥 Candidates",
            total_candidates
        )

    with col4:
        st.metric(
            "✅ Recommended",
            hire_count
        )

    # ---------------- Ranking ----------------

    st.subheader("🏆 Candidate Ranking")

    import pandas as pd

    df = pd.DataFrame(results)

    df = df[
        [
            "Rank",
            "Candidate",
            "Score",
            "Matched Skills",
            "Resume Skills",
            "Status"
        ]
    ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
import pandas as pd
import streamlit as st
from components.upload import upload_resume
from streamlit_option_menu import option_menu
from utils.preprocessing import TextPreprocessor
from utils.skill_extractor import SkillExtractor
from utils.similarity import ResumeSimilarity
import plotly.graph_objects as go

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🤖",
    layout="wide",
)
load_css()
@st.cache_resource
def load_models():
    return (
        TextPreprocessor(),
        SkillExtractor(),
        ResumeSimilarity()
    )

preprocessor, extractor, similarity = load_models()

# ---------------- Sidebar ----------------
with st.sidebar:

    st.markdown("""
    <div style='text-align:center;padding:15px;'>
        <h2 style='color:white;'>🤖 Resume AI</h2>
        <p style='color:#d1d5db;font-size:14px;'>
            AI Resume Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Job Description",
            "Upload Resume",
            "Candidates",
            "Results",
            "Analytics"
        ],
        icons=[
            "house",
            "file-earmark-text",
            "cloud-upload",
            "people",
            "clipboard-data",
            "graph-up"
        ],
        default_index=0,
    )

    st.markdown("---")

    st.markdown(
        """
        <div style='text-align:center;
                    color:#cfcfcf;
                    font-size:12px;
                    padding-top:20px;'>

        Version 1.0

        Made by <b>Deepak</b>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Main Page ----------------
st.markdown("""
<div style="
padding:25px;
border-radius:18px;
background:linear-gradient(90deg,#4F46E5,#06B6D4);
color:white;
text-align:center;
margin-bottom:30px;
box-shadow:0px 6px 18px rgba(0,0,0,0.2);
">

<h1 style="margin-bottom:10px;">
🤖 AI Resume Intelligence Platform
</h1>

<p style="font-size:18px;">
Analyze resumes against job descriptions using Artificial Intelligence
</p>

</div>
""", unsafe_allow_html=True)
resumes = upload_resume()

resume_text = ""

if resumes:
    st.subheader("📄 Uploaded Resumes")

    resume_names = [resume["filename"] for resume in resumes]

    selected_resume = st.selectbox(
        "Select Resume",
        resume_names
    )

    for resume in resumes:
        if resume["filename"] == selected_resume:
            resume_text = resume["text"]
            break

    st.text_area(
        "Resume Content",
        resume_text,
        height=250
    )
st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the job description here..."
)
analyze = st.button("🚀 Analyze Resume")


if analyze:

    if resumes and job_description:

        progress = st.progress(0)
        status = st.empty()

        status.info("📄 Reading Resume...")
        progress.progress(20)

        clean_resume = preprocessor.clean_text(resume_text)
        clean_job = preprocessor.clean_text(job_description)

        status.info("🧹 Cleaning Resume...")
        progress.progress(40)

        resume_skills = extractor.extract_skills(clean_resume)
        job_skills = extractor.extract_skills(clean_job)

        status.info("🧠 Extracting Skills...")
        progress.progress(60)

        score = similarity.calculate_similarity(
            clean_resume,
            clean_job
        )

        status.info("🤖 AI Matching Resume...")
        progress.progress(90)

        progress.progress(100)
        status.success("✅ Analysis Completed!")

        # Continue with your existing code...

        resume_skills = extractor.extract_skills(clean_resume)
        job_skills = extractor.extract_skills(clean_job)

        score = similarity.calculate_similarity(
            clean_resume,
            clean_job
        )

        matched_skills = []

        missing_skills = []

        for skill in job_skills:
            if skill in resume_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        st.subheader("🎯 Overall Match Score")

        fig = go.Figure(
    go.Pie(
        values=[score, 100 - score],
        hole=0.75,                 # Bigger hole = donut
        rotation=90,
        sort=False,
        textinfo="none",
        marker=dict(
            colors=["#4F46E5", "#E5E7EB"],
            line=dict(color="white", width=4)
        )
    )
)

        fig.update_layout(
    height=320,
    width=320,
    margin=dict(t=20, b=20, l=20, r=20),
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    annotations=[
        dict(
            text=f"<b style='font-size:28px'>{score:.1f}%</b><br><span style='font-size:14px;color:gray'>Match Score</span>",
            x=0.5,
            y=0.5,
            showarrow=False
        )
    ]
)

        st.plotly_chart(fig, use_container_width=True)

        if score >= 80:
            st.success("⭐ Excellent Match")
        elif score >= 60:
            st.info("👍 Good Match")
        elif score >= 40:
            st.warning("⚠ Average Match")
        else:
            st.error("❌ Poor Match")

        # ---------------- Resume Skills ----------------
        st.subheader("🧠 Resume Skills")

        badge_html = ""

        for skill in resume_skills:
            badge_html += f"""
            <span style="
                display:inline-block;
                background:#4F46E5;
                color:white;
                padding:8px 14px;
                margin:6px;
                border-radius:20px;
                font-size:14px;
                font-weight:500;">
                {skill}
            </span>
            """

        st.markdown(badge_html, unsafe_allow_html=True)

        # ---------------- Matching Skills ----------------
        st.subheader("✅ Matching Skills")

        match_html = ""

        for skill in matched_skills:
            match_html += f"""
            <span style="
                display:inline-block;
                background:#16a34a;
                color:white;
                padding:8px 14px;
                margin:6px;
                border-radius:20px;
                font-size:14px;">
                ✓ {skill}
            </span>
            """

        st.markdown(match_html, unsafe_allow_html=True)

        # ---------------- Missing Skills ----------------
        st.subheader("❌ Missing Skills")

        missing_html = ""

        for skill in missing_skills:
            missing_html += f"""
            <span style="
                display:inline-block;
                background:#dc2626;
                color:white;
                padding:8px 14px;
                margin:6px;
                border-radius:20px;
                font-size:14px;">
                ✗ {skill}
            </span>
            """

        st.markdown(missing_html, unsafe_allow_html=True)

        # ---------------- Recommendation ----------------
        st.subheader("💡 AI Recommendation")

        if len(missing_skills) == 0:
            st.success("🎉 Candidate is an excellent fit for this role.")
        else:
            st.info("To improve the resume match, focus on these skills:")

            for skill in missing_skills:
                st.write(f"✔ {skill}")
        
st.write(f"Current Page: **{selected}**")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏆 Top Match Score",
        value="92%",
        delta="+5%"
    )

with col2:
    st.metric(
        label="📈 Average Match Score",
        value="76%",
        delta="+2%"
    )

with col3:
    st.metric(
        label="👥 Candidates",
        value="10"
    )

with col4:
    st.metric(
        label="🎯 Skills Matched",
        value="85%"
    )
st.markdown("---")

st.subheader("🏆 Candidate Ranking")

candidate_data = pd.DataFrame(
    {
        "Rank": [1, 2, 3, 4, 5],
        "Candidate": [
            "John Doe",
            "Alice Smith",
            "Robert Brown",
            "Michael Johnson",
            "Emma Wilson",
        ],
        "Match Score": ["92%", "87%", "81%", "76%", "71%"],
        "Status": [
            "Excellent",
            "Excellent",
            "Very Good",
            "Good",
            "Good",
        ],
    }
)

st.dataframe(candidate_data, use_container_width=True, hide_index=True)
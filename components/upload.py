import streamlit as st
from utils.parser import ResumeParser


@st.cache_resource
def get_parser():
    return ResumeParser()


def upload_resume():

    st.markdown("""
    <div style="
        padding:20px;
        border-radius:15px;
        background:#F8FAFC;
        border:2px dashed #4F46E5;
        text-align:center;
        margin-bottom:20px;
    ">
        <h3>📤 Upload Your Resume</h3>
        <p style="color:gray;">
            Upload your resume in <b>PDF</b> format to begin AI-powered analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        st.info("📄 Supported format: PDF")
        return []

    parser = get_parser()

    st.success(f"✅ {len(uploaded_files)} resume(s) uploaded successfully!")

    resumes = []

    for file in uploaded_files:

        text = parser.extract_text(file)

        st.write("📄 File:", file.name)
        st.write("Characters extracted:", len(text))

        if text:
            st.success("✅ Text extracted successfully")
        else:
            st.error("❌ No text extracted")

        resumes.append({
            "filename": file.name,
            "text": text
        })

    return resumes
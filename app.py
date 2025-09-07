import streamlit as st
import openai
from io import BytesIO
import PyPDF2
import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="wide"
)

class ResumeReviewer:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:  # Check extraction success
                    text += page_text + "\n"
            if not text.strip():
                st.error("No text could be extracted. Please check your PDF is typed, not scanned.")
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""

    def analyze_resume(self, resume_text: str, job_role: str, job_description: str = "") -> Dict:
        """Analyze resume using OpenAI GPT"""
        prompt = f"""
As an expert HR professional and career coach, analyze this resume for a {job_role} position.

Resume Text:
{resume_text}

{"Job Description: " + job_description if job_description else ""}

Provide detailed feedback in the following structure:

1. OVERALL SCORE: Rate the resume 1-10 for the target role

2. STRENGTHS:
- List 3-4 key strengths

3. AREAS FOR IMPROVEMENT:
- Missing skills/keywords for {job_role}
- Formatting/structure issues
- Content clarity problems

4. SPECIFIC RECOMMENDATIONS:
- Actionable suggestions to improve the resume
- Keywords to add
- Sections to enhance

5. SECTION-BY-SECTION FEEDBACK:
- Professional Summary/Objective
- Work Experience
- Skills
- Education
- Other sections

Be specific, constructive, and actionable in your feedback.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.3
            )
            # Defensive: check that the structure exists to prevent errors
            if (response.choices and
                hasattr(response.choices, "message") and
                hasattr(response.choices.message, "content")):
                feedback = response.choices.message.content
                return {"success": True, "feedback": feedback}
            else:
                return {"success": False, "error": "No feedback returned from OpenAI."}
        except Exception as e:
            error_message = str(e)
            if "API key" in error_message:
                error_message += " Please check your OpenAI API key."
            return {"success": False, "error": error_message}

def main():
    st.title("🎯 AI-Powered Resume Reviewer")
    st.markdown("Get tailored feedback to optimize your resume for specific job roles")

    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        default_key = os.getenv("OPENAI_API_KEY", "")
        api_key = st.text_input(
            "OpenAI API Key",
            value=default_key,
            type="password",
            placeholder="Enter your OpenAI API key"
        )  # Fixed: Add placeholder argument
        if not api_key:
            st.warning("Please enter your OpenAI API key to use the resume reviewer")
            st.stop()

    reviewer = ResumeReviewer(api_key)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📄 Upload Resume")
        input_method = st.radio("Choose input method:", ["Upload PDF", "Paste Text"])
        resume_text = ""

        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
            if uploaded_file:
                resume_text = reviewer.extract_text_from_pdf(uploaded_file)
                if resume_text:
                    st.success("PDF uploaded and text extracted successfully!")
                    with st.expander("Preview extracted text"):
                        st.text_area("Extracted text:", resume_text, height=200, disabled=True)
                else:
                    st.error("No text extracted. Try pasting text or uploading a different PDF.")
        else:
            resume_text = st.text_area(
                "Paste your resume text here:",
                height=300,
                placeholder="Paste your resume content here"
            )  # Fixed: Add placeholder argument

        # Job role and description
        st.header("🎯 Target Position")
        job_role = st.text_input(
            "Job Role/Title",
            placeholder="e.g., Data Scientist, Product Manager"
        )  # Fixed: Add placeholder argument

        job_description = st.text_area(
            "Job Description (Optional)",
            height=150,
            placeholder="Paste the job description here for more targeted feedback..."
        )  # Fixed: Add placeholder argument

    with col2:
        st.header("📊 AI Feedback")
        analyze_disabled = not (resume_text and job_role)
        if st.button("🔍 Analyze Resume", type="primary", disabled=analyze_disabled):
            if not resume_text:
                st.error("Please provide your resume text")
            elif not job_role:
                st.error("Please specify the target job role")
            else:
                with st.spinner("Analyzing your resume..."):
                    result = reviewer.analyze_resume(resume_text, job_role, job_description)
                if result["success"]:
                    st.markdown("### 📋 Analysis Results")
                    st.markdown(result["feedback"])
                    st.download_button(
                        label="📥 Download Feedback",
                        data=result["feedback"],
                        file_name=f"resume_feedback_{job_role.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Analysis failed: {result['error']}")

        with st.expander("💡 Tips for Better Results"):
            st.markdown("""
- **Be specific** with job roles (e.g., "Senior Data Scientist" vs "Data Scientist")
- **Include job descriptions** for more targeted feedback
- **Ensure clear text** in PDF uploads
- **Review multiple versions** to track improvements
            """)

if __name__ == "__main__":
    main()

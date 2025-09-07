# AI Resume Reviewer

An LLM-powered application that provides tailored feedback on resumes for specific job roles.

## Features

- **Resume Upload**: Support for PDF files and text input
- **Job Role Targeting**: Specify target position for tailored feedback
- **AI Analysis**: GPT-powered review with structured feedback
- **Downloadable Results**: Export feedback as text file
- **Privacy-First**: No data storage, processing happens in real-time

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Create an API key from your dashboard

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

4. **Use the App**
   - Enter your OpenAI API key in the sidebar
   - Upload PDF or paste resume text
   - Specify target job role
   - Get AI-powered feedback

## Usage Tips

- Be specific with job roles (e.g., "Senior Data Scientist")
- Include job descriptions for more targeted feedback
- Ensure PDF text is clear and readable
- Review multiple versions to track improvements

## Security

- API keys are not stored
- Resume data is processed in real-time only
- No data persistence or external storage
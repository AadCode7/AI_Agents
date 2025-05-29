import streamlit as st
import PyPDF2
import io 
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon=":mag_right:", layout="centered")
st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format and get feedback on how to improve it.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf","txt"])
job_role = st.text_input("Enter the job role you are applying for (optional)", placeholder="e.g., Software Engineer, Data Scientist")

analyse = st.button("Analyse Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8").strip()

if analyse and uploaded_file is not None:
    st.write("Button Pressed!")
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content:
            st.error("The uploaded file is empty or could not be read. Please upload a valid resume.")
            st.stop()

        prompt = f"""Please analyse this resume and provide constructive feedback. Focus on the following aspects: 1. Content clarity and impact, 2. Skills presentation, 3. Experience Descriptions, 4. Specific Improvements for {job_role if job_role else 'general job applications'}

        Resume Content:
        {file_content}
        
        Please provide you analysis in a clear, structured format with specific suggestions for improvement.        
        """
        
        client = OpenAI(api_key = OPENAI_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ], 
            temperature = 0.7
            max_tokens = 1000
        )

        st.markdown("### Analysis Result")
        st.write(response.choices[0].message.content.strip())   


    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")

import streamlit as st
import requests  # Required to talk to your Azure Function
import base64    # Required to encode the PDF for transport
import os
from dotenv import load_dotenv #

load_dotenv()
# --- CONFIGURATION ---
# IMPORTANT: Replace this with the URL you copied from VS Code or the Azure Portal
AZURE_FUNCTION_URL = os.getenv("AZURE_FUNCTION_URL")
st.set_page_config(page_title="AI Resume Matcher Pro", page_icon="📄")

st.title("📄 AI Resume Matcher Pro")
st.markdown("Upload your resume and paste a job description to see how well you match using our **Azure Serverless Backend**.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    st.info("Backend: Azure Functions (Python)\nAI Engine: Gemini 2.5-Flash-Lite")
    st.markdown("---")
    st.markdown("Created by Rayn Shamieh")

# --- MAIN INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose your Resume PDF", type="pdf")

with col2:
    st.subheader("2. Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=250)

# --- ANALYSIS TRIGGER ---
if st.button("Analyze Match"):
    if uploaded_file and jd_text:
        with st.spinner("🤖 Sending data to Azure Serverless Backend..."):
            try:
                # 1. Convert PDF bytes to base64 string for JSON transport
                pdf_bytes = uploaded_file.getvalue()
                encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                
                # 2. Construct the data payload for your Azure Function
                payload = {
                    "resume_bytes": encoded_pdf,
                    "jd_text": jd_text
                }
                
                # 3. Call the Cloud API
                response = requests.post(AZURE_FUNCTION_URL, json=payload)
                
                # 4. Display the results
                if response.status_code == 200:
                    analysis_data = response.json()
                    report = analysis_data.get("analysis", "No analysis returned.")
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📊 AI Analysis Report")
                    st.markdown(report)
                else:
                    st.error(f"Azure Backend Error ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Connection Error: Could not reach Azure. Ensure your URL is correct. Details: {str(e)}")
    else:
        st.warning("Please provide both a Resume PDF and a Job Description.")
import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURATION ---
API_KEY = "AIzaSyBBe9wTr90nnVD6dxY5ppdzDgVp1A08leY"
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄")

st.title("📄 AI Resume Matcher Pro")
st.markdown("Upload your resume and paste a job description to see how well you match.")

# --- SIDEBAR: Settings ---
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Select Model", ["gemini-2.5-flash-lite", "gemini-1.5-flash-8b"])
    st.info("Using 2.5-Flash-Lite for best free-tier stability.")

# --- MAIN INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose your Resume PDF", type="pdf")

with col2:
    st.subheader("2. Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze Match"):
    if uploaded_file and jd_text:
        with st.spinner("🤖 Gemini is analyzing your profile..."):
            try:
                # Prepare prompt
                prompt = f"Analyze this Resume PDF against the JD: {jd_text}. Provide Match Score (%), Missing Skills, and 3 specific Improvements."
                
                # Call Gemini
                response = client.models.generate_content(
                    model=model_choice,
                    contents=[
                        types.Part.from_bytes(
                            data=uploaded_file.getvalue(),
                            mime_type='application/pdf'
                        ),
                        prompt
                    ]
                )
                
                # Display Results
                st.success("Analysis Complete!")
                st.markdown("### 📊 Report")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload a PDF and provide a Job Description.")


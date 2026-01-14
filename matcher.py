import pathlib
from google import genai
from google.genai import types

# --- CONFIGURATION ---
import os
# This looks for the key in your computer's hidden settings
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})

def get_first_pdf():
    """Finds the first PDF file in the current directory."""
    pdfs = list(pathlib.Path('.').glob('*.pdf'))
    return pdfs[0] if pdfs else None

def analyze_resume_pdf(pdf_path, jd_text):
    prompt = f"""
    Analyze the attached Resume PDF against this Job Description:
    {jd_text}
    
    Provide:
    1. Match Score (0-100%)
    2. Missing Keywords
    3. 3 specific Resume Improvements
    """

    try:
        print(f"🚀 Analyzing: {pdf_path}...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[
                types.Part.from_bytes(
                    data=pdf_path.read_bytes(),
                    mime_type='application/pdf'
                ),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    resume_path = get_first_pdf()
    if not resume_path:
        print("❌ Error: No PDF file found in this folder.")
        return

    job_desc = "Looking for a Python Developer with AI experience."

    report = analyze_resume_pdf(resume_path, job_desc)
    print("\n" + "="*40 + "\n" + report)

if __name__ == "__main__":
    main()

import os
import azure.functions as func
from google import genai
from google.genai import types
import json

app = func.FunctionApp()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})


@app.route(route="analyze", auth_level=func.AuthLevel.FUNCTION)
def resume_matcher_func(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        resume_bytes = req_body.get('resume_bytes') 
        jd_text = req_body.get('jd_text')

        prompt = f"Analyze this Resume against the JD: {jd_text}. Return Score, Gaps, and 3 Tips."

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[
                types.Part.from_bytes(data=resume_bytes, mime_type='application/pdf'),
                prompt
            ]
        )

        return func.HttpResponse(
            json.dumps({"analysis": response.text}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

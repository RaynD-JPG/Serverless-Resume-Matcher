# 📄 AI Resume Matcher Pro

A serverless, cloud-native application that analyzes resumes against job descriptions using Google Gemini 2.5-Flash-Lite and Azure Functions.

## 🚀 Overview
This project demonstrates a decoupled architecture with a Python-based Streamlit frontend and an Azure Serverless backend. It provides real-time AI feedback on resume-JD alignment, identifying skill gaps and providing actionable tips for job seekers.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python)
- **Backend**: Azure Functions (Serverless / Python v2 Model)
- **AI Model**: Google Gemini 2.5-Flash-Lite
- **Security**: Environment Variables, .env protection, and Azure App Settings

## 🏗️ Architecture
- **Frontend**: Captures PDF data and encodes it into Base64 for secure transport.
- **Backend**: An HTTP-triggered Azure Function that decodes data, processes it via the Gemini API, and returns a JSON analysis.
- **Security**: Sensitive API keys are stored in Azure App Settings (not in code), and the backend endpoint is protected via function-level authorization.

## ⚙️ Setup & Installation

1. **Clone the repo**:
   ```bash
   git clone [https://github.com/RaynD-JPG/Serverless-Resume-Matcher.git](https://github.com/RaynD-JPG/Serverless-Resume-Matcher.git)
   cd Serverless-Resume-Matcher
import os
import json
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback/Debug: try to find it in the current working directory if not found above
    api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key.strip())
else:
    print("Warning: GOOGLE_API_KEY not found in environment.")

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file object."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def parse_json_response(response_text):
    """Cleans and parses the JSON response from the AI."""
    try:
        # Attempt to find JSON structure if wrapped in other text
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = response_text[start:end]
            return json.loads(json_str)
        else:
            return None
    except json.JSONDecodeError:
        return None

def analyze_resume_gemini(resume_text, jd_text):
    """
    Analyzes a resume against a JD using Gemini.
    Returns a dictionary with the analysis results.
    """
    prompt = f"""
    You are a "Brutal & Strategic Career Architect" specializing in helping MBA candidates pivot from Industrial/Operations backgrounds (e.g., Manufacturing, Engineering) into high-tier Marketing and Consulting roles.
    
    Current State: The recruiter has 10 seconds. If they smell "Factory Owner" instead of "Brand Manager", this file is trash.
    
    Job Description:
    {jd_text}
    
    Resume Content:
    {resume_text}
    
    Instructions:
    1. **The 'Operations Trap' Detection**:
       - Scan for industrial titles (Engineer, Ops Assistant) vs. Marketing/Consulting JD.
       - If found, your 'Brutal Diagnosis' MUST explicitly call out this framing as a rejection trigger.
    
    2. **The 'Strategic Kill Shot'**:
       - tailored for High-Impact Projects (GTM strategies, Case Competitions, National Semifinalist titles).
       - Command the user to move these to the TOP 10% of the resume, ignoring chronology if needed.
    
    3. **The Transformation Engine (Before & After)**:
       - Find 3 real bullet points from the resume (Industrial/Ops focused).
       - Rewrite them into "Corporate Strategy/Marketing" language.
       - Rules: 
         - 'SKU Management' -> 'Portfolio Logistics'
         - 'CSR Events' -> 'BTL Consumer Engagement'
         - 'Production Targets' -> 'Operational KPIs & Efficiency'
         - 'Supervising Workers' -> 'Stakeholder Management'
    
    4. **Output strictly valid JSON** with this structure:
    {{
        "score": (integer 0-100),
        "brutal_diagnosis": [(list of 3-4 harsh, direct bullet points. Call out the Ops Trap if applicable)],
        "high_priority_fixes": [(list of 6 actionable, high-ROI fixes. Put 'Kill Shot' moves first)],
        "keyword_gap_analysis": [
            {{ "missing_keyword": "string", "category": "Technical/Soft/Industry", "importance": "High/Med" }}
        ],
        "transformation_engine": [
            {{ "before": "Original bullet point", "after": "Rewritten 'Consulting/Marketing' bullet", "explanation": "Why this shift works" }}
        ]
    }}
    """

    try:
        # User requested gemini-2.0-flash
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content(prompt)
        parsed_result = parse_json_response(response.text)
        
        if parsed_result:
            return parsed_result
        else:
            return {
                "score": 0,
                "missing_keywords": ["Error parsing output"],
                "strengths": [],
                "reason": "AI failed to return valid JSON. Raw output: " + response.text[:100] + "..."
            }
            
    except Exception as e:
         return {
                "score": 0,
                "missing_keywords": ["API Error"],
                "strengths": [],
                "reason": f"System Error: {str(e)}"
            }

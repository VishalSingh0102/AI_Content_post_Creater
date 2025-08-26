import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Choose a Gemini model
MODEL = "gemini-1.5-flash"   # free & fast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    topic: str

@app.post("/generate")
def generate_text(request: PromptRequest):
    prompt = f"Write a detailed LinkedIn post about {request.topic}."
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        # Extract text safely
        if hasattr(response, "text") and response.text:
            result_text = response.text
        else:
            # fallback for different response structure
            result_text = response.candidates[0].content.parts[0].text

        return {"result": result_text.replace("\n", "<br>")}

    except Exception as e:
        return {"error": str(e)}
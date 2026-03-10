from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

# ===== GEMINI CLIENT =====
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ===== FASTAPI APP =====
app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HOME PAGE =====
@app.get("/")
def home():
    return {
        "message": "AI Test Generator ishlayapti 🚀"
    }

# ===== REQUEST MODEL =====
class Question(BaseModel):
    question: str

# ===== TEST GENERATOR =====
@app.post("/generate")
async def generate_test(data: Question):

    prompt = f"""
Quyidagi savoldan 4 variantli test tuz.

Savol: {data.question}

A) ...
B) ...
C) ...
D) ...

Oxirida to'g'ri javobni yoz.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return {
            "test": response.text.replace("\n", "<br>")
        }

    except Exception as e:
        return {
            "error": str(e)
        }
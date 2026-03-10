from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ===== GEMINI API KEY (Render Environment dan olinadi) =====
genai.configure(api_key=os.getenv("AIzaSyAY2XcohwWpS-wfQNCWUAJcoY8vm-QAssQ"))

# ===== MODEL =====
model = genai.GenerativeModel("gemini-1.5-flash")

# ===== FASTAPI =====
app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HOME ROUTE =====
@app.get("/")
def home():
    return {"message": "AI Test Generator ishlayapti 🚀"}

# ===== REQUEST MODEL =====
class Question(BaseModel):
    question: str

# ===== TEST GENERATOR =====
@app.post("/generate")
async def generate_test(data: Question):

    try:
        prompt = f"""
Quyidagi savoldan 4 variantli test tuz.

Format:
Savol: ...
A) ...
B) ...
C) ...
D) ...

Oxirida to'g'ri javobni yoz.

Savol: {data.question}
"""

        response = model.generate_content(prompt)

        if not response.text:
            return {"error": "AI javob qaytarmadi"}

        return {
            "test": response.text.replace("\n", "<br>")
        }

    except Exception as e:
        return {"error": str(e)}
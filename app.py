from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Bosh sahifa HTML ochadi
@app.get("/")
def home():
    return FileResponse("index.html")

class Question(BaseModel):
    question: str

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
        text = response.text or ""
        return {"test": text.replace("\n", "<br>")}
    except Exception as e:
        return {"error": str(e)}
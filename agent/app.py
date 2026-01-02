import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# --------------------------------------------------
# 1. CARGAR VARIABLES DE ENTORNO
# --------------------------------------------------
load_dotenv()



if not HF_API_KEY:
    raise RuntimeError("❌ No se encontró la variable HF_API_KEY")

# --------------------------------------------------
# 2. INICIALIZAR CLIENTE HF (TOGETHER)
# --------------------------------------------------
client = InferenceClient(
    provider="together",
    api_key=HF_API_KEY
)

# --------------------------------------------------
# 3. FASTAPI
# --------------------------------------------------
app = FastAPI(title="Jeffersson AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# --------------------------------------------------
# 4. ENDPOINT CHAT
# --------------------------------------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres el asistente virtual del portafolio de Jeffersson Pretell. "
                        "Responde siempre en español, de forma profesional y clara."
                    )
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            max_tokens=512,
            temperature=0.3
        )

        return {
            "response": completion.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

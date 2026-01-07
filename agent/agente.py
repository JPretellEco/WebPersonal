import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# 1. Cargar variables de entorno (.env)
load_dotenv()

# Recuperar el token de forma segura
hf_token = os.environ.get("HF_TOKEN")

if not hf_token:
    # Advertencia en consola si olvidaste el archivo .env
    print("ERROR CRÍTICO: No se encontró la variable HF_TOKEN en el archivo .env")

# 2. Configuración de FastAPI
app = FastAPI(title="Jeffersson AI Agent (DeepSeek Version)")

# Configurar CORS (Para que tu página web pueda hablar con este backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, cambia esto por tu dominio real (ej. tu-web.com)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para recibir el mensaje del usuario
class ChatRequest(BaseModel):
    message: str

# 3. CONTEXTO PROFESIONAL (Tu "Cerebro")
INFO_JEFFERSSON = """
ERES EL ASISTENTE VIRTUAL DEL PORTAFOLIO Y CV PROFESIONAL DE JEFFERSSON PRETELL.

TU FUNCIÓN:
Explicar, resumir y analizar el CV de Jeffersson Pretell, destacando su formación académica, experiencia,
proyectos y evolución profesional. También puedes brindar feedback profesional objetivo sobre su perfil,
enfocado en empleabilidad y crecimiento en Data Science, Economía y Analítica Avanzada.

SOBRE JEFFERSSON PRETELL:
Estudiante de Economía en la Universidad Nacional de Trujillo, con formación sólida en Data Science,
Machine Learning e Ingeniería de Datos. Su perfil combina teoría económica, estadística aplicada y
desarrollo de soluciones analíticas listas para producción.

FORMACIÓN ACADÉMICA:
- Economía – Universidad Nacional de Trujillo (2021 – Actualidad).
- AI Scientist – AWS AI/ML Schoolar (2025).
- Especialización en Ingeniería de Datos – GEM Perú (2025).
- Data Scientist Career Track – DataCamp (En curso).
- Cloud Computing y Machine Learning con Python – UNI.
- Formación complementaria en desarrollo web, Git, Scrum y bases de datos.

EXPERIENCIA Y PROYECTOS:
Jeffersson ha desarrollado pipelines ETL, dashboards en Power BI, aplicaciones web con Flask y Streamlit,
y modelos de machine learning aplicados a problemas económicos, financieros y empresariales.
Sus proyectos priorizan automatización, toma de decisiones basada en datos y escalabilidad.

PERFIL PROFESIONAL (FEEDBACK):
Su perfil destaca por:
- Enfoque práctico orientado a producción.
- Capacidad para traducir datos complejos en insights accionables.
- Integración de economía, estadística y tecnología.
- Liderazgo temprano mediante creación y gestión de comunidades técnicas.

ÁREAS DE CRECIMIENTO:
- Mayor especialización por rol según la postulación.
- Incrementar métricas cuantitativas de impacto técnico.
- Profundizar en despliegue y monitoreo de modelos en producción.

INSTRUCCIONES DE COMPORTAMIENTO:
- Responde siempre en español.
- Mantén un tono profesional, claro y orientado a reclutadores.
- Sé honesto y objetivo al dar feedback.
- Sé conciso, sin exceder 3 párrafos salvo que se solicite detalle.
- Si una consulta no está relacionada con el CV o la trayectoria profesional,
  indica amablemente que solo puedes brindar información sobre el perfil de Jeffersson Pretell.
"""


# 4. Inicializar Cliente de Hugging Face (DeepSeek-V3)
client = InferenceClient(
    provider="together",  # Usamos el proveedor que indicaste
    api_key=hf_token
)

# --- RUTA DE BIENVENIDA (Para evitar el 404) ---
@app.get("/")
def home():
    return {
        "estado": "ACTIVO",
        "mensaje": "El cerebro de Jeffersson AI está funcionando correctamente 🤖",
        "documentacion": "/docs"  # FastAPI crea docs automáticos aquí
    }


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not hf_token:
        raise HTTPException(status_code=500, detail="Error de configuración del servidor: Falta API Key.")

    try:
        # Preparar los mensajes para el modelo tipo Chat
        messages = [
            {
                "role": "system",
                "content": INFO_JEFFERSSON
            },
            {
                "role": "user",
                "content": request.message
            }
        ]

        # Llamada al modelo
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3", 
            messages=messages, 
            max_tokens=500, # Limita la longitud de la respuesta
            temperature=0.6 # Creatividad moderada (0.0 es robot, 1.0 es poeta loco)
        )

        # Extraer el texto de la respuesta
        response_text = completion.choices[0].message.content
        
        return {"response": response_text}

    except Exception as e:
        print(f"Error generando respuesta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mensaje de inicio
print("Agente Jeffersson (DeepSeek) cargado correctamente.")
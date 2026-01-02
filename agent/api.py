import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- LIBRERÍAS DE IA ---
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. CONFIGURACIÓN DEL TOKEN (TU CLAVE) ---
# He puesto tu token aquí directamente para que funcione YA.
os.environ["HUGGINGFACEHUB_API_TOKEN"] = # LA API KEY DE HG

# --- 2. INFORMACIÓN DE TU PERFIL ---
INFO_JEFFERSSON = """
NOMBRE: Jeffersson Pretell
PERFIL PROFESIONAL:
Estudiante de Economía (Universidad Nacional de Trujillo) con fuerte especialización en Ciencia de Datos, Estadística y Matemáticas Aplicadas.
Su objetivo es convertirse en un Economista-Estadístico-Programador con perfil de Data Scientist Full Stack.

HABILIDADES TÉCNICAS (STACK):
- Lenguajes de Programación: Python (Avanzado), R/RStudio (Avanzado), SQL, JavaScript (Básico).
- Big Data: Hadoop, Spark, PySpark.
- Cloud & Bases de Datos: AWS, SQL Server, PostgreSQL, MongoDB, Databricks.
- Herramientas de Desarrollo: Docker, Git/GitHub, Linux, Visual Studio Code.
- Visualización y Web: Power BI, Streamlit, Flask, HTML5/CSS3.
- Metodologías: Scrum, MLOps, DevOps básico.

EXPERIENCIA Y PROYECTOS DESTACADOS:
1. Web Scraping de Precios Retail:
   - Descripción: Solución a la asimetría de información mediante la extracción y centralización de precios de múltiples tiendas.
   - Tecnologías: Python, Flask, Selenium, BeautifulSoup.

2. App de Predicción Fuga de Clientes (Churn):
   - Descripción: Modelo de Machine Learning utilizando PCA (Análisis de Componentes Principales) y Regresión Logística para predecir el abandono de clientes.
   - Tecnologías: Python, Streamlit, Scikit-learn.

3. Detección de Rostros con OpenCV:
   - Descripción: Script de visión artificial utilizando modelos Haar Cascades para detección facial en tiempo real.
   - Tecnologías: Python, OpenCV.

4. Automatización de WhatsApp:
   - Descripción: Bot para envío masivo y programado de mensajes con fines de marketing.
   - Tecnologías: Python, Selenium.

5. Detección de Fraudes con Tarjetas de Crédito:
   - Descripción: Modelo de clasificación supervisada para identificar transacciones fraudulentas.
   - Tecnologías: Python, Scikit-learn, Pandas.

EDUCACIÓN Y FORMACIÓN:
- Universidad Nacional de Trujillo: Estudiante de Economía (VII Ciclo).
- Datacamp: Data Scientist Career Track.
- GEM: Especialización en Ingeniería de Datos (Julio 2025 - Octubre 2025).
- Udacity & AWS: Nanodegree AI Scientist (Beca AWS AI & ML Scholar).
- Universidad Nacional de Ingeniería (UNI): Fundamentos de Cloud Computing y ML con Python.

INTERESES:
- Inteligencia Artificial Generativa, NLP (Procesamiento de Lenguaje Natural).
- Aplicación de modelos económicos y econometría con tecnología moderna.
- Frase personal: "Conectar modelos económicos y tecnología no es el futuro, es el presente."
"""

# --- 3. INICIALIZACIÓN DE LA APP ---
app = FastAPI(title="Jeffersson AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

rag_chain = None

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- 4. CARGA DEL MODELO RAG ---
@app.on_event("startup")
async def load_model():
    global rag_chain
    print("⏳ Iniciando carga del agente...")

    # A. Vector Store (Embeddings Locales - Gratis)
    docs = [Document(page_content=INFO_JEFFERSSON)]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    # Usamos embeddings ligeros y rápidos (se descargan una sola vez)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    
    # B. LLM (Mistral-7B vía Hugging Face API)
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_new_tokens=512,  # <--- CORREGIDO (Ya no usamos max_length)
        temperature=0.3,
        huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"]
    )
    
    # C. Prompt del Sistema
    system_prompt = (
        "Eres el asistente virtual IA del portafolio de Jeffersson Pretell. "
        "Responde preguntas sobre sus proyectos, habilidades y educación basándote en el contexto. "
        "Responde siempre en ESPAÑOL de manera profesional y amable. "
        "Si no sabes la respuesta, di 'No tengo información sobre eso'. "
        "\n\nContexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # D. Cadena LCEL
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✅ Agente Jeffersson AI cargado correctamente.")

# --- 5. ENDPOINT ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not rag_chain:
        raise HTTPException(status_code=503, detail="El modelo se está cargando...")
    
    try:
        response_text = rag_chain.invoke(request.message)
        return {"response": response_text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
import streamlit as st
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document

# --- 1. CONFIGURACIÓN DE TU PERFIL (BASE DE CONOCIMIENTO) ---
# Aquí está la información que la IA usará para responder.
INFO_JEFFERSSON = """
NOMBRE: Jeffersson Pretell
PERFIL: Estudiante de Economía (UNTRM) con especialización en Ciencia de Datos, Estadística y Matemáticas Aplicadas.
OBJETIVO: Convertirse en Economista-Estadístico-Programador y Data Scientist Full Stack.

HABILIDADES TÉCNICAS (STACK):
- Lenguajes: Python (avanzado), R/RStudio (avanzado), SQL.
- Big Data: Hadoop, Spark, PySpark.
- Cloud & DB: AWS, SQL Server, PostgreSQL, MongoDB, Databricks.
- Herramientas: Docker, Git/GitHub, Linux, Power BI.
- Web: Streamlit, Flask (Básico), HTML/CSS.

EXPERIENCIA Y PROYECTOS DESTACADOS:
1. Web Scraping Retail: Comparador de precios usando Python (Selenium/BeautifulSoup) para reducir asimetría de información.
2. Predicción de Fuga de Clientes (Churn): Modelo de Machine Learning usando PCA y Regresión Logística desplegado en Streamlit.
3. Detección de Rostros: Script de visión artificial con OpenCV.
4. Automatización WhatsApp: Bot de envío masivo para marketing usando Selenium.
5. Detección de Fraudes: Modelo supervisado para tarjetas de crédito con Scikit-learn.

EDUCACIÓN:
- Universidad Nacional de Trujillo (Economía, VII Ciclo).
- Datacamp (Data Scientist Career Track).
- GEM (Especialización Ingeniería de Datos).
- Udacity & AWS (Nanodegree AI Scientist - Beca).
- Universidad Nacional de Ingeniería (Cloud Computing y ML).

INTERESES:
- Inteligencia Artificial Generativa, NLP, Modelos Económicos, Econometría.
- "Conectar modelos económicos y tecnología no es el futuro, es el presente".
"""

# --- 2. CONFIGURACIÓN DE LA APP STREAMLIT ---
st.set_page_config(page_title="Jeffersson AI", layout="wide")

# Ocultar elementos propios de Streamlit para que se vea limpio en el iframe
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp { padding-top: 0; }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🤖 Chat con Jeffersson AI")
st.markdown("Soy un agente entrenado con el perfil profesional de Jeffersson. ¡Pregúntame lo que quieras!")

# --- 3. GESTIÓN DE API KEY ---
# Para pruebas locales, pedimos la clave si no está en variables de entorno
if "OPENAI_API_KEY" not in os.environ:
    api_key = st.text_input("🔑 Ingresa tu OpenAI API Key para probar:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.info("Por favor ingresa una API Key de OpenAI para continuar.")
        st.stop()

# --- 4. LÓGICA RAG (SOLO SE EJECUTA UNA VEZ) ---
@st.cache_resource
def setup_rag_chain():
    # A. Crear Documento
    docs = [Document(page_content=INFO_JEFFERSSON)]
    
    # B. Dividir texto (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    # C. Vector Store (Base de datos en memoria)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    
    # D. Modelo LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # E. Prompt del Sistema
    system_prompt = (
        "Eres el asistente virtual del portafolio de Jeffersson Pretell. "
        "Responde preguntas sobre su experiencia y habilidades basándote ESTRICTAMENTE "
        "en el contexto proporcionado. "
        "Sé profesional, conciso y amable. Si no sabes algo, di que no tienes esa información. "
        "Responde siempre en primera persona como si fueras su asistente digital. "
        "\n\n"
        "Contexto: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain

rag_chain = setup_rag_chain()

# --- 5. INTERFAZ DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de usuario
if prompt := st.chat_input("Ej: ¿Qué experiencia tiene Jeffersson con Python?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = rag_chain.invoke({"input": prompt})
            answer = response["answer"]
            st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
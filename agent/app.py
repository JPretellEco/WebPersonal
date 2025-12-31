import streamlit as st
import os
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Jeffersson AI", layout="wide")
st.title("🤖 Chat con Jeffersson AI")

INFO_JEFFERSSON = """
NOMBRE: Jeffersson Pretell
PERFIL: Estudiante de Economía con especialización en Ciencia de Datos y Estadística.
OBJETIVO: Convertirse en Economista-Estadístico-Programador y Data Scientist Full Stack.
HABILIDADES: Python, R, SQL, Spark, Cloud, ML, NLP.
"""

# --- API KEY ---
if "OPENAI_API_KEY" not in os.environ:
    api_key = st.text_input("🔑 Ingresa tu OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.stop()

client = OpenAI()

# --- HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- INPUT ---
if user_input := st.chat_input("Pregunta sobre Jeffersson"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = f"""
Eres el asistente virtual del portafolio de Jeffersson Pretell.
Responde SOLO con la información proporcionada.
Si no está en el contexto, di que no lo sabes.

CONTEXTO:
{INFO_JEFFERSSON}

PREGUNTA:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# 📊 Portafolio Data Scientist - Jeffersson Pretell

![Estado](https://img.shields.io/badge/Estado-En_Desarrollo-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![AI Model](https://img.shields.io/badge/AI-DeepSeek_V3-purple)

Bienvenido al repositorio de mi portafolio profesional. Este proyecto combina un diseño web moderno e interactivo con un **Agente de IA personalizado** capaz de responder preguntas sobre mi perfil profesional, habilidades y experiencia en tiempo real.

---

## 🚀 Características Principales

### 🎨 Frontend (Web)
- **Diseño Responsivo:** Adaptable a móviles y escritorio.
- **Interactividad:** Fondo de partículas (`particles.js`), carruseles y efectos de escritura.
- **Filtros Dinámicos:** Clasificación de proyectos por categoría (Analytics, AI, Dev, etc.).
- **Persistencia de Sesión:** El chat mantiene la conversación activa aunque navegues entre páginas.

### 🤖 Backend (AI Agent)
- **Arquitectura:** API REST construida con **FastAPI**.
- **Cerebro:** Integración con **DeepSeek-V3** vía Hugging Face Inference API.
- **RAG Ligero:** El modelo recibe un contexto estructurado (System Prompt) con mi perfil profesional completo para generar respuestas precisas y alucinaciones mínimas.
- **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`).

---

## 🛠️ Tecnologías Utilizadas

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla).
* **Backend:** Python, FastAPI, Uvicorn.
* **IA / LLM:** Hugging Face Hub (`InferenceClient`), DeepSeek-V3.
* **Librerías Python:** `pydantic`, `python-dotenv`.

---

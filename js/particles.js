document.addEventListener("DOMContentLoaded", () => {
    
    /* =========================================
       1. LÓGICA DEL CHATBOT (FASTAPI / BACKEND)
       ========================================= */
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatWindow = document.getElementById('chatbot-window');
    const chatClose = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // URL de tu Backend FastAPI (Local)
    // NOTA: Cuando subas esto a internet, cambia esta URL por la de producción.
    const API_URL = "http://127.0.0.1:8000/chat"; 

    // A. Abrir/Cerrar Ventana
    if (chatToggle && chatWindow) {
        chatToggle.addEventListener('click', () => {
            chatWindow.classList.toggle('hidden');
            // Dar foco al input si se abre
            if (!chatWindow.classList.contains('hidden') && chatInput) {
                setTimeout(() => chatInput.focus(), 100);
            }
        });
    }

    if (chatClose && chatWindow) {
        chatClose.addEventListener('click', () => {
            chatWindow.classList.add('hidden');
        });
    }

    // B. Función para agregar mensajes al DOM (HTML)
    function addMessage(text, sender) {
        if (!chatMessages) return;

        const div = document.createElement('div');
        div.classList.add('message');
        // Define clase según quién envía: 'user-message' o 'bot-message'
        div.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        div.textContent = text;
        
        chatMessages.appendChild(div);
        // Auto-scroll al final
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // C. Función para enviar mensaje a la API
    async function handleChatSubmit(e) {
        e.preventDefault();
        
        if (!chatInput) return;
        
        const message = chatInput.value.trim();
        if (!message) return;

        // 1. Mostrar mensaje del usuario
        addMessage(message, 'user');
        chatInput.value = '';

        // 2. Mostrar indicador "Escribiendo..."
        const loadingDiv = document.createElement('div');
        loadingDiv.textContent = "Analizando perfil...";
        loadingDiv.classList.add('typing-indicator'); // Asegúrate de tener este estilo en CSS
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            // 3. Petición POST a FastAPI
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) throw new Error("Error en la respuesta del servidor");

            const data = await response.json();
            
            // 4. Remover loading y mostrar respuesta del Bot
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }
            addMessage(data.response, 'bot');

        } catch (error) {
            console.error("Error:", error);
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }
            addMessage("Lo siento, no puedo conectar con el cerebro del agente en este momento. Asegúrate de que 'api.py' esté ejecutándose.", 'bot');
        }
    }

    // Listener del formulario
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }


    /* =========================================
       2. PARTICLES.JS (FONDO)
       ========================================= */
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS("particles-js", {
            "particles": {
                "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#38bdf8" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5, "random": false },
                "size": { "value": 3, "random": true },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#38bdf8",
                    "opacity": 0.4,
                    "width": 1
                },
                "move": { "enable": true, "speed": 2 }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": { "enable": true, "mode": "repulse" },
                    "onclick": { "enable": true, "mode": "push" }
                }
            },
            "retina_detect": true
        });
    }

    /* =========================================
       3. LÓGICA DEL CARRUSEL
       ========================================= */
    const track = document.querySelector('.carousel-track');
    if (track) {
        const slides = Array.from(track.children);
        const nextButton = document.getElementById('nextBtn');
        const prevButton = document.getElementById('prevBtn');
        let currentIndex = 0;

        // Función para mover slides
        const moveToSlide = (index) => {
            slides.forEach(slide => slide.classList.remove('current-slide'));
            slides[index].classList.add('current-slide');
        };

        // Click derecho
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                currentIndex = (currentIndex + 1) % slides.length; 
                moveToSlide(currentIndex);
            });
        }

        // Click izquierdo
        if (prevButton) {
            prevButton.addEventListener('click', () => {
                currentIndex = (currentIndex - 1 + slides.length) % slides.length;
                moveToSlide(currentIndex);
            });
        }
    }
});

/* =========================================
   4. SISTEMA DE MODALES (GLOBAL)
   ========================================= */

window.openModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; 
    }
};

window.closeModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; 
        
        const videos = modal.querySelectorAll('video');
        videos.forEach(v => v.pause());
    }
};

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
        document.body.style.overflow = 'auto';
        const videos = event.target.querySelectorAll('video');
        videos.forEach(v => v.pause());
    }
};
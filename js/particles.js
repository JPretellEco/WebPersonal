document.addEventListener("DOMContentLoaded", () => {
    
    /* =========================================
       1. LÓGICA DEL CHATBOT (CON MEMORIA / PERSISTENCIA)
       ========================================= */
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatWindow = document.getElementById('chatbot-window');
    const chatClose = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // URL de tu Backend FastAPI (Local)
    const API_URL = "http://127.0.0.1:8000/chat"; 

    // --- A. CARGAR ESTADO AL INICIAR (Memoria) ---
    loadChatState();

    // --- B. ABRIR / CERRAR CHAT ---
    if (chatToggle && chatWindow) {
        chatToggle.addEventListener('click', () => {
            chatWindow.classList.remove('hidden'); // Forzamos mostrar
            // Dar foco al input
            if (chatInput) setTimeout(() => chatInput.focus(), 100);
            saveChatState(); // Guardamos que está abierto
        });
    }

    if (chatClose && chatWindow) {
        chatClose.addEventListener('click', () => {
            chatWindow.classList.add('hidden'); // Ocultamos
            saveChatState(); // Guardamos que está cerrado
        });
    }

    // --- C. PROCESAR EL ENVÍO DE MENSAJES ---
    async function handleChatSubmit(e) {
        e.preventDefault();
        
        if (!chatInput) return;
        const message = chatInput.value.trim();
        if (!message) return;

        // 1. Mostrar mensaje del usuario y guardar estado
        addMessageToUI(message, 'user');
        chatInput.value = '';

        // 2. Mostrar indicador "Escribiendo..." (No se guarda en historial)
        const loadingDiv = document.createElement('div');
        loadingDiv.textContent = "Analizando perfil...";
        loadingDiv.classList.add('message', 'bot-message', 'typing-indicator'); 
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
            addMessageToUI(data.response, 'bot');

        } catch (error) {
            console.error("Error:", error);
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }
            addMessageToUI("Lo siento, no puedo conectar con el cerebro del agente en este momento. Asegúrate de que 'agente.py' esté ejecutándose.", 'bot');
        }
    }

    // Listener del formulario
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }

    // --- D. FUNCIONES DE UTILIDAD Y MEMORIA ---

    // Agrega mensaje al HTML y guarda en SessionStorage
    function addMessageToUI(text, sender) {
        if (!chatMessages) return;

        const div = document.createElement('div');
        div.classList.add('message');
        div.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        div.textContent = text;
        
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // ¡IMPORTANTE! Guardar cada vez que se añade un mensaje válido
        saveChatState();
    }

    function saveChatState() {
        if (!chatWindow) return;

        // 1. Guardar si está visible o no
        const isOpen = !chatWindow.classList.contains('hidden');
        sessionStorage.setItem('chat_isOpen', isOpen);

        // 2. Guardar el historial de mensajes
        const messages = [];
        // Seleccionamos solo los mensajes reales (ignorando el 'typing-indicator')
        // Usamos querySelectorAll dentro de chatMessages para obtener el orden correcto
        const messageElements = chatMessages.querySelectorAll('.message:not(.typing-indicator)');
        
        messageElements.forEach(msg => {
            const isUser = msg.classList.contains('user-message');
            messages.push({
                text: msg.textContent,
                sender: isUser ? 'user' : 'bot'
            });
        });
        sessionStorage.setItem('chat_history', JSON.stringify(messages));
    }

    function loadChatState() {
        if (!chatWindow) return;

        // 1. Recuperar estado Abierto/Cerrado
        const isOpen = sessionStorage.getItem('chat_isOpen') === 'true';
        if (isOpen) {
            chatWindow.classList.remove('hidden');
        } else {
            chatWindow.classList.add('hidden');
        }

        // 2. Recuperar Historial
        const historyData = sessionStorage.getItem('chat_history');
        if (historyData) {
            const history = JSON.parse(historyData);
            
            // Solo restauramos si hay historial previo
            if (history.length > 0) {
                chatMessages.innerHTML = ''; // Limpiamos mensaje por defecto si hay historial
                history.forEach(msg => {
                    const div = document.createElement('div');
                    div.classList.add('message');
                    div.classList.add(msg.sender === 'user' ? 'user-message' : 'bot-message');
                    div.textContent = msg.text;
                    chatMessages.appendChild(div);
                });
                // Scroll al final al cargar
                setTimeout(() => {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 100);
            }
        }
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

    /* =========================================
       EFECTO MÁQUINA DE ESCRIBIR (QUOTE)
       ========================================= */
    
    const line1 = document.querySelector('.quote-section .line1');
    const line2 = document.querySelector('.quote-section .line2');

    // Función genérica para escribir texto
    function typeWriter(element, text, speed, callback) {
        let i = 0;
        element.innerHTML = ""; // Limpiar texto inicial
        element.classList.add('typing'); // Añadir cursor

        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                element.classList.remove('typing'); // Quitar cursor al terminar
                if (callback) callback(); // Ejecutar siguiente acción
            }
        }
        type();
    }

    // Ejecutar solo si existen los elementos
    if (line1 && line2) {
        const text1 = line1.innerText; 
        const text2 = line2.innerText; 

        // Borramos el contenido inicial para que no se vea duplicado al cargar
        line1.innerHTML = "&nbsp;"; 
        line2.innerHTML = "&nbsp;";

        // Iniciamos la secuencia (Velocidad: 40ms por letra)
        setTimeout(() => {
            line1.innerHTML = ""; 
            typeWriter(line1, text1, 80, () => {
                // Callback: Cuando termina la línea 1, empieza la 2
                line2.innerHTML = ""; 
                typeWriter(line2, text2, 40);
            });
        }, 500);
    }

    /* =========================================
       FILTRO DE PROYECTOS
       ========================================= */
    const filterItems = document.querySelectorAll('.filter-item');
    const projectCards = document.querySelectorAll('.project-card');

    if (filterItems.length > 0) {
        filterItems.forEach(item => {
            item.addEventListener('click', () => {
                // 1. Quitar clase active de todos
                filterItems.forEach(fi => fi.classList.remove('active'));
                
                // 2. Activar el clicado
                item.classList.add('active');

                // 3. Obtener valor del filtro
                const filterValue = item.getAttribute('data-filter');

                // 4. Mostrar/Ocultar tarjetas
                projectCards.forEach(card => {
                    const categories = card.getAttribute('data-category');
                    
                    if (filterValue === 'all' || categories.includes(filterValue)) {
                        card.classList.remove('hidden');
                        // Pequeña animación de entrada
                        card.style.opacity = '0';
                        setTimeout(() => card.style.opacity = '1', 50);
                    } else {
                        card.classList.add('hidden');
                    }
                });
            });
        });
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
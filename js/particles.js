document.addEventListener("DOMContentLoaded", () => {
    
    /* --- LÓGICA DEL CHATBOT --- */
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatWindow = document.getElementById('chatbot-window');
    const chatClose = document.getElementById('chatbot-close');
    const chatFrame = document.getElementById('chat-frame');

    // URL de tu aplicación Streamlit (Cuando la despliegues)
    // Por ahora usamos una de prueba o blank
   const APP_URL = "http://localhost:8501/?embed=true";

    // Abrir/Cerrar Chat
    chatToggle.addEventListener('click', () => {
        const isHidden = chatWindow.classList.contains('hidden');
        
        if (isHidden) {
            chatWindow.classList.remove('hidden');
            // Cargar el iframe solo cuando se abre por primera vez para ahorrar recursos
            if (chatFrame.src === "about:blank") {
                // AQUÍ PONDRÁS LA URL REAL DE TU AGENTE
                // chatFrame.src = APP_URL; 
                console.log("Cargando agente...");
            }
        } else {
            chatWindow.classList.add('hidden');
        }
    });

    // Cerrar con la X
    chatClose.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
    });

    /* --- PARTICLES.JS (FONDO) --- */
    /* Asegúrate de que particles.js esté cargado antes de ejecutar esto */
    if (typeof particlesJS !== 'undefined') {
        particlesJS("particles-js", {
            "particles": {
                "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#38bdf8" }, /* Color Azul Cyan */
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
});


/* --- LÓGICA DEL CARRUSEL (Solo si existe en la página) --- */
    const track = document.querySelector('.carousel-track');
    if (track) {
        const slides = Array.from(track.children);
        const nextButton = document.getElementById('nextBtn');
        const prevButton = document.getElementById('prevBtn');
        let currentIndex = 0;

        // Función para mover slides
        const moveToSlide = (index) => {
            // Ocultar todos
            slides.forEach(slide => slide.classList.remove('current-slide'));
            // Mostrar el actual
            slides[index].classList.add('current-slide');
        };

        // Click derecho
        nextButton.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % slides.length; // Loop infinito
            moveToSlide(currentIndex);
        });

        // Click izquierdo
        prevButton.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            moveToSlide(currentIndex);
        });
    }


/* --- SISTEMA DE MODALES --- */

// Función global para abrir modales
window.openModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Evita scroll de fondo
    }
};

// Función global para cerrar modales
window.closeModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Restaura scroll
        
        // Si hay videos en el modal, pausarlos al cerrar
        const videos = modal.querySelectorAll('video');
        videos.forEach(v => v.pause());
    }
};

// Cerrar modal si se hace clic fuera del contenido
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
        document.body.style.overflow = 'auto';
        const videos = event.target.querySelectorAll('video');
        videos.forEach(v => v.pause());
    }
};
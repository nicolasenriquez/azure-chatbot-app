class ChatbotInterface {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000'; // Cambiar por la URL de tu backend
        this.sessionId = this.generateSessionId();
        this.messages = [];
        this.isTyping = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAPIHealth();
        this.setupPWA();
    }

    generateSessionId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `session_${timestamp}_${random}`;
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.getElementById('chatInterface').classList.contains('active')) {
                document.getElementById('chatInput').value = '';
            }
        });

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const chatInterface = document.getElementById('chatInterface');
                    if (chatInterface.classList.contains('active')) {
                        setTimeout(() => {
                            document.getElementById('chatInput').focus();
                        }, 100);
                    }
                }
            });
        });

        observer.observe(document.getElementById('chatInterface'), {
            attributes: true,
            attributeFilter: ['class']
        });
    }

    async checkAPIHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/health`);
            if (response.ok) {
                console.log('API conectada correctamente');
            } else {
                console.warn('API no disponible, usando modo demo');
            }
        } catch (error) {
            console.warn('No se pudo conectar con la API, usando modo demo');
        }
    }

    setupPWA() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(console.error);
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        const message = input.value.trim();

        if (!message || this.isTyping) return;

        input.value = '';
        sendButton.disabled = true;
        this.autoResize(input);

        this.addMessage(message, 'user');
        this.showTypingIndicator();

        try {
            const response = await this.callAPI(message);
            this.hideTypingIndicator();
            this.addMessage(response, 'ai');
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Lo siento, hubo un error al procesar tu mensaje. Por favor, inténtalo de nuevo.', 'ai');
            console.error('Error en la API:', error);
        }

        sendButton.disabled = false;
        input.focus();
    }

    async callAPI(message) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    message: message
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.response || 'Respuesta recibida';
        } catch (error) {
            await this.delay(1000 + Math.random() * 2000);
            return this.generateDemoResponse(message);
        }
    }

    generateDemoResponse(message) {
        const responses = [
            "Gracias por tu mensaje. Como asistente de IA, estoy aquí para ayudarte con cualquier pregunta o tarea que tengas.",
            "Entiendo tu consulta. Permíteme procesar esta información y ofrecerte la mejor respuesta posible.",
            "Es una pregunta interesante. Basándome en mi conocimiento, puedo ayudarte a explorar diferentes perspectivas sobre este tema.",
            "Me parece una consulta muy relevante. Te ayudo a analizarla paso a paso para encontrar la mejor solución.",
            "Perfecto, puedo asistirte con esto. Déjame compartir contigo información útil y práctica sobre tu consulta."
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    addMessage(text, type) {
        const messagesContainer = document.getElementById('chatMessages');
        const emptyState = messagesContainer.querySelector('.empty-state');
        
        if (emptyState) {
            emptyState.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        
        const currentTime = new Date().toLocaleTimeString('es-ES', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        const content = marked.parse(text);

        messageElement.innerHTML = `
            <div class="message-content">
                ${content}
                <div class="message-time">${currentTime}</div>
            </div>
        `;

        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.messages.push({
            text: text,
            type: type,
            timestamp: new Date()
        });
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.id = 'typingIndicator';
        
        typingIndicator.innerHTML = `
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <span>AI está escribiendo...</span>
        `;

        messagesContainer.appendChild(typingIndicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        this.isTyping = true;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }

    autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

let chatbot;

function startChat() {
    document.getElementById('welcomeScreen').classList.add('hidden');
    document.getElementById('chatInterface').classList.add('active');
    
    if (!chatbot) {
        chatbot = new ChatbotInterface();
    }
}

function goBack() {
    document.getElementById('chatInterface').classList.remove('active');
    document.getElementById('welcomeScreen').classList.remove('hidden');
}

function sendMessage() {
    if (chatbot) {
        chatbot.sendMessage();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(textarea) {
    if (chatbot) {
        chatbot.autoResize(textarea);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Chatbot Interface cargada correctamente');
    
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    link.as = 'style';
    document.head.appendChild(link);
});
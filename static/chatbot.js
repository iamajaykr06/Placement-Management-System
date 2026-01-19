// Chatbot functionality for Placement Management System

class PlacementChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <div id="chatbot-container" class="chatbot-container">
                <div id="chatbot-header" class="chatbot-header">
                    <div class="chatbot-header-content">
                        <div class="chatbot-avatar">🤖</div>
                        <div>
                            <h3>Placement Assistant</h3>
                            <p>How can I help you?</p>
                        </div>
                    </div>
                    <button id="chatbot-minimize" class="chatbot-minimize">−</button>
                </div>
                <div id="chatbot-messages" class="chatbot-messages"></div>
                <div id="chatbot-input-container" class="chatbot-input-container">
                    <input 
                        type="text" 
                        id="chatbot-input" 
                        class="chatbot-input" 
                        placeholder="Type your message..."
                        autocomplete="off"
                    >
                    <button id="chatbot-send" class="chatbot-send-btn">➤</button>
                </div>
            </div>
            <button id="chatbot-toggle" class="chatbot-toggle">
                <span class="chatbot-icon">💬</span>
                <span class="chatbot-badge">1</span>
            </button>
        `;
        
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        const toggle = document.getElementById('chatbot-toggle');
        const minimize = document.getElementById('chatbot-minimize');
        const sendBtn = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');

        toggle.addEventListener('click', () => this.toggleChatbot());
        minimize.addEventListener('click', () => this.toggleChatbot());
        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    toggleChatbot() {
        const container = document.getElementById('chatbot-container');
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            container.classList.add('chatbot-open');
            document.getElementById('chatbot-input').focus();
        } else {
            container.classList.remove('chatbot-open');
        }
    }

    addWelcomeMessage() {
        const welcomeMessage = {
            text: "Hello! 👋 I'm your Placement Assistant. I can help you with:\n\n• Registration process\n• Job applications\n• Profile setup\n• General questions\n\nWhat would you like to know?",
            sender: 'bot',
            timestamp: new Date()
        };
        this.addMessage(welcomeMessage);
    }

    addMessage(message) {
        this.messages.push(message);
        this.renderMessage(message);
    }

    renderMessage(message) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message chatbot-message-${message.sender}`;
        
        const time = new Date(message.timestamp).toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="chatbot-message-content">
                ${message.sender === 'bot' ? '<div class="chatbot-avatar-small">🤖</div>' : ''}
                <div class="chatbot-message-text">
                    ${this.formatMessage(message.text)}
                    <span class="chatbot-message-time">${time}</span>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatMessage(text) {
        // Convert newlines to <br>
        return text.replace(/\n/g, '<br>');
    }

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const userMessage = input.value.trim();
        
        if (!userMessage) return;
        
        // Add user message
        this.addMessage({
            text: userMessage,
            sender: 'user',
            timestamp: new Date()
        });
        
        input.value = '';
        
        // Simulate typing delay
        setTimeout(() => {
            const botResponse = this.getBotResponse(userMessage);
            this.addMessage({
                text: botResponse,
                sender: 'bot',
                timestamp: new Date()
            });
        }, 500);
    }

    getBotResponse(userMessage) {
        const message = userMessage.toLowerCase();
        
        // Registration questions
        if (message.includes('register') || message.includes('sign up') || message.includes('signup')) {
            return "To register:\n\n👨‍🎓 As Student:\n1. Click 'Register as Student'\n2. Fill in username, email, and password\n3. Complete your profile after login\n\n🏢 As Company:\n1. Click 'Register as Company'\n2. Fill in company details\n3. Start posting jobs!\n\nNeed help with registration?";
        }
        
        // Login questions
        if (message.includes('login') || message.includes('sign in') || message.includes('signin')) {
            return "To login:\n\n1. Click the 'Login' button\n2. Enter your email and password\n3. You'll be redirected to your dashboard\n\nForgot your password? Contact support for assistance.";
        }
        
        // Job application questions
        if (message.includes('apply') || message.includes('job') || message.includes('application')) {
            return "To apply for jobs:\n\n1. Login to your student account\n2. Browse available jobs\n3. Click 'Apply' on any job\n4. Track your applications in 'My Applications'\n\nMake sure your profile is complete for better chances!";
        }
        
        // Profile questions
        if (message.includes('profile') || message.includes('update profile')) {
            return "To update your profile:\n\n👨‍🎓 Students:\n• Go to 'Profile' from dashboard\n• Add your skills, bio, and links\n• Complete all fields for better visibility\n\n🏢 Companies:\n• Go to 'Company Profile'\n• Add company details and logo\n• Keep information up to date";
        }
        
        // Company posting jobs
        if (message.includes('post job') || message.includes('posting') || message.includes('company')) {
            return "To post a job:\n\n1. Login as a company\n2. Complete your company profile\n3. Go to 'Post Job'\n4. Fill in job details (title, description, salary, etc.)\n5. Set application deadline\n6. Publish!\n\nYou can manage applicants from the same page.";
        }
        
        // General help
        if (message.includes('help') || message.includes('how') || message.includes('what')) {
            return "I can help you with:\n\n✅ Registration process\n✅ Login issues\n✅ Job applications\n✅ Profile management\n✅ Posting jobs\n✅ General questions\n\nWhat specific help do you need?";
        }
        
        // Greetings
        if (message.includes('hi') || message.includes('hello') || message.includes('hey')) {
            return "Hello! 👋 Welcome to Placement Management System. How can I assist you today?";
        }
        
        // Contact/Support
        if (message.includes('contact') || message.includes('support') || message.includes('help')) {
            return "For support:\n\n📧 Email: support@placement.com\n📞 Phone: +1-234-567-8900\n💬 Chat: Available 24/7\n\nIs there something specific I can help with?";
        }
        
        // Default response
        const responses = [
            "I'm here to help! Could you be more specific about what you need?",
            "That's a great question! Try asking about registration, jobs, or profiles.",
            "I can help with registration, job applications, and profile setup. What do you need?",
            "Let me help you! You can ask about:\n• How to register\n• How to apply for jobs\n• How to update your profile\n• How to post jobs"
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
}

// Initialize chatbot when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new PlacementChatbot();
    });
} else {
    new PlacementChatbot();
}

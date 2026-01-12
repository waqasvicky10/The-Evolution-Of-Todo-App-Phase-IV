/**
 * Todo Chat UI - JavaScript
 *
 * This file handles:
 * - Authentication
 * - Message sending/receiving
 * - Conversation history loading
 * - UI updates and interactions
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000/api';
const AUTH_TOKEN_KEY = 'todo_chat_token';
const USER_NAME_KEY = 'todo_chat_user';

// State
let authToken = null;
let isProcessing = false;

// DOM Elements
const loginScreen = document.getElementById('login-screen');
const chatContainer = document.getElementById('chat-container');
const loginForm = document.getElementById('login-form');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const voiceButton = document.getElementById('voice-button');
const messagesContainer = document.getElementById('messages-container');
const userNameDisplay = document.getElementById('user-name');
const logoutBtn = document.getElementById('logout-btn');
const statusText = document.getElementById('status-text');
const sendIcon = document.getElementById('send-icon');
const loadingSpinner = document.getElementById('loading-spinner');

// Voice Recognition
let recognition = null;
let isRecording = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupEventListeners();
    setupLanguageMenu();
});

/**
 * Setup language menu logic
 */
function setupLanguageMenu() {
    const langBtn = document.getElementById('lang-btn');
    const langMenu = document.getElementById('lang-menu');
    const langOptions = document.querySelectorAll('.lang-option');
    const currentLangIcon = document.getElementById('current-lang-icon');

    // Load stored language
    const storedLang = localStorage.getItem('todo_chat_lang') || 'en';
    updateLanguageUI(storedLang);

    // Toggle menu
    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        langMenu.classList.toggle('show');
    });

    // Handle option click
    langOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            const selectedLang = e.currentTarget.dataset.lang;
            localStorage.setItem('todo_chat_lang', selectedLang);

            updateLanguageUI(selectedLang);

            // Update recognition if active
            if (recognition) {
                recognition.lang = selectedLang === 'ur' ? 'ur-PK' : 'en-US';
            }

            langMenu.classList.remove('show');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!langMenu.contains(e.target) && !langBtn.contains(e.target)) {
            langMenu.classList.remove('show');
        }
    });

    function updateLanguageUI(lang) {
        // Update icon
        currentLangIcon.textContent = lang === 'ur' ? '🇵🇰' : '🇺🇸';

        // Update active class
        langOptions.forEach(opt => {
            if (opt.dataset.lang === lang) {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });
    }
}

/**
 * Check if user is already authenticated
 */
function checkAuthentication() {
    const savedToken = localStorage.getItem(AUTH_TOKEN_KEY);
    const savedUsername = localStorage.getItem(USER_NAME_KEY);

    if (savedToken && savedUsername) {
        authToken = savedToken;
        login(savedUsername);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Login form
    loginForm.addEventListener('submit', handleLogin);

    // Message form
    messageForm.addEventListener('submit', handleSendMessage);

    // Logout button
    logoutBtn.addEventListener('click', handleLogout);

    // Voice button
    if (voiceButton) {
        voiceButton.addEventListener('click', handleVoiceInput);
    }

    // Enter key in message input
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(e);
        }
    });

    // Initialize voice recognition
    initVoiceRecognition();
}

/**
 * Handle login form submission
 */
async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showError('Please enter username and password');
        return;
    }

    // For demo purposes, we'll use a test token
    // In production, this would call an authentication endpoint
    authToken = 'test_token';
    localStorage.setItem(AUTH_TOKEN_KEY, authToken);
    localStorage.setItem(USER_NAME_KEY, username);

    login(username);
}

/**
 * Perform login (show chat, load history)
 */
async function login(username) {
    // Update UI
    loginScreen.style.display = 'none';
    chatContainer.style.display = 'flex';
    userNameDisplay.textContent = username;
    messageInput.disabled = false;
    sendButton.disabled = false;
    enableVoiceButton();

    // Load conversation history
    await loadConversationHistory();

    // Focus message input
    messageInput.focus();

    setStatus('Ready');
}

/**
 * Handle logout
 */
function handleLogout() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_NAME_KEY);
    authToken = null;

    // Clear messages
    const messages = messagesContainer.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());

    // Show login screen
    chatContainer.style.display = 'none';
    loginScreen.style.display = 'flex';

    // Reset form
    loginForm.reset();
}

/**
 * Load conversation history from API
 */
async function loadConversationHistory() {
    try {
        setStatus('Loading history...');

        const response = await fetch(`${API_BASE_URL}/chat/history?limit=50`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load history');
        }

        const data = await response.json();

        // Display messages
        if (data.messages && data.messages.length > 0) {
            // Remove welcome message
            const welcomeMsg = messagesContainer.querySelector('.welcome-message');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }

            data.messages.forEach(msg => {
                appendMessage(msg.role, msg.content, msg.timestamp, false);
            });

            scrollToBottom();
        }

        setStatus('Ready');
    } catch (error) {
        console.error('Error loading history:', error);
        setStatus('Error loading history');
    }
}

/**
 * Handle send message
 */
async function handleSendMessage(e) {
    e.preventDefault();

    const message = messageInput.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // Disable input while processing
    isProcessing = true;
    messageInput.disabled = true;
    sendButton.disabled = true;
    showLoading(true);
    setStatus('Sending...');

    try {
        // Display user message immediately
        const timestamp = new Date().toISOString();
        appendMessage('user', message, timestamp);
        messageInput.value = '';
        scrollToBottom();

        // Send to API
        setStatus('AI is thinking...');
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleLogout();
                showError('Session expired. Please log in again.');
                return;
            }
            throw new Error('Failed to send message');
        }

        const data = await response.json();

        // Display assistant response
        appendMessage('assistant', data.response, data.timestamp, true, data.tool_calls);
        scrollToBottom();

        setStatus('Ready');
    } catch (error) {
        console.error('Error sending message:', error);
        showError('Failed to send message. Please try again.');
        setStatus('Error');
    } finally {
        // Re-enable input
        isProcessing = false;
        messageInput.disabled = false;
        sendButton.disabled = false;
        showLoading(false);
        messageInput.focus();
    }
}

/**
 * Append a message to the chat
 */
function appendMessage(role, content, timestamp, animate = true, toolCalls = []) {
    // Remove welcome message if it exists
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'message-timestamp';
    timestampDiv.textContent = formatTimestamp(timestamp);

    contentDiv.appendChild(bubble);
    contentDiv.appendChild(timestampDiv);

    // Add tool call indicators if present
    if (toolCalls && toolCalls.length > 0) {
        const toolCallsDiv = document.createElement('div');
        toolCallsDiv.className = 'tool-calls';
        toolCallsDiv.innerHTML = '<strong>🛠️ Actions:</strong>';

        toolCalls.forEach(tc => {
            const toolItem = document.createElement('div');
            toolItem.className = 'tool-call-item';
            toolItem.textContent = `✓ ${tc.tool_name}`;
            toolCallsDiv.appendChild(toolItem);
        });

        contentDiv.appendChild(toolCallsDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    messagesContainer.appendChild(messageDiv);

    if (animate) {
        setTimeout(() => scrollToBottom(), 100);
    }
}

/**
 * Format timestamp for display
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();

    const isToday = date.toDateString() === now.toDateString();

    if (isToday) {
        return date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    } else {
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
    }
}

/**
 * Scroll to bottom of messages
 */
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Show/hide loading spinner
 */
function showLoading(show) {
    sendIcon.style.display = show ? 'none' : 'inline';
    loadingSpinner.style.display = show ? 'inline' : 'none';
}

/**
 * Set status text
 */
function setStatus(text) {
    statusText.textContent = text;
}

/**
 * Show error message
 */
function showError(message) {
    const errorToast = document.getElementById('error-toast');
    const errorMessage = document.getElementById('error-message');

    errorMessage.textContent = message;
    errorToast.style.display = 'flex';

    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    const errorToast = document.getElementById('error-toast');
    errorToast.style.display = 'none';
}

/**
 * Initialize voice recognition
 */
function initVoiceRecognition() {
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.warn('Speech recognition not supported in this browser');
        // if (voiceButton) {
        //     voiceButton.style.display = 'none';
        //     voiceButton.title = "Voice input not supported in this browser";
        // }
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    // Default to stored language or English
    const storedLang = localStorage.getItem('todo_chat_lang') || 'en';
    recognition.lang = storedLang === 'ur' ? 'ur-PK' : 'en-US';

    recognition.onstart = () => {
        isRecording = true;
        voiceButton.classList.add('recording');
        setStatus('🎤 Listening...');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        messageInput.value = transcript;
        setStatus('Processing voice input...');

        // Automatically send the message
        setTimeout(() => {
            if (messageInput.value.trim()) {
                handleSendMessage(new Event('submit'));
            }
        }, 500);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isRecording = false;
        voiceButton.classList.remove('recording');

        let errorMsg = 'Voice input failed';
        if (event.error === 'no-speech') {
            errorMsg = 'No speech detected. Please try again.';
        } else if (event.error === 'not-allowed') {
            errorMsg = 'Microphone access denied. Please enable it in your browser settings.';
        }

        showError(errorMsg);
        setStatus('Ready');
    };

    recognition.onend = () => {
        isRecording = false;
        voiceButton.classList.remove('recording');
        if (statusText.textContent === '🎤 Listening...') {
            setStatus('Ready');
        }
    };
}

/**
 * Handle voice input button click
 */
function handleVoiceInput() {
    if (!recognition) {
        showError('Voice input not available in this browser');
        return;
    }

    if (isRecording) {
        // Stop recording
        recognition.stop();
        return;
    }

    // Use stored language preference
    const storedLang = localStorage.getItem('todo_chat_lang') || 'en';
    recognition.lang = storedLang === 'ur' ? 'ur-PK' : 'en-US';

    // Start recording
    try {
        recognition.start();
    } catch (error) {
        console.error('Failed to start recognition:', error);
        showError('Failed to start voice input. Please try again.');
    }
}

/**
 * Enable voice button after login
 */
function enableVoiceButton() {
    if (voiceButton) {
        voiceButton.disabled = false;

        // Visual indicator if not supported
        if (!recognition) {
            voiceButton.classList.add('disabled-look');
        }
    }
}

/**
 * Set input text
 */
function setInput(text) {
    messageInput.value = text;
    messageInput.focus();
}

/**
 * Send a message programmatically
 */
function sendMessage(text) {
    messageInput.value = text;
    handleSendMessage(new Event('submit'));
}

// Export for inline onclick handler
window.hideError = hideError;
window.setInput = setInput;
window.sendMessage = sendMessage;

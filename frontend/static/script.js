/**
 * LarAndre+ Chatbot Frontend
 * Handles voice interaction, chat display, and character animations
 */

class LarAndreChatbot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isListening = false;
        this.isSpeaking = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.idleTimer = null;
        this.idleTimeout = 30000; // 30 seconds
        
        // Settings
        this.settings = {
            voiceSpeed: 1.0,
            voicePitch: 1.0,
            autoSpeak: true,
            laraInterrupts: true,
            laraEnabled: true
        };
        
        // DOM elements
        this.chatContainer = document.getElementById('chat-container');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.voiceBtn = document.getElementById('voice-btn');
        this.voiceStatus = document.getElementById('voice-status');
        this.andreFrame = document.getElementById('andre-frame');
        this.laraFrame = document.getElementById('lara-frame');
        this.andreStatus = document.getElementById('andre-status');
        this.laraStatus = document.getElementById('lara-status');
        
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    init() {
        // Initialize speech recognition
        this.initSpeechRecognition();
        
        // Load voices
        this.loadVoices();
        
        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        // Settings panel
        this.initSettings();
        
        // Start idle timer
        this.resetIdleTimer();
        
        console.log('LarAndre+ Chatbot initialized!');
    }
    
    initSpeechRecognition() {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech recognition not supported in this browser');
            this.voiceBtn.disabled = true;
            this.voiceBtn.title = 'Speech recognition not supported';
            return;
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.voiceBtn.classList.add('listening');
            this.voiceStatus.textContent = '🎤 Listening...';
        };
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.userInput.value = transcript;
            this.voiceStatus.textContent = `Heard: "${transcript}"`;
            
            // Auto-send after 1 second
            setTimeout(() => {
                this.sendMessage();
            }, 1000);
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.voiceStatus.textContent = `Error: ${event.error}`;
            this.stopListening();
        };
        
        this.recognition.onend = () => {
            this.stopListening();
        };
    }
    
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        
        // Some browsers load voices asynchronously
        if (this.synthesis.onvoiceschanged !== undefined) {
            this.synthesis.onvoiceschanged = () => {
                this.voices = this.synthesis.getVoices();
            };
        }
    }
    
    toggleVoiceInput() {
        if (!this.recognition) return;
        
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    stopListening() {
        this.isListening = false;
        this.voiceBtn.classList.remove('listening');
        if (!this.voiceStatus.textContent.startsWith('Heard:')) {
            this.voiceStatus.textContent = '';
        }
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        
        if (!message) return;
        
        // Disable input while processing
        this.sendBtn.disabled = true;
        this.userInput.disabled = true;
        this.voiceStatus.textContent = '';
        
        // Display user message
        this.addMessage('user', message);
        
        // Clear input
        this.userInput.value = '';
        
        // Update Andre status
        this.updateCharacterStatus('andre', 'Thinking...');
        
        try {
            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    lara_muted: !this.settings.laraEnabled
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response');
            }
            
            const data = await response.json();
            
            // Handle responses based on who speaks first
            if (data.speaker === 'lara_first' && data.lara_response && this.settings.laraEnabled) {
                // Lara interrupts first
                this.updateCharacterStatus('lara', 'Speaking! 😤');
                await this.addMessage('lara', data.lara_response);
                await this.speak(data.lara_response, 'lara');
                
                // Then Andre responds
                await new Promise(resolve => setTimeout(resolve, 500));
                this.updateCharacterStatus('andre', 'Responding...');
                await this.addMessage('andre', data.andre_response);
                await this.speak(data.andre_response, 'andre');
            } else {
                // Normal Andre response
                this.updateCharacterStatus('andre', 'Speaking...');
                await this.addMessage('andre', data.andre_response);
                await this.speak(data.andre_response, 'andre');
            }
            
            // Reset statuses
            this.updateCharacterStatus('andre', 'Ready');
            this.updateCharacterStatus('lara', 'Watching...');
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('system', 'Sorry, something went wrong. Please try again.');
            this.updateCharacterStatus('andre', 'Error');
        }
        
        // Re-enable input
        this.sendBtn.disabled = false;
        this.userInput.disabled = false;
        this.userInput.focus();
        
        // Reset idle timer
        this.resetIdleTimer();
    }
    
    addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'andre' || type === 'lara') {
            const nameSpan = document.createElement('div');
            nameSpan.className = 'speaker-name';
            nameSpan.textContent = type === 'andre' ? 'Andre' : 'Lara';
            contentDiv.appendChild(nameSpan);
        }
        
        const textP = document.createElement('p');
        textP.textContent = content;
        contentDiv.appendChild(textP);
        
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
    
    removeEmojis(text) {
        // Remove emojis from text for cleaner speech
        return text.replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F900}-\u{1F9FF}]|[\u{1F018}-\u{1F270}]|[\u{238C}-\u{2454}]|[\u{20D0}-\u{20FF}]/gu, '').trim();
    }
    
    async speak(text, character = 'andre') {
        if (!this.settings.autoSpeak) return;
        if (character === 'lara' && !this.settings.laraEnabled) return;
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        // Remove emojis for cleaner speech
        const cleanText = this.removeEmojis(text);
        if (!cleanText) return; // Don't speak if only emojis
        
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = this.settings.voiceSpeed;
        utterance.pitch = this.settings.voicePitch;
        
        // Try to select appropriate voice
        let selectedVoice = null;
        
        if (character === 'andre') {
            // Prefer male voices for Andre
            selectedVoice = this.voices.find(voice => 
                voice.name.includes('Male') || 
                voice.name.includes('Daniel') ||
                voice.name.includes('Alex')
            );
        } else if (character === 'lara') {
            // Prefer female voices for Lara, slightly higher pitch
            selectedVoice = this.voices.find(voice => 
                voice.name.includes('Female') || 
                voice.name.includes('Samantha') ||
                voice.name.includes('Victoria')
            );
            utterance.pitch = this.settings.voicePitch * 1.2; // Slightly higher
        }
        
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }
        
        // Animate character while speaking
        const frame = character === 'andre' ? this.andreFrame : this.laraFrame;
        
        utterance.onstart = () => {
            this.isSpeaking = true;
            frame.classList.add('speaking');
        };
        
        utterance.onend = () => {
            this.isSpeaking = false;
            frame.classList.remove('speaking');
        };
        
        utterance.onerror = (error) => {
            console.error('Speech synthesis error:', error);
            frame.classList.remove('speaking');
        };
        
        this.synthesis.speak(utterance);
        
        // Wait for speech to finish
        return new Promise((resolve) => {
            utterance.onend = () => {
                this.isSpeaking = false;
                frame.classList.remove('speaking');
                resolve();
            };
        });
    }
    
    updateCharacterStatus(character, status) {
        if (character === 'andre') {
            this.andreStatus.textContent = status;
        } else if (character === 'lara') {
            this.laraStatus.textContent = status;
        }
    }
    
    resetIdleTimer() {
        clearTimeout(this.idleTimer);
        
        if (!this.settings.laraInterrupts || !this.settings.laraEnabled) return;
        
        this.idleTimer = setTimeout(() => {
            this.handleIdle();
        }, this.idleTimeout);
    }
    
    async handleIdle() {
        if (this.isSpeaking || !this.settings.laraEnabled) {
            this.resetIdleTimer();
            return;
        }
        
        try {
            const response = await fetch(`/lara/idle?lara_muted=${!this.settings.laraEnabled}`);
            if (response.status === 204) {
                this.updateCharacterStatus('lara', 'Muted 🔇');
                return;
            }
            const data = await response.json();
            
            this.updateCharacterStatus('lara', 'Impatient! 😤');
            await this.addMessage('lara', data.comment);
            await this.speak(data.comment, 'lara');
            this.updateCharacterStatus('lara', 'Watching...');
            
            this.resetIdleTimer();
        } catch (error) {
            console.error('Error getting idle comment:', error);
        }
    }
    
    initSettings() {
        const settingsToggle = document.getElementById('settings-toggle');
        const settingsPanel = document.getElementById('settings-panel');
        const voiceSpeed = document.getElementById('voice-speed');
        const voicePitch = document.getElementById('voice-pitch');
        const speedValue = document.getElementById('speed-value');
        const pitchValue = document.getElementById('pitch-value');
        const autoSpeak = document.getElementById('auto-speak');
        const laraInterrupts = document.getElementById('lara-interrupts');
        const laraMuteToggle = document.getElementById('lara-mute-toggle');
        
        settingsToggle.addEventListener('click', () => {
            settingsPanel.classList.toggle('active');
        });
        
        voiceSpeed.addEventListener('input', (e) => {
            this.settings.voiceSpeed = parseFloat(e.target.value);
            speedValue.textContent = this.settings.voiceSpeed.toFixed(1) + 'x';
        });
        
        voicePitch.addEventListener('input', (e) => {
            this.settings.voicePitch = parseFloat(e.target.value);
            pitchValue.textContent = this.settings.voicePitch.toFixed(1) + 'x';
        });
        
        autoSpeak.addEventListener('change', (e) => {
            this.settings.autoSpeak = e.target.checked;
            if (!e.target.checked) {
                this.synthesis.cancel();
            }
        });
        
        laraInterrupts.addEventListener('change', (e) => {
            this.settings.laraInterrupts = e.target.checked;
            if (e.target.checked) {
                this.resetIdleTimer();
            } else {
                clearTimeout(this.idleTimer);
            }
        });

        laraMuteToggle.addEventListener('change', (e) => {
            this.settings.laraEnabled = !e.target.checked;
            if (this.settings.laraEnabled) {
                this.updateCharacterStatus('lara', 'Watching...');
                this.resetIdleTimer();
            } else {
                this.synthesis.cancel();
                clearTimeout(this.idleTimer);
                this.updateCharacterStatus('lara', 'Muted 🔇');
            }
        });
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new LarAndreChatbot();
});


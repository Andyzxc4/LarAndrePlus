"""
Configuration file for LarAndre+ Chatbot
"""

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000

# Model Configuration
DEFAULT_MODEL = "distilgpt2"  # Lightweight and fast
# Alternative models:
# - "gpt2" (124M params, slower but better quality)
# - "microsoft/DialoGPT-small" (for conversations)
# - "TinyLlama/TinyLlama-1.1B-Chat-v1.0" (1.1B params, good quality)

# Response Generation Settings
MAX_NEW_TOKENS = 100
TEMPERATURE = 0.8
TOP_P = 0.9
REPETITION_PENALTY = 1.2

# Personality Settings
ANDRE_PERSONALITY_TRAITS = [
    "conversational and friendly",
    "witty with a good sense of humor",
    "knowledgeable but not pretentious",
    "occasionally self-deprecating",
    "thoughtful and insightful"
]

LARA_PERSONALITY_TRAITS = [
    "playful and sassy",
    "affectionately jealous",
    "teasing but loving",
    "quick-witted",
    "fiercely protective"
]

# Conversation Settings
MAX_HISTORY = 10  # Number of conversation exchanges to keep
CONTEXT_HISTORY = 3  # Number of exchanges to use for context

# Interruption Settings
LARA_RANDOM_INTERRUPT_CHANCE = 0.10  # 10% chance
IDLE_TIMEOUT_SECONDS = 30

# Trigger words for Lara's jealous responses
TRIGGER_GIRL_NAMES = [
    "sarah", "emma", "olivia", "sophia", "isabella",
    "mia", "emily", "jennifer", "jessica", "amanda",
    "ashley", "laura", "melissa", "nicole", "rachel"
]

# Device Configuration (Auto-detected)
# Will use MPS (Metal Performance Shaders) if available on Apple Silicon
# Otherwise falls back to CPU
USE_MPS_IF_AVAILABLE = True


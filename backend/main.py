"""
LarAndre+ Chatbot Backend
A witty chatbot with dual personalities: Andre (main) and Lara (girlfriend)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from contextlib import asynccontextmanager
import random
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file in project root
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

print(f"📁 Project root: {BASE_DIR}")
print(f"🔑 API key loaded: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

from chatbot_engine import ChatbotEngine

# Initialize chatbot engine
chatbot = ChatbotEngine()

# Store conversation history per session
conversation_sessions = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    await chatbot.initialize()
    yield
    # Shutdown (cleanup if needed)
    pass

app = FastAPI(title="LarAndre+ Chatbot API", lifespan=lifespan)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    andre_response: str
    lara_response: Optional[str] = None
    lara_interrupts: bool = False
    speaker: str  # "andre" or "lara_first"

@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: MessageRequest):
    """
    Main chat endpoint
    Handles conversation logic with Andre and Lara personalities
    """
    try:
        session_id = request.session_id
        message = request.message.strip()
        
        # Initialize session if doesn't exist
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = {
                "history": [],
                "last_activity": time.time(),
                "lara_interrupt_count": 0
            }
        
        session = conversation_sessions[session_id]
        session["last_activity"] = time.time()
        
        # Check if Lara should interrupt
        lara_response = None
        lara_interrupts = False
        lara_is_mad = False
        speaker = "andre"
        
        # Lara interrupts if:
        # 1. User says something bad about Lara (she gets MAD)
        # 2. Another girl's name is mentioned (non-celebrity)
        # 3. Random playful interruption (10% chance)
        
        # Common girl names (non-celebrity)
        girl_names = [
            "sarah", "emma", "olivia", "sophia", "isabella", "mia", "emily", 
            "jennifer", "jessica", "amanda", "ashley", "brittany", "nicole", 
            "samantha", "rachel", "lauren", "hannah", "alexis", "victoria", 
            "madison", "elizabeth", "natalie", "grace", "chloe", "zoe", 
            "lily", "ella", "ava", "abigail", "addison", "mackenzie", 
            "kayla", "leah", "anna", "julia", "morgan", "sydney", "destiny",
            "maria", "stephanie", "catherine", "katherine", "michelle"
        ]
        
        # Celebrity names (won't trigger Lara's jealousy)
        celebrity_names = [
            "taylor swift", "ariana grande", "beyonce", "rihanna", 
            "selena gomez", "kim kardashian", "kylie jenner",
            "billie eilish", "dua lipa", "lady gaga", "adele",
            "scarlett johansson", "emma watson", "jennifer lawrence"
        ]
        
        message_lower = message.lower()
        
        # Check if user said something bad about Lara (PRIORITY - handle this first!)
        # Expanded to catch more variations
        negative_about_lara = [
            'lara is ugly', 'lara is annoying', 'lara is stupid', 
            'lara is dumb', 'lara is bad', 'hate lara', 'lara sucks',
            'lara is mean', 'lara is terrible', 'lara is boring',
            'dont like lara', "don't like lara", 'lara is lame',
            'lara is fat', 'lara is gross', 'lara is weird', 'lara is crazy',
            'lara is useless', 'lara is pathetic', 'lara is worthless',
            'lara looks bad', 'lara sounds bad', 'dislike lara',
            'lara though', 'but lara'  # Catches phrases like "Lara is fat though"
        ]
        
        # Also check for pattern: "lara is [negative word]"
        lara_is_negative_pattern = 'lara is ' in message_lower and any(
            neg_word in message_lower for neg_word in [
                'ugly', 'annoying', 'stupid', 'dumb', 'fat', 'gross', 
                'mean', 'terrible', 'boring', 'lame', 'weird', 'crazy',
                'bad', 'useless', 'pathetic', 'worthless'
            ]
        )
        
        if any(phrase in message_lower for phrase in negative_about_lara) or lara_is_negative_pattern:
            # Lara gets GENUINELY MAD - different from jealousy
            lara_response = await chatbot.generate_lara_mad_response(message)
            lara_interrupts = True
            lara_is_mad = True
            speaker = "lara_first"
            session["lara_interrupt_count"] += 1
        else:
            # Check for celebrity names
            mentions_celebrity = any(celeb in message_lower for celeb in celebrity_names)
            
            # Check for regular girl names
            mentions_other_girl = any(name in message_lower for name in girl_names)
            
            random_interrupt = random.random() < 0.10  # 10% chance
            
            if mentions_celebrity:
                # Celebrity mentioned - Andre responds casually, Lara doesn't get jealous
                pass  # Just let Andre handle it normally
            elif mentions_other_girl:
                # Regular girl name mentioned - Lara gets jealous!
                lara_response = await chatbot.generate_lara_jealous_response(message)
                lara_interrupts = True
                speaker = "lara_first"
                session["lara_interrupt_count"] += 1
            elif random_interrupt and len(session["history"]) > 2:
                lara_response = await chatbot.generate_lara_playful_comment()
                lara_interrupts = True
                speaker = "lara_first"
        
        # Generate Andre's response
        # Pass lara_is_mad flag so Andre knows to calm things down
        andre_response = await chatbot.generate_andre_response(
            message=message,
            history=session["history"],
            lara_interrupted=lara_interrupts,
            lara_is_mad=lara_is_mad
        )
        
        # Check if Lara should respond instead (for "Who is Lara?" questions)
        if andre_response == "LARA_SHOULD_RESPOND":
            lara_response = "I'm Andre's girlfriend hehe! Don't worry, I'm watching everything you say! 😊"
            andre_response = "That's Lara for you! Always making sure everyone knows she's my girlfriend."
            lara_interrupts = True
            speaker = "lara_first"
        
        # Add to conversation history
        session["history"].append({
            "user": message,
            "andre": andre_response,
            "lara": lara_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 exchanges (increased for better context retention)
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]
        
        return ChatResponse(
            andre_response=andre_response,
            lara_response=lara_response,
            lara_interrupts=lara_interrupts,
            speaker=speaker
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/lara/idle")
async def lara_idle_comment():
    """
    Endpoint for when user is idle/quiet
    Returns a playful comment from Lara (DYNAMICALLY GENERATED)
    """
    # Generate dynamic idle comment
    comment = await chatbot.generate_lara_playful_comment()
    return {"comment": comment}

@app.post("/clear/{session_id}")
async def clear_conversation(session_id: str):
    """
    Clear/reset conversation history for a specific session
    """
    if session_id in conversation_sessions:
        # Keep the session but clear history
        conversation_sessions[session_id]["history"] = []
        conversation_sessions[session_id]["lara_interrupt_count"] = 0
        conversation_sessions[session_id]["last_activity"] = time.time()
        return {
            "success": True,
            "message": "Conversation cleared! Starting fresh.",
            "session_id": session_id
        }
    else:
        # Create new session
        conversation_sessions[session_id] = {
            "history": [],
            "lara_interrupt_count": 0,
            "created_at": time.time(),
            "last_activity": time.time()
        }
        return {
            "success": True,
            "message": "New session created!",
            "session_id": session_id
        }

@app.delete("/clear/{session_id}")
async def delete_conversation(session_id: str):
    """
    Completely delete a conversation session
    """
    if session_id in conversation_sessions:
        del conversation_sessions[session_id]
        return {
            "success": True,
            "message": f"Session {session_id} deleted."
        }
    return {
        "success": False,
        "message": f"Session {session_id} not found."
    }

@app.get("/test/dynamic")
async def test_dynamic():
    """Test dynamic Lara response"""
    try:
        response = await chatbot.generate_lara_jealous_response("I talked to Emma")
        return {"success": True, "response": response, "model_available": chatbot.model is not None}
    except Exception as e:
        return {"success": False, "error": str(e), "model_available": chatbot.model is not None}

@app.post("/debug/prompt")
async def debug_prompt(request: MessageRequest):
    """
    Debug endpoint to see the exact prompt being sent to Gemini
    (Doesn't actually call Gemini, just shows the prompt)
    """
    try:
        from datetime import datetime
        
        # Build the prompt exactly as it would be sent
        message = request.message
        session_id = request.session_id or "default"
        
        # Get or create session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = {
                "history": [],
                "lara_interrupt_count": 0,
                "created_at": time.time(),
                "last_activity": time.time()
            }
        
        session = conversation_sessions[session_id]
        
        # Build context
        context_parts = []
        for exchange in session["history"][-5:]:
            context_parts.append(f"User: {exchange['user']}")
            context_parts.append(f"Andre: {exchange['andre']}")
        context = "\n".join(context_parts) if context_parts else "This is the first message."
        
        # Build full prompt
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        full_prompt = f"""{chatbot.andre_system_prompt}

CURRENT DATE & TIME: {current_date} at {current_time}
(Use this to answer questions about "latest", "recent", or current information)

{context}

User: {message}
Andre: """
        
        return {
            "message": message,
            "current_date": current_date,
            "current_time": current_time,
            "full_prompt": full_prompt,
            "prompt_length": len(full_prompt),
            "context_exchanges": len(session["history"])
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": chatbot.is_initialized,
        "active_sessions": len(conversation_sessions)
    }

# Mount static files for frontend
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")
app.mount("/faces", StaticFiles(directory=os.path.join(BASE_DIR, "faces")), name="faces")


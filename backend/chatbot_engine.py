"""
Chatbot Engine using Ollama + Llama 3.2
"""

import ollama
import random
import os
from typing import List, Dict, Optional
from datetime import datetime

class ChatbotEngine:
    def __init__(self):
        self.client = None
        self.is_initialized = False
        self.model_name = "llama3.2:3b"
        
        # Andre's personality - witty and conversational
        self.andre_system_prompt = """You are Andre, a helpful and friendly person. Your girlfriend is Lara.

IMPORTANT RULES:
- Answer ALL questions directly and naturally (no arbitrary length limits)
- Use simple everyday English - talk like a real person
- For "latest" or "recent" questions, give your best answer based on general knowledge
- Be conversational and friendly
- If you truly don't know, just say so briefly
- Always acknowledge Lara when she's mentioned - she's your girlfriend!

Examples:
User: "What is gravity"
Andre: "Gravity is the force that pulls things toward Earth. It's why we don't float away!"

User: "Justin Bieber latest album"  
Andre: "His latest album as of my knowledge is 'Justice' from 2021. Check streaming platforms for any newer releases!"

User: "Tell me about Lara"
Andre: "Lara? She's my girlfriend! She's awesome but gets a bit jealous sometimes haha!"
"""
        
        # Lara's personality - playful and jealous
        self.lara_traits = [
            "playful and sassy",
            "affectionately jealous", 
            "teasing but loving",
            "quick-witted"
        ]
    
    async def initialize(self):
        """Initialize connection to Ollama"""
        try:
            print("🦙 Connecting to Ollama (Local Llama 3.2)...")
            
            # Test connection
            self.client = ollama.Client()
            
            # Simple test - try to get list of models
            try:
                models_response = self.client.list()
                print(f"   Models available: {len(models_response.get('models', []))} models")
            except Exception as list_err:
                print(f"   Note: Could not list models ({list_err}), but will try to use {self.model_name}")
            
            # Test if we can actually use the model with a simple query
            test_response = self.client.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': 'Hi'}],
                options={'num_predict': 10}
            )
            
            if test_response and 'message' in test_response:
                self.is_initialized = True
                print(f"✅ Llama 3.2 ready! (FREE, LOCAL, SMART)")
            else:
                raise Exception("Invalid response format")
            
        except Exception as e:
            print(f"⚠️  Error connecting to Ollama: {e}")
            print("   Make sure Ollama is running: brew services start ollama")
            print("   And model is downloaded: ollama pull llama3.2:3b")
            self.is_initialized = False
    
    async def generate_andre_response(
        self, 
        message: str, 
        history: List[Dict],
        lara_interrupted: bool = False,
        lara_is_mad: bool = False
    ) -> str:
        """Generate Andre's response with his witty personality"""
        
        message_lower = message.lower()

        # Handle special questions first
        # Time/Date questions
        if any(word in message_lower for word in ['time', 'date', 'today', 'day is it', 'what day']):
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")

            if 'time' in message_lower:
                return f"It's {time_str} right now."
            elif 'date' in message_lower or 'today' in message_lower or 'what day' in message_lower:
                return f"Today is {date_str}."
            else:
                return f"It's {time_str} on {date_str}."

        # Who is Andre
        if 'who are you' in message_lower or 'who is andre' in message_lower:
            return "I'm Andre speaking! I'm your best friend today. What can I do for you?"

        # Who is Lara - Let Lara respond herself!
        if 'who is lara' in message_lower:
            return "LARA_SHOULD_RESPOND"
        
        # If Lara is MAD - Andre calms things down
        if lara_is_mad:
            calming_responses = [
                "Whoa, whoa! Let's all calm down here. That wasn't cool to say. Anyway, what can I help you with?",
                "Okay, that was out of line. Let's reset and start fresh. What do you need help with?",
                "Hey, let's not go there. Everyone deserves respect. So, what can I do for you today?",
                "Alright, let's take a breath and move forward. How can I assist you?",
                "That wasn't necessary. Let's keep things friendly. What would you like to talk about?",
            ]
            return random.choice(calming_responses)

        # If Lara interrupted, add a comment about her
        lara_comment = ""
        if lara_interrupted:
            # Check if user mentioned a girl's name
            girl_names = [
                "sarah", "emma", "olivia", "sophia", "isabella", "mia", "emily", 
                "jennifer", "jessica", "amanda", "ashley", "brittany", "nicole", 
                "samantha", "rachel", "lauren", "hannah", "alexis", "victoria", 
                "madison", "elizabeth", "natalie", "grace", "chloe", "zoe", 
                "lily", "ella", "ava", "abigail", "addison", "mackenzie", 
                "kayla", "leah", "anna", "julia", "morgan", "sydney", "destiny",
                "maria", "stephanie", "catherine", "katherine", "michelle"
            ]
            
            mentioned_girl = any(name in message_lower for name in girl_names)
            
            if mentioned_girl:
                # Dynamic cautious responses using Llama
                if self.is_initialized:
                    try:
                        response = self.client.chat(
                            model=self.model_name,
                            messages=[
                                {
                                    'role': 'user',
                                    'content': f"Generate a SHORT, nervous, cautious response (5-8 words max) for someone trying to avoid a topic. Be lighthearted and slightly awkward. Make it unique each time.\n\nExamples:\n'Uhh, who? Let's change topics!'\n'I don't know anything about that!'\n'Let's talk about something else!'\n\nYour response:"
                                }
                            ],
                            options={
                                'temperature': 1.15,
                                'top_p': 0.95,
                                'repeat_penalty': 1.3,
                                'num_predict': 50
                            }
                        )
                        
                        answer = response['message']['content'].strip()
                        if answer and len(answer) > 5 and len(answer) < 100:
                            lara_comment = answer + " "
                            print(f"✨ Andre cautious (Llama): {lara_comment[:50]}...")
                        else:
                            lara_comment = "Uhh, I don't know who that is... let's change topics! "
                    except Exception as e:
                        print(f"⚠️ Andre cautious response failed: {e}")
                        lara_comment = "I... I don't know anything about that! "
                else:
                    lara_comment = "I don't know who that is... keep it down, Lara's watching! "
            else:
                comments = [
                    "Anyway, don't mind her... ",
                    "Ignore my girlfriend, she's always like this... ",
                    "See what I mean? She's jealous... ",
                    "There she goes again... ",
                    "That's Lara for you... "
                ]
                lara_comment = random.choice(comments)
        
        # Build context from recent history
        context = self._build_context(history, max_history=5)
        
        # Create prompt for Llama
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        context_str = f"Recent conversation:\n{context}\n\n" if context and len(context) < 400 else ""
        
        full_prompt = f"""{self.andre_system_prompt}

CURRENT DATE: {current_date} at {current_time}

{context_str}User: {message}

Andre: {lara_comment}"""
        
        # Try to use Llama
        if self.is_initialized:
            try:
                print(f"🦙 Asking Llama: {message}")
                # Build conversation history for context (to avoid repetition)
                messages = [
                    {
                        'role': 'system',
                        'content': self.andre_system_prompt + f"\n\nCurrent date: {current_date}\n\nIMPORTANT: Vary your responses. If asked the same question, give a different angle or phrasing each time."
                    }
                ]
                
                # Add recent conversation history for context awareness
                for exchange in history[-3:]:  # Last 3 exchanges
                    messages.append({'role': 'user', 'content': exchange['user']})
                    messages.append({'role': 'assistant', 'content': exchange['andre']})
                
                # Add current message
                messages.append({'role': 'user', 'content': message})
                
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    options={
                        'temperature': 1.1,  # Higher = more creative and varied
                        'top_p': 0.95,
                        'top_k': 50,
                        'repeat_penalty': 1.2,  # Penalize repetition
                        'num_predict': 200  # Max tokens
                    }
                )
                
                answer = response['message']['content'].strip()
                
                if not answer:
                    print(f"⚠️  Empty response from Llama")
                    return self._fallback_andre_response(message, lara_interrupted)
                
                print(f"✅ Llama responded: {answer[:80]}...")
                
                # Clean up the response
                if answer.startswith("Andre:"):
                    answer = answer[6:].strip()

                # Ensure the cautious/Lara comment is included if she interrupted
                if lara_interrupted and lara_comment:
                    if not any(comment_part in answer for comment_part in lara_comment.split()[:3]):
                        answer = lara_comment + answer
                
                return answer
                
            except Exception as e:
                print(f"❌ Llama error: {type(e).__name__}: {e}")
                return self._fallback_andre_response(message, lara_interrupted)
        else:
            print("⚠️  Using fallback mode (Ollama not initialized)")
            return self._fallback_andre_response(message, lara_interrupted)
    
    async def generate_lara_jealous_response(self, message: str) -> str:
        """Generate Lara's jealous/sassy response dynamically"""
        
        if self.is_initialized:
            try:
                lara_prompt = f"""You are Lara, a playful character. User said: "{message}"

Create a SHORT, witty, playful response (1 sentence) that shows you noticed another person's name was mentioned. Be lighthearted and fun. Add an emoji at the end.

Style examples:
"Wait, who's that you're talking about? Interesting! 😏"
"Oh really? Tell me more about this person! 🤨"
"Did someone else just get mentioned? I'm curious now! 👀"

Your response (keep it short and fun):"""

                response = self.client.chat(
                    model=self.model_name,
                    messages=[{'role': 'user', 'content': lara_prompt}],
                    options={
                        'temperature': 1.2,  # Very creative for Lara
                        'top_p': 0.95,
                        'repeat_penalty': 1.3,  # Strong anti-repetition
                        'num_predict': 100
                    }
                )
                
                answer = response['message']['content'].strip()
                if answer and len(answer) > 10:
                    print(f"✨ Lara jealous (Llama): {answer[:60]}...")
                    return answer
            except Exception as e:
                print(f"⚠️ Lara jealous response failed: {e}")
        
        # Fallback
        responses = [
            "Wait, hold on! Did you just mention another girl? I'm RIGHT here! 😤",
            "Excuse me?! You know I'm your girlfriend, right? Why are you talking about other girls? 😒",
            "Oh really? Another girl? That's interesting... Andre, did you hear that?! 💁‍♀️",
        ]
        return random.choice(responses)
    
    async def generate_lara_mad_response(self, message: str) -> str:
        """Generate Lara's MAD response when insulted"""
        
        if self.is_initialized:
            try:
                lara_prompt = f"""You are Lara. The user just said something VERY rude about you: "{message}"

Respond with GENUINE anger and offense (1-2 sentences). Show that you're seriously upset and won't tolerate disrespect. Be firm and direct. Add an angry emoji.

Examples:
"Excuse me?! Don't EVER talk to me like that! 😡"
"Wow, really? That's incredibly rude! I don't deserve that! 😠"
"Are you serious right now? You can't just say things like that to me! 🤬"

Your angry response:"""

                response = self.client.chat(
                    model=self.model_name,
                    messages=[{'role': 'user', 'content': lara_prompt}],
                    options={
                        'temperature': 1.15,  # High creativity for mad responses
                        'top_p': 0.95,
                        'repeat_penalty': 1.3,
                        'num_predict': 100
                    }
                )
                
                answer = response['message']['content'].strip()
                if answer and len(answer) > 10:
                    print(f"😡 Lara MAD (Llama): {answer[:60]}...")
                    return answer
            except Exception as e:
                print(f"⚠️ Lara mad response failed: {e}")
        
        # Fallback
        responses = [
            "Excuse me?! Don't EVER talk to me like that! 😡",
            "Wow, really? That's incredibly rude and hurtful! 😠",
            "Are you serious right now? I don't deserve to be spoken to that way! 🤬",
        ]
        return random.choice(responses)
    
    async def generate_lara_playful_comment(self) -> str:
        """Generate a random playful comment from Lara"""
        
        if self.is_initialized:
            try:
                lara_prompt = """Generate a SHORT, playful comment (1 sentence) for when someone is being quiet or not responding. Be fun and lighthearted. Add an emoji.

Examples:
"Hey! Are you still there? Say something! 😊"
"Thinking hard or just daydreaming? 🤔"
"Come on, don't leave us waiting! 😄"

Your response:"""

                response = self.client.chat(
                    model=self.model_name,
                    messages=[{'role': 'user', 'content': lara_prompt}],
                    options={
                        'temperature': 1.2,  # Very creative for playful comments
                        'top_p': 0.95,
                        'repeat_penalty': 1.3,
                        'num_predict': 80
                    }
                )
                
                answer = response['message']['content'].strip()
                if answer and len(answer) > 10:
                    print(f"✨ Lara playful (Llama): {answer[:60]}...")
                    return answer
            except Exception as e:
                print(f"⚠️ Lara playful response failed: {e}")
        
        # Fallback
        comments = [
            "Hey! Are you ignoring us? That's rude! 😤",
            "Hello? Earth to you! We're waiting here... 😊",
            "Is this thing on? Are you still there? 🤔",
        ]
        return random.choice(comments)
    
    def _build_context(self, history: List[Dict], max_history: int = 3) -> str:
        """Build conversation context from history"""
        if not history:
            return "This is the first message."
        
        recent_history = history[-max_history:]
        context_parts = []
        
        for exchange in recent_history:
            context_parts.append(f"User: {exchange['user']}")
            context_parts.append(f"Andre: {exchange['andre']}")
        
        return "\n".join(context_parts) if context_parts else "No previous conversation."

    def _fallback_andre_response(self, message: str, lara_interrupted: bool) -> str:
        """Fallback responses when Ollama isn't available"""
        
        message_lower = message.lower()
        
        # Check if user mentioned a girl's name
        girl_names = [
            "sarah", "emma", "olivia", "sophia", "isabella", "mia", "emily", 
            "jennifer", "jessica", "amanda", "ashley", "brittany", "nicole", 
            "samantha", "rachel", "lauren", "hannah", "alexis", "victoria", 
            "madison", "elizabeth", "natalie", "grace", "chloe", "zoe", 
            "lily", "ella", "ava", "abigail", "addison", "mackenzie", 
            "kayla", "leah", "anna", "julia", "morgan", "sydney", "destiny",
            "maria", "stephanie", "catherine", "katherine", "michelle"
        ]
        mentioned_girl = any(name in message_lower for name in girl_names)
        
        prefix = ""
        if lara_interrupted and mentioned_girl:
            cautious_prefixes = [
                "Shh, I don't know who that is... keep it down, Lara's watching! ",
                "Uhh, who? Never heard of her... please, let's change the subject before Lara gets more upset! ",
                "I... I don't know anything about that! Can we talk about something else? ",
            ]
            prefix = random.choice(cautious_prefixes)
        elif lara_interrupted:
            prefixes = [
                "Don't mind her, she's my girlfriend... always jealous! ",
                "That's Lara for you... anyway, ",
                "See? She's always like this... ",
            ]
            prefix = random.choice(prefixes)
        
        # Greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'sup', 'greetings']) and len(message.split()) <= 3:
            responses = [
                f"{prefix}Hey! What's up? I'm Andre, your best friend today!",
                f"{prefix}Hi there! I'm Andre. How can I help you?",
                f"{prefix}Hello! Good to see you here! What's on your mind?",
            ]
            return random.choice(responses)

        # Jokes
        if 'joke' in message_lower:
            jokes = [
                f"{prefix}Why don't scientists trust atoms? Because they make up everything!",
                f"{prefix}What do you call a fake noodle? An impasta!",
                f"{prefix}Why did the scarecrow win an award? He was outstanding in his field!",
            ]
            return random.choice(jokes)
        
        # For everything else
        responses = [
            f"{prefix}That's a good question! Let me think about that for you.",
            f"{prefix}Interesting! I'm working on getting you a proper answer.",
            f"{prefix}Hmm, let me process that... I want to give you a good response!",
        ]
        return random.choice(responses)

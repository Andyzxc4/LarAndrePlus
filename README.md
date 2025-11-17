# LarAndre+ 🤖💕

A witty, interactive chatbot web application featuring dual AI personalities with voice interaction and facial animations!

## Overview

LarAndre+ is a unique chatbot application where you can interact with Andre (the main chatbot) and his playful, jealous girlfriend Lara. The app features:

- 🗣️ **Voice Interaction**: Speak to the chatbot and hear responses in different voices
- 🤖 **Dual Personalities**: Andre provides helpful, witty responses while Lara adds playful interruptions
- 🎭 **Animated Characters**: Visual feedback with character animations during speech
- 🎬 **Talking-Head Videos**: Generate SadTalker videos from a static face + TTS audio (runs on MPS or CPU)
- 🧠 **Powered by AI**: Uses Hugging Face's DistilGPT2 for natural language processing
- ⚡ **Optimized for M4**: Runs efficiently on Apple Silicon (MacBook Pro M4)

## Features

### Main Chatbot (Andre)
- Conversational, humorous personality
- Answers questions like ChatGPT
- Natural-sounding speech synthesis
- Context-aware responses

### Side Character (Lara)
- Playful, sassy personality
- Interrupts when other girls are mentioned
- Comments when user is idle/quiet
- Adds humor and personality to conversations

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI/NLP**: Hugging Face Transformers (DistilGPT2)
- **Talking-Head Animation**: SadTalker (PyTorch w/ MPS + CPU fallback)
- **Voice**: Web Speech API (Speech Recognition + Speech Synthesis)
- **Optimization**: PyTorch with Metal Performance Shaders (MPS) for M4

## Project Structure

```
mini-project/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI server and endpoints
│   └── chatbot_engine.py    # AI/NLP engine with personality logic
├── frontend/
│   ├── index.html           # Main web interface
│   └── static/
│       ├── style.css        # Beautiful, modern styling
│       └── script.js        # Voice interaction and chat logic
├── faces/                   # Character images
│   ├── andre.jpg           # (Add your image here)
│   └── lara.jpg            # (Add your girlfriend's image here)
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.9 or higher
- MacBook Pro M4 (or any Mac with Apple Silicon)
- Modern web browser (Chrome, Safari, Edge)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   git clone <your-github-url>/LarAndrePlus.git /Users/lara/dre-proj-git/LarAndrePlus
   cd /Users/lara/dre-proj-git/LarAndrePlus
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add character images**:
   - Place your face image as `faces/andre.jpg`
   - Place your girlfriend's face image as `faces/lara.jpg`
   - Images should be square (e.g., 500x500px) for best results

5. **Run the application**:
   ```bash
   python run_server.py
   ```

6. **Open in browser**:
   ```
   http://localhost:8000
   ```

## Running Locally on a New Mac (MPS or CPU)

1. **Install prerequisites**
   ```bash
   xcode-select --install          # command-line tools (once)
   brew install ffmpeg git         # ffmpeg needed for SadTalker output
   ```
2. **Clone + create a virtual environment**
   ```bash
   git clone <repo-url> /Users/lara/dre-proj-git/LarAndrePlus
   cd /Users/lara/dre-proj-git/LarAndrePlus
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Prepare SadTalker assets (optional unless you need videos)**
   ```bash
   python tools/setup_talking_head.py
   ```
4. **(Optional) Force CPU mode**
   ```bash
   export TALKING_HEAD_DEVICE=cpu
   export PYTORCH_ENABLE_MPS_FALLBACK=1
   ```
5. **Run the server**
   ```bash
   python run_server.py
   ```
6. **Hit the health & talking-head endpoints**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/talking-head/status
   ```

The same steps work on Intel Macs—the talking-head pipeline will automatically fall back to CPU without any NVIDIA hardware.

## Usage

### Text Chat
1. Type your message in the text area
2. Press "Send" or hit Enter
3. Enjoy the witty responses!

### Voice Chat
1. Click the microphone button 🎤
2. Speak your message
3. The app will transcribe and send automatically
4. Listen to the spoken responses

### Settings
- Click the gear icon ⚙️ to adjust:
  - Voice speed
  - Voice pitch
  - Auto-speak toggle
  - Lara's interruptions toggle
  - Lara mute toggle (completely silence Lara without disabling Andre)

## Talking-Head Generator (SadTalker)

Bring Andre or Lara to life by pairing any TTS audio clip with their static portrait.

1. **Install / update dependencies**
   ```bash
   cd /Users/lara/dre-proj-git/LarAndrePlus
   python3 -m venv venv && source venv/bin/activate  # or reuse your env
   pip install -r requirements.txt
   ```
2. **Download SadTalker assets once**
   ```bash
   python tools/setup_talking_head.py
   ```
3. **Generate a video via CLI**
   ```bash
   python tools/generate_talking_head.py \
       --character lara \
       --audio /path/to/lara-tts.wav
   ```
   Videos land in `generated_media/talking_head/` and are automatically served at  
   `http://localhost:8000/media/talking_head/<filename>.mp4`.
4. **Or call the FastAPI endpoint**
   ```bash
   curl -X POST http://localhost:8000/talking-head \
     -F "character=andre" \
     -F "expression_scale=1.0" \
     -F "audio_file=@/path/to/andre.wav"
   ```

The backend auto-detects Apple Metal (MPS) support and falls back to CPU if needed. You can override with `export TALKING_HEAD_DEVICE=cpu` (or `mps`).

➡️ Need more detail? See `TALKING_HEAD_SETUP.md`.

## Personality Logic

### When Lara Interrupts

1. **Other Girls Mentioned**: If you mention names like Sarah, Emma, Olivia, etc., Lara will interrupt with a jealous comment
2. **Random Interrupts**: 10% chance for playful comments during conversation
3. **Idle Timer**: If you're quiet for 30 seconds, Lara will ask why you're taking so long

### Andre's Responses

After Lara interrupts, Andre will:
1. Address your original question
2. Add a comment like "Don't mind her, she's my girlfriend... always jealous!"
3. Keep the conversation flowing naturally

## Customization

### Adjusting Personalities

Edit `backend/chatbot_engine.py`:
- Modify `andre_traits` for Andre's personality
- Modify `lara_traits` for Lara's personality
- Add more responses in the response arrays

### Changing Models

To use a different Hugging Face model:
```python
# In chatbot_engine.py, line ~32
model_name = "distilgpt2"  # Change to your preferred model
```

Recommended lightweight models:
- `distilgpt2` (default, 82M parameters)
- `gpt2` (124M parameters)
- `microsoft/DialoGPT-small` (for conversations)

### Adding More Trigger Words

Edit `backend/main.py`:
```python
# Line ~57
girl_names = ["sarah", "emma", ...]  # Add more names
```

## Performance Tips

- **First Launch**: Initial model download may take a few minutes
- **MPS Acceleration**: Automatically uses Apple Silicon GPU if available
- **Memory Usage**: Expect ~1-2GB RAM usage for the model
- **Response Time**: 1-3 seconds per response on M4

## Troubleshooting

### Voice Recognition Not Working
- Ensure you're using HTTPS or localhost
- Grant microphone permissions in browser
- Try Chrome or Edge (better speech recognition support)

### Model Loading Errors
```bash
# Clear Hugging Face cache
rm -rf ~/.cache/huggingface
# Reinstall transformers
pip install --upgrade transformers
```

### MPS/GPU Not Available
- Check PyTorch installation: `python -c "import torch; print(torch.backends.mps.is_available())"`
- Reinstall PyTorch: `pip install --upgrade torch`

## Future Enhancements

- [ ] Custom voice training with your actual voice
- [ ] More advanced facial animations (lip-sync)
- [ ] Additional characters
- [ ] Conversation history persistence
- [ ] Multi-language support
- [ ] Mobile app version

## Credits

Created with ❤️ for Andre and Lara

- **AI/ML**: Hugging Face Transformers
- **Framework**: FastAPI
- **Inspiration**: Modern conversational AI and a playful relationship dynamic

## License

This is a personal project. Feel free to fork and customize for your own use!

---

**Note**: This chatbot is optimized for personal use on MacBook Pro M4. Performance may vary on other systems.

Enjoy chatting with LarAndre+! 🎉


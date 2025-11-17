# LarAndre+ Project Structure

Complete overview of the project architecture and file organization.

## Directory Structure

```
mini-project/
├── backend/                    # Backend Python code
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastAPI server & API endpoints
│   └── chatbot_engine.py      # AI/NLP engine with personalities
│
├── frontend/                   # Frontend web interface
│   ├── index.html             # Main HTML page
│   └── static/                # Static assets
│       ├── style.css          # Styling and animations
│       └── script.js          # JavaScript logic & voice API
│
├── faces/                      # Character images
│   ├── README.md              # Image requirements guide
│   ├── andre.jpg              # Your face photo (add this)
│   ├── andre.svg              # Placeholder (auto-generated)
│   ├── lara.jpg               # Girlfriend's photo (add this)
│   └── lara.svg               # Placeholder (auto-generated)
│
├── generated_media/            # Talking-head outputs (served via /media)
├── tools/                      # Helper scripts
│   ├── setup_talking_head.py   # Download SadTalker repo + checkpoints
│   └── generate_talking_head.py# CLI for video generation
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── start.sh                   # Quick start script
├── test_setup.py              # Installation verification
├── create_placeholder_images.py  # Image placeholder generator
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick start guide
├── SETUP_GUIDE.md             # Detailed setup instructions
└── PROJECT_STRUCTURE.md       # This file
```

## File Descriptions

### Backend Files

#### `backend/main.py`
- **Purpose**: FastAPI server and REST API endpoints
- **Key Features**:
  - `/chat` - Main conversation endpoint
  - `/lara/idle` - Idle timeout comments
  - `/health` - Health check
  - `/talking-head/status` - SadTalker readiness
  - `/talking-head` - Generate talking-head video from audio upload
  - Session management
  - CORS middleware
  - Static file serving
- **Dependencies**: FastAPI, chatbot_engine

#### `backend/chatbot_engine.py`
- **Purpose**: AI/NLP processing and personality logic
- **Key Features**:
  - Hugging Face Transformers integration
  - DistilGPT2 model
  - Andre's personality (witty, conversational)
  - Lara's personality (playful, jealous)
  - MPS (Metal Performance Shaders) support for M4
  - Context-aware response generation
- **Key Classes**: `ChatbotEngine`

### Frontend Files

#### `frontend/index.html`
- **Purpose**: Main web interface
- **Key Features**:
  - Character display with animations
  - Chat message area
  - Voice/text input controls
  - Settings panel
  - Responsive design
- **Technologies**: HTML5, Web Speech API

#### `frontend/static/style.css`
- **Purpose**: Styling and visual design
- **Key Features**:
  - Modern gradient backgrounds
  - Character animations (pulse, speaking)
  - Chat bubbles styling
  - Responsive layout
  - Settings panel
- **Design**: Dark theme with blue/pink accents

#### `frontend/static/script.js`
- **Purpose**: Client-side logic and interactions
- **Key Features**:
  - Voice recognition (Speech-to-Text)
  - Voice synthesis (Text-to-Speech)
  - Chat message handling
  - Character animations
  - Idle timeout detection
  - Settings management
- **Main Class**: `LarAndreChatbot`

### Configuration Files

#### `config.py`
- **Purpose**: Centralized configuration
- **Settings**:
  - Server (host, port)
  - AI model selection
  - Personality traits
  - Interruption settings
  - Trigger words
  - Device settings (MPS)

#### `requirements.txt`
- **Purpose**: Python package dependencies
- **Key Packages**:
  - fastapi (web framework)
  - uvicorn (ASGI server)
  - transformers (Hugging Face)
  - torch (PyTorch for ML)
  - pydantic (data validation)

### Utility Files

#### `start.sh`
- **Purpose**: Quick startup script
- **Usage**: `./start.sh`
- **Actions**: Checks environment, activates venv, starts server

#### `test_setup.py`
- **Purpose**: Installation verification
- **Usage**: `python3 test_setup.py`
- **Checks**: Python version, packages, files, MPS support

#### `create_placeholder_images.py`
- **Purpose**: Generate placeholder images
- **Usage**: `python3 create_placeholder_images.py`
- **Output**: SVG placeholder images for testing

### Documentation Files

#### `README.md`
- **Purpose**: Main project documentation
- **Content**: Features, installation, usage, troubleshooting

#### `QUICKSTART.md`
- **Purpose**: Fast 5-minute setup guide
- **Content**: Minimal steps to get started

#### `SETUP_GUIDE.md`
- **Purpose**: Comprehensive setup instructions
- **Content**: Detailed steps, troubleshooting, customization

## Data Flow

### User Message Flow

```
User Input (Text/Voice)
    ↓
Frontend (script.js)
    ↓ POST /chat
Backend API (main.py)
    ↓
Check for interruptions
    ↓
ChatbotEngine (chatbot_engine.py)
    ↓
Hugging Face Model (DistilGPT2)
    ↓
Generated Response
    ↓
Backend API (main.py)
    ↓ JSON Response
Frontend (script.js)
    ↓
Display + Voice Synthesis
```

### Lara Interruption Logic

```
User Message
    ↓
Check triggers:
  • Girl names mentioned?
  • Random interrupt (10%)?
  • Idle timeout (30s)?
    ↓ YES
Generate Lara response
    ↓
Display Lara's comment
    ↓
Speak Lara's voice
    ↓
Generate Andre's response
    ↓
Display Andre's answer
    ↓
Speak Andre's voice
```

## API Endpoints

### `POST /chat`
- **Request**: 
  ```json
  {
    "message": "string",
    "session_id": "string",
    "lara_muted": false
  }
  ```
- **Response**:
  ```json
  {
    "andre_response": "string",
    "lara_response": "string | null",
    "lara_interrupts": "boolean",
    "speaker": "andre | lara_first"
  }
  ```

### `GET /lara/idle`
- **Query**: `lara_muted` (optional) to skip when Lara is disabled
- **Response**:
  ```json
  {
    "comment": "string"
  }
  ```

### `GET /health`
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": "boolean",
    "active_sessions": "number"
  }
  ```

### `GET /talking-head/status`
- **Response**:
  ```json
  {
    "ready": true,
    "repo_dir": ".../vendors/SadTalker",
    "checkpoints_present": true,
    "device": "mps",
    "message": "SadTalker ready"
  }
  ```

### `POST /talking-head`
- **Form Fields**:
  - `character`: `"andre"` or `"lara"`
  - `audio_file`: `.wav` or `.mp3`
  - `expression_scale` (optional float)
  - `still_mode` (optional bool)
- **Response**:
  ```json
  {
    "character": "lara",
    "filename": "lara_20241117_153015.mp4",
    "video_url": "/media/talking_head/lara_20241117_153015.mp4",
    "device": "mps"
  }
  ```

## Key Technologies

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Transformers**: Hugging Face library
- **PyTorch**: Machine learning framework
- **Pydantic**: Data validation

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling and animations
- **JavaScript (ES6+)**: Logic and interactions
- **Web Speech API**: Voice recognition and synthesis

### AI/ML
- **DistilGPT2**: Lightweight language model (82M params)
- **MPS**: Metal Performance Shaders for M4 GPU
- **Tokenizers**: Text processing

## Performance Characteristics

### Resource Usage
- **RAM**: 1-2GB (including model)
- **CPU/GPU**: Moderate (MPS accelerated)
- **Storage**: ~500MB (model cache)

### Response Times
- **First response**: 5-10 seconds (model loading)
- **Subsequent responses**: 1-3 seconds
- **Voice synthesis**: Instant

### Optimization
- MPS (Metal Performance Shaders) for Apple Silicon
- Lightweight DistilGPT2 model
- Conversation history pruning
- Async/await for non-blocking operations

## Customization Points

### Personalities
- Edit `backend/chatbot_engine.py`
- Modify `andre_traits` and `lara_traits` arrays
- Add custom response templates

### Trigger Words
- Edit `config.py`
- Modify `TRIGGER_GIRL_NAMES` list
- Add custom interruption logic in `main.py`

### Styling
- Edit `frontend/static/style.css`
- Change color scheme (CSS variables)
- Modify animations

### AI Model
- Edit `config.py`
- Change `DEFAULT_MODEL`
- Options: gpt2, DialoGPT-medium, TinyLlama, etc.

### Voices
- Edit `frontend/static/script.js`
- Modify voice selection logic
- Adjust pitch/rate settings

## Security Considerations

### Current Implementation
- Runs locally (no external API calls)
- No data persistence
- No user authentication
- CORS allows all origins (development mode)

### Production Recommendations
- Restrict CORS origins
- Add rate limiting
- Implement session authentication
- Add input sanitization
- Use HTTPS

## Future Enhancements

Potential improvements:
- Custom voice cloning
- Advanced lip-sync animations
- WebRTC for real-time voice
- Conversation history export
- Multiple character support
- Emotion detection
- Multi-language support
- Mobile app version

## Maintenance

### Regular Updates
- Update Python packages: `pip install --upgrade -r requirements.txt`
- Clear model cache: `rm -rf ~/.cache/huggingface`
- Check for security updates

### Monitoring
- Check `/health` endpoint
- Monitor RAM usage
- Review error logs

### Backup
- Important files: `backend/`, `frontend/`, `config.py`
- User data: None (no persistence)
- Images: `faces/` directory

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Author**: Andre & Lara 💕


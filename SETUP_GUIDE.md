# LarAndre+ Setup Guide

Complete step-by-step guide to get your chatbot running!

## Quick Start (5 minutes)

```bash
# 1. Navigate to project
cd /Users/andre-d.lacra/ai-native-projects/mini-project

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your images (see below)

# 5. Run the app
./start.sh
```

## Detailed Setup

### 1. System Requirements

- ✅ macOS with Apple Silicon (M1/M2/M3/M4)
- ✅ Python 3.9 or higher
- ✅ 4GB+ free RAM
- ✅ Modern web browser (Chrome, Safari, Edge)
- ✅ Microphone (for voice input)

### 2. Python Environment

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This will install:
# - FastAPI (web framework)
# - Uvicorn (server)
# - Transformers (Hugging Face)
# - PyTorch (AI/ML)
# - And other dependencies
```

**Note**: First installation may take 5-10 minutes as it downloads PyTorch and models.

### 4. Add Character Images

You need to add two images to the `faces/` directory:

1. **Your face** (`andre.jpg`):
   ```bash
   # Copy your image
   cp /path/to/your/photo.jpg faces/andre.jpg
   ```

2. **Your girlfriend's face** (`lara.jpg`):
   ```bash
   # Copy her image
   cp /path/to/girlfriend/photo.jpg faces/lara.jpg
   ```

**Image Requirements**:
- Format: JPG or PNG
- Size: 500x500px recommended (square)
- File size: < 1MB
- Good lighting and clear face visibility

### 5. Test the Installation

```bash
# Test imports
python3 -c "import fastapi, torch, transformers; print('✅ All imports OK')"

# Check PyTorch MPS support
python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

### 6. Run the Application

**Option A: Use the startup script (recommended)**
```bash
./start.sh
```

**Option B: Manual start**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the App

Open your browser and go to:
```
http://localhost:8000
```

You should see the LarAndre+ interface with both characters!

## First Time Usage

### Testing Text Chat
1. Type "Hello!" in the text box
2. Click "Send"
3. Wait for Andre's response (may take a few seconds on first run)
4. Try mentioning another girl's name to trigger Lara!

### Testing Voice Chat
1. Click the microphone button 🎤
2. Allow microphone access when prompted
3. Speak clearly: "Tell me a joke"
4. The app will transcribe and respond
5. Listen to the spoken response

### Adjusting Settings
1. Click the gear icon ⚙️ in the bottom right
2. Adjust voice speed and pitch
3. Toggle auto-speak and interruptions
4. Settings are saved for your session

## Troubleshooting

### Problem: "ModuleNotFoundError"
```bash
# Solution: Activate venv and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "Address already in use"
```bash
# Solution: Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Then restart
./start.sh
```

### Problem: Voice recognition not working
- **Check browser**: Use Chrome or Edge (best support)
- **Check permissions**: Allow microphone access
- **Check connection**: Must be localhost or HTTPS

### Problem: Slow responses
- **First run**: Model downloads take time (normal)
- **Subsequent runs**: Should be faster (1-3 seconds)
- **If still slow**: Consider using distilgpt2 model (default)

### Problem: Images not showing
```bash
# Check images exist
ls -lh faces/

# Should show:
# andre.jpg
# lara.jpg

# Verify they're valid images
file faces/andre.jpg
file faces/lara.jpg
```

### Problem: MPS not available
```bash
# Check PyTorch installation
pip uninstall torch
pip install torch

# Verify MPS
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

## Customization

### Change AI Model

Edit `config.py`:
```python
DEFAULT_MODEL = "distilgpt2"  # Change to your preferred model
```

### Adjust Personalities

Edit `backend/chatbot_engine.py`:
```python
# Around line 16-28
self.andre_traits = [
    "your custom traits here"
]
```

### Add More Trigger Names

Edit `config.py`:
```python
TRIGGER_GIRL_NAMES = [
    "sarah", "emma", "add_more_here"
]
```

### Change Idle Timeout

Edit `config.py`:
```python
IDLE_TIMEOUT_SECONDS = 30  # Change to desired seconds
```

## Advanced Configuration

### Using a Better Model

For better quality responses (requires more RAM/time):

```python
# In config.py
DEFAULT_MODEL = "microsoft/DialoGPT-medium"
# or
DEFAULT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

### Running on Different Port

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Production Mode

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

## Performance Optimization

### M4 Optimization
- The app automatically uses Metal Performance Shaders (MPS)
- Should see "Model loaded on Apple Silicon GPU (MPS)" in logs
- Expect ~1-3 second response times

### Memory Management
- Model uses ~500MB-1GB RAM
- Total app uses ~1-2GB RAM
- Close other apps if experiencing slowness

### Response Speed
- **First response**: 5-10 seconds (model loading)
- **Subsequent responses**: 1-3 seconds
- **Voice synthesis**: Instant

## Getting Help

If you encounter issues:

1. Check the terminal output for error messages
2. Look in the browser console (F12) for JavaScript errors
3. Verify all files are present:
   ```bash
   tree -L 2
   ```
4. Check system resources:
   ```bash
   top -l 1 | grep -E "PhysMem|CPU"
   ```

## Next Steps

Once everything is working:

1. ✅ Chat with Andre and test responses
2. ✅ Trigger Lara by mentioning other names
3. ✅ Test voice interaction
4. ✅ Customize personalities
5. ✅ Adjust settings to your preference
6. ✅ Add more trigger words
7. ✅ Experiment with different AI models

Enjoy your LarAndre+ chatbot! 🎉


# 🚀 How to Run LarAndre+ Chatbot

## Quick Start (Every Time)

### Method 1: Using the Simple Runner (Recommended)

```bash
cd /Users/lara/dre-proj-git/LarAndrePlus
source venv/bin/activate
python run_server.py
```

Then open your browser to: **http://127.0.0.1:8000**

### Method 2: Using the Start Script

```bash
cd /Users/lara/dre-proj-git/LarAndrePlus
source venv/bin/activate
./start.sh
```

Then open your browser to: **http://127.0.0.1:8000**

### Method 3: Manual Start

```bash
cd /Users/lara/dre-proj-git/LarAndrePlus/backend
source ../venv/bin/activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Then open your browser to: **http://127.0.0.1:8000**

---

## First-Time Setup on this Mac

1. **Install prerequisites**
   ```bash
   xcode-select --install         # if you haven't already
   brew install git ffmpeg        # ffmpeg powers SadTalker video writes
   ```
2. **Clone + create your environment**
   ```bash
   git clone <repo-url>/LarAndrePlus.git /Users/lara/dre-proj-git/LarAndrePlus
   cd /Users/lara/dre-proj-git/LarAndrePlus
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Prep SadTalker assets (only if you need talking-head videos)**
   ```bash
   python tools/setup_talking_head.py
   ```
4. **Run the server (pick any quick-start method above)**

Need CPU-only mode? Set `export TALKING_HEAD_DEVICE=cpu` before starting.

---

## What You'll See

When the server starts successfully, you'll see:

```
==================================================
🚀 Starting LarAndre+ Chatbot Server
==================================================

Loading language model...
Model loaded on Apple Silicon GPU (MPS)
Chatbot engine initialized successfully!

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Testing the Server

### Check Health Status
```bash
curl http://127.0.0.1:8000/health
```

Should return:
```json
{"status":"healthy","model_loaded":true,"active_sessions":0}
```

### Access the Web Interface
Open your browser and go to:
```
http://127.0.0.1:8000
```

You should see the beautiful LarAndre+ interface with Andre and Lara!

---

## Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

Or kill it manually:
```bash
pkill -f "uvicorn main:app"
```

Or kill by port:
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Troubleshooting

### "Address already in use"
Port 8000 is occupied. Kill the existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

### "ModuleNotFoundError"
Virtual environment not activated:
```bash
source venv/bin/activate
```

### Model loading slowly
First time loading takes 5-10 seconds (downloading model).
Subsequent starts are faster.

### Can't access from browser
Make sure you're using the correct URL:
- ✅ http://127.0.0.1:8000
- ✅ http://localhost:8000
- ❌ https://... (no HTTPS needed)

---

## Features to Try

Once the app is open:

1. **Text Chat**: Type "Hey Andre, who are you?" and press Enter
2. **Voice Input**: Click the 🎤 microphone button and speak
3. **Trigger Lara**: Type "I met Sarah today" (she'll interrupt!)
4. **Idle Timer**: Wait 30 seconds to see Lara's comment
5. **Settings**: Click the ⚙️ gear icon to adjust voice and behavior

---

## Development Mode

The server runs with `--reload` flag, meaning:
- ✅ Automatically restarts when you edit Python files
- ✅ Changes take effect immediately
- ✅ Great for development

---

## First Run

On first run, you'll see:
1. "Loading language model..." (5-10 seconds)
2. Model downloads from Hugging Face (~270MB)
3. "Model loaded on Apple Silicon GPU (MPS)" ✅
4. Server starts listening

Subsequent runs are faster since the model is cached.

---

## Your Setup

**Project**: `/Users/lara/dre-proj-git/LarAndrePlus`  
**Python**: 3.12+ recommended  
**AI Model**: Llama 3.2 via Ollama (local)  
**Talking-Head**: SadTalker (PyTorch w/ MPS or CPU fallback)  
**GPU**: MPS (Metal Performance Shaders) ✅  
**Images**: `faces/Andre.JPG`, `faces/Lara.png`

---

## Everything Working!

✅ Dependencies installed  
✅ Virtual environment created  
✅ AI model loads successfully  
✅ MPS (GPU) acceleration enabled  
✅ Server starts and responds  
✅ Frontend accessible  
✅ Images present

**You're ready to chat!** 🎉

---

## Need Help?

- **Installation issues**: Read `INSTALLATION_SUCCESS.md`
- **General docs**: Read `START_HERE.md`
- **Quick guide**: Read `QUICKSTART.md`
- **Customization**: Edit `config.py`
- **Test setup**: Run `python test_setup.py`

Enjoy your LarAndre+ chatbot! 🤖💕


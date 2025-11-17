# 🚀 Quick Start Guide

Get LarAndre+ running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ macOS (preferably with Apple Silicon M1/M2/M3/M4)
- ✅ Python 3.9+ installed
- ✅ At least 4GB free RAM

## Installation (One-Time Setup)

### Step 1: Open Terminal

Press `Cmd + Space`, type "Terminal", and press Enter.

### Step 2: Navigate to Project

```bash
cd /Users/andre-d.lacra/ai-native-projects/mini-project
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (you'll need to do this each time you open a new terminal)
source venv/bin/activate

# Your terminal should now show (venv) at the beginning
```

### Step 4: Install Required Packages

```bash
# This will take 5-10 minutes on first run
pip install -r requirements.txt
```

Wait for all packages to download and install. You'll see a progress bar.

### Step 5: Add Your Photos

Option A - Use placeholders for testing:
```bash
python3 create_placeholder_images.py
```

Option B - Add your real photos:
```bash
# Copy your photo
cp /path/to/your-photo.jpg faces/andre.jpg

# Copy your girlfriend's photo
cp /path/to/girlfriend-photo.jpg faces/lara.jpg
```

### Step 6: Test Installation (Optional but Recommended)

```bash
python3 test_setup.py
```

If you see "ALL TESTS PASSED" ✅, you're ready to go!

## Running the App

### Every Time You Want to Use the App:

```bash
# Make sure you're in the project directory
cd /Users/andre-d.lacra/ai-native-projects/mini-project

# Activate the virtual environment
source venv/bin/activate

# Start the server
./start.sh
```

You should see:
```
🚀 Starting LarAndre+ Chatbot...
✅ Environment ready!
🤖 Starting FastAPI server...
Access the app at: http://localhost:8000
```

### Open in Browser

Open your favorite browser and go to:
```
http://localhost:8000
```

You should see the beautiful LarAndre+ interface! 🎉

## Using the App

### Text Chat
1. Type a message in the text box
2. Press Enter or click "Send"
3. Wait a few seconds for the response
4. Enjoy the conversation!

**Try asking:**
- "Tell me a joke"
- "What's the weather like?"
- "Who's your girlfriend?"
- "I met Sarah today" (triggers Lara! 😄)

### Voice Chat
1. Click the microphone button 🎤
2. Allow microphone access when prompted
3. Speak clearly
4. Watch it transcribe your speech
5. Get a spoken response!

### Trigger Lara
Mention another girl's name to see Lara's jealous response:
- "I met Emma today"
- "Sarah said hello"
- "I was talking to Olivia"

### Stay Quiet
Don't type or speak for 30 seconds, and Lara will interrupt with a comment! 😄

## Stopping the App

Press `Ctrl + C` in the terminal where the server is running.

## Troubleshooting

### "ModuleNotFoundError"
You forgot to activate the virtual environment:
```bash
source venv/bin/activate
```

### "Port already in use"
The app is already running, or another app is using port 8000:
```bash
# Kill the process
lsof -ti:8000 | xargs kill -9
# Then start again
./start.sh
```

### Voice input not working
- Use Chrome or Edge browser (Safari has limited support)
- Make sure you clicked "Allow" for microphone permissions
- Try typing instead

### Slow first response
- This is normal! The AI model loads on first use
- Subsequent responses are much faster (1-3 seconds)

### Images not showing
Make sure you have:
- `faces/andre.jpg` or `faces/andre.svg`
- `faces/lara.jpg` or `faces/lara.svg`

## Tips & Tricks

### Better Responses
The app gets better at conversation as you chat more. Give it context!

### Customize Settings
Click the gear icon ⚙️ to adjust:
- Voice speed (talk faster/slower)
- Voice pitch (higher/lower voice)
- Auto-speak (toggle automatic voice responses)
- Lara's interruptions (toggle her comments)

### Keyboard Shortcuts
- `Enter`: Send message
- `Shift + Enter`: New line in message

## What's Next?

Once comfortable, check out:
- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Detailed setup guide
- `config.py` - Customization options

## Common Questions

**Q: How much does this cost?**
A: Nothing! It runs completely locally on your Mac.

**Q: Is my data private?**
A: Yes! Everything runs on your computer. No data is sent to external servers.

**Q: Can I use a different AI model?**
A: Yes! Edit `config.py` and change `DEFAULT_MODEL`.

**Q: Why is it slow?**
A: First response loads the model. After that it should be fast. If consistently slow, you may need to close other apps.

**Q: Can I change the personalities?**
A: Yes! Edit `backend/chatbot_engine.py` to customize Andre and Lara.

**Q: The voices sound robotic**
A: They use your Mac's text-to-speech. For custom voices, you'd need to record voice samples (future feature!).

## Need More Help?

Check the full guides:
- `README.md` - Complete documentation
- `SETUP_GUIDE.md` - Detailed setup
- `config.py` - Configuration options

---

**Enjoy your LarAndre+ chatbot!** 🎉

If you have issues, make sure to:
1. Check terminal output for errors
2. Run `python3 test_setup.py` to verify installation
3. Make sure virtual environment is activated
4. Check browser console (F12) for JavaScript errors


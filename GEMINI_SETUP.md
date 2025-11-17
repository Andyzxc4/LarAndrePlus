# 🚀 Gemini AI Setup (FREE!)

Your chatbot now uses **Google Gemini Flash** - it's smart, fast, and uses simple English!

## Why Gemini?

- ✅ **Actually Smart**: Understands and answers questions properly
- ✅ **Fast**: Responds in 1-2 seconds
- ✅ **Free**: No cost for personal use
- ✅ **Simple English**: Talks like a real person
- ✅ **Lightweight**: No huge model downloads
- ✅ **Always Updated**: Google keeps improving it

## 🔑 Get Your FREE API Key (2 minutes)

### Step 1: Go to Google AI Studio
Open this link in your browser:
```
https://aistudio.google.com/app/apikey
```

### Step 2: Sign In
- Use your Google account (Gmail)
- If you don't have one, create it (free)

### Step 3: Create API Key
- Click "Create API Key" button
- It will generate a long string like: `AIzaSyD...`
- **Copy this key!**

### Step 4: Set the API Key

**Option A: Using Terminal (Temporary)**
```bash
export GEMINI_API_KEY='your-key-here'
```
(Replace `your-key-here` with your actual key)

**Option B: Using .env File (Permanent - Recommended)**
```bash
cd /Users/andre-d.lacra/ai-native-projects/mini-project

# Create .env file
echo "GEMINI_API_KEY='your-key-here'" > .env
```

**Option C: Add to Shell Profile (Always Active)**
```bash
# Add to your ~/.zshrc or ~/.bash_profile
echo "export GEMINI_API_KEY='your-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### Step 5: Restart the Server
```bash
cd /Users/andre-d.lacra/ai-native-projects/mini-project
source venv/bin/activate
python run_server.py
```

---

## ✅ Verify It's Working

When you start the server, you should see:
```
✅ Gemini AI ready! (Fast and smart)
```

Instead of:
```
⚠️  WARNING: No Gemini API key found!
```

---

## 🧪 Test Your Chatbot

Once running, open http://127.0.0.1:8000 and try:

1. **Smart Questions**:
   - "What's the meaning of life?"
   - "How does gravity work?"
   - "Tell me about artificial intelligence"

2. **Conversations**:
   - "Hey, how are you?"
   - "What's your favorite hobby?"
   - "Do you like pizza?"

3. **Trigger Lara**:
   - "I met Sarah today" (she'll interrupt!)
   - "My friend Emma is nice"

The responses will be MUCH better than before! 🎉

---

## 🆓 Is It Really Free?

**YES!** Google Gemini has a free tier:
- **15 requests per minute** (more than enough)
- **1,500 requests per day** (plenty for personal use)
- **No credit card required**

For your personal chatbot, this is perfect!

---

## 🔒 Security

**Keep your API key secret!**
- ❌ Don't share it online
- ❌ Don't commit it to Git (it's in .gitignore)
- ✅ Store it in .env file
- ✅ Only use it for your personal projects

---

## 🐛 Troubleshooting

### "No API key found" Warning
**Solution**: Follow Step 4 above to set your key

### "API key invalid"
**Solution**: Make sure you copied the entire key (starts with `AIza`)

### "Quota exceeded"
**Solution**: You hit the free limit (rare). Wait a few minutes.

### ".env file not loading"
**Solution**: Install python-dotenv:
```bash
pip install python-dotenv
```

Then add to backend/main.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📊 What Changed?

### Before (DistilGPT2):
- ❌ Slow responses (5-10 seconds)
- ❌ Often nonsensical answers
- ❌ Limited understanding
- ❌ 270MB model download
- ✅ Ran locally (no internet needed)

### After (Gemini Flash):
- ✅ Fast responses (1-2 seconds)
- ✅ Smart, accurate answers
- ✅ Understands context well
- ✅ No downloads needed
- ✅ Simple English responses
- ⚠️ Needs internet connection

---

## 🔄 Want to Switch Back?

If you prefer the local model (no internet):

1. Uncomment lines in `requirements.txt`:
   ```
   transformers==4.46.3
   torch==2.9.0
   accelerate==1.2.1
   ```

2. Install them:
   ```bash
   pip install transformers torch accelerate
   ```

3. Let me know and I'll switch the code back!

---

## 💡 Pro Tips

### Make Responses Even Better
Edit the system prompt in `backend/chatbot_engine.py` (line 20-31) to customize Andre's personality!

### Check API Usage
Go to: https://aistudio.google.com/app/apikey
Click on your key to see usage stats.

### Get More Quota
If you need more requests, you can upgrade (but unlikely needed for personal use).

---

## 🎉 You're All Set!

Once you add your API key, your chatbot will be MUCH smarter!

**Quick Summary:**
1. Get key: https://aistudio.google.com/app/apikey
2. Set it: `export GEMINI_API_KEY='your-key'`
3. Run: `python run_server.py`
4. Chat: http://127.0.0.1:8000

Enjoy your smart, witty AI companion! 🤖💕

---

**Questions?** Read `HOW_TO_RUN.md` for server setup.


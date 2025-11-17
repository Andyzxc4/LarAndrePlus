#!/bin/bash
# Quick Gemini API Setup Script

echo "========================================"
echo "🚀 Gemini API Setup"
echo "========================================"
echo ""

# Check if API key is already set
if [ ! -z "$GEMINI_API_KEY" ]; then
    echo "✅ API key already set!"
    echo "   Key: ${GEMINI_API_KEY:0:20}..."
    echo ""
    echo "You're ready to go! Just run:"
    echo "  python run_server.py"
    exit 0
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Found .env file"
    source .env
    if [ ! -z "$GEMINI_API_KEY" ]; then
        echo "✅ API key loaded from .env"
        export GEMINI_API_KEY
        echo ""
        echo "You're ready! Run:"
        echo "  python run_server.py"
        exit 0
    fi
fi

# No API key found
echo "⚠️  No Gemini API key found!"
echo ""
echo "Don't worry! Your chatbot works without it,"
echo "but it's MUCH smarter with Gemini AI."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Quick Setup (2 minutes, FREE):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Get your FREE API key:"
echo "   👉 https://aistudio.google.com/app/apikey"
echo ""
echo "2️⃣  Copy the key (starts with 'AIza...')"
echo ""
echo "3️⃣  Run this command:"
echo "   export GEMINI_API_KEY='your-key-here'"
echo ""
echo "4️⃣  Start the server:"
echo "   python run_server.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OR create a .env file (permanent):"
echo "  echo \"GEMINI_API_KEY='your-key-here'\" > .env"
echo ""
echo "Full guide: Read GEMINI_SETUP.md"
echo ""
echo "========================================"


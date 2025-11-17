#!/bin/bash
# LarAndre+ Startup Script

echo "🚀 Starting LarAndre+ Chatbot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ Dependencies not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Environment ready!"
echo "🤖 Starting FastAPI server..."
echo ""
echo "Access the app at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Start the server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000


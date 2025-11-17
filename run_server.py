#!/usr/bin/env python3
"""
Simple server runner for LarAndre+ Chatbot
Run this from anywhere in the project
"""

import os
import sys

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')

# Add backend to path
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

print("=" * 50)
print("🚀 Starting LarAndre+ Chatbot Server")
print("=" * 50)
print()
print("Backend directory:", backend_dir)
print("Project root:", project_root)
print()
print("Loading...")
print()

# Import and run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


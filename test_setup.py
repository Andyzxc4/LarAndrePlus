#!/usr/bin/env python3
"""
Test script to verify LarAndre+ installation
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version OK")
        return True
    else:
        print("❌ Python 3.9+ required")
        return False

def check_imports():
    """Check required packages"""
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'transformers': 'Transformers',
        'torch': 'PyTorch',
        'pydantic': 'Pydantic'
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            all_ok = False
    
    return all_ok

def check_torch_mps():
    """Check PyTorch MPS support"""
    try:
        import torch
        if torch.backends.mps.is_available():
            print("✅ MPS (Apple Silicon GPU) available")
            return True
        else:
            print("⚠️  MPS not available, will use CPU")
            return True
    except Exception as e:
        print(f"❌ Error checking MPS: {e}")
        return False

def check_files():
    """Check required files exist"""
    required_files = [
        'requirements.txt',
        'backend/main.py',
        'backend/chatbot_engine.py',
        'frontend/index.html',
        'frontend/static/style.css',
        'frontend/static/script.js',
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_ok = False
    
    return all_ok

def check_images():
    """Check face images"""
    images = ['faces/andre.jpg', 'faces/lara.jpg']
    
    for img in images:
        if os.path.exists(img):
            print(f"✅ {img} present")
        else:
            print(f"⚠️  {img} missing (add your images here)")

def main():
    print("=" * 50)
    print("LarAndre+ Installation Test")
    print("=" * 50)
    print()
    
    print("1. Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("2. Checking required packages...")
    imports_ok = check_imports()
    print()
    
    print("3. Checking PyTorch MPS support...")
    mps_ok = check_torch_mps()
    print()
    
    print("4. Checking project files...")
    files_ok = check_files()
    print()
    
    print("5. Checking face images...")
    check_images()
    print()
    
    print("=" * 50)
    if python_ok and imports_ok and files_ok:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Next steps:")
        print("1. Add your face images to faces/ directory")
        print("2. Run: ./start.sh")
        print("3. Open: http://localhost:8000")
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("Fix the issues above, then run this test again.")
        print()
        print("Common fixes:")
        print("- Install packages: pip install -r requirements.txt")
        print("- Check Python version: python3 --version")
    print("=" * 50)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Create placeholder images for testing
Run this if you don't have face images yet
"""

import os

def create_svg_placeholder(name, color, output_path):
    """Create an SVG placeholder image"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="500" fill="{color}"/>
  <circle cx="250" cy="200" r="80" fill="white" opacity="0.3"/>
  <ellipse cx="230" cy="190" rx="15" ry="20" fill="black" opacity="0.5"/>
  <ellipse cx="270" cy="190" rx="15" ry="20" fill="black" opacity="0.5"/>
  <path d="M 200 250 Q 250 290 300 250" stroke="black" stroke-width="3" fill="none" opacity="0.5"/>
  <text x="250" y="350" font-family="Arial, sans-serif" font-size="40" fill="white" text-anchor="middle" font-weight="bold">{name}</text>
  <text x="250" y="400" font-family="Arial, sans-serif" font-size="20" fill="white" text-anchor="middle" opacity="0.7">Placeholder Image</text>
  <text x="250" y="430" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle" opacity="0.5">Replace with real photo</text>
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg_content)

def main():
    # Create faces directory if it doesn't exist
    os.makedirs('faces', exist_ok=True)
    
    # Create placeholder images
    print("Creating placeholder images...")
    
    # Andre placeholder (blue)
    if not os.path.exists('faces/andre.jpg'):
        create_svg_placeholder('ANDRE', '#3b82f6', 'faces/andre.svg')
        print("✅ Created faces/andre.svg (placeholder for Andre)")
        print("   Note: Rename your actual photo to andre.jpg")
    else:
        print("✅ faces/andre.jpg already exists")
    
    # Lara placeholder (pink)
    if not os.path.exists('faces/lara.jpg'):
        create_svg_placeholder('LARA', '#ec4899', 'faces/lara.svg')
        print("✅ Created faces/lara.svg (placeholder for Lara)")
        print("   Note: Rename your actual photo to lara.jpg")
    else:
        print("✅ faces/lara.jpg already exists")
    
    print()
    print("=" * 50)
    print("Placeholder images created!")
    print()
    print("To use your real photos:")
    print("1. Copy your face photo: cp /path/to/photo.jpg faces/andre.jpg")
    print("2. Copy girlfriend's photo: cp /path/to/photo.jpg faces/lara.jpg")
    print()
    print("Image requirements:")
    print("- Format: JPG or PNG")
    print("- Recommended size: 500x500px (square)")
    print("- File size: < 1MB")
    print("=" * 50)

if __name__ == "__main__":
    main()


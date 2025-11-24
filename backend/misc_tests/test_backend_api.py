"""
Test the actual backend API endpoint to verify real LLM is being used.

Usage:
    cd backend
    uv run python misc_tests/test_backend_api.py
"""

import os
import sys
import json
import requests
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


def test_backend_endpoint():
    """Test the backend API endpoint."""
    print("=" * 70)
    print("  TESTING BACKEND API ENDPOINT")
    print("=" * 70)
    
    url = "http://localhost:8000/api/v1/ai/layout/generate"
    
    payload = {
        "prompt": "Create an Instagram post for a tech startup launch with blue and purple gradient, modern minimalist style"
    }
    
    print(f"\nAPI Key (first 10 chars): {settings.GEMINI_API_KEY[:10]}...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"\nMaking request...")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n[OK] Response received!")
            print(f"\nDesign ID: {result.get('id')}")
            print(f"Title: {result.get('title')}")
            print(f"Format: {result.get('format')}")
            
            design_json = result.get('design_json', {})
            objects = design_json.get('objects', [])
            
            print(f"\nDesign JSON:")
            print(f"  Version: {design_json.get('version')}")
            print(f"  Background: {design_json.get('background')}")
            print(f"  Number of objects: {len(objects)}")
            
            # Check if it's mock data
            is_mock = False
            for obj in objects:
                if obj.get('type') == 'text':
                    text = obj.get('text', '')
                    if 'Sample Headline' in text or 'Sample Subheadline' in text:
                        is_mock = True
                        break
            
            if is_mock:
                print(f"\n[X] WARNING: Response contains MOCK DATA!")
                print(f"    Text contains 'Sample Headline' or 'Sample Subheadline'")
                print(f"    This means the real LLM is NOT being used!")
                return False
            else:
                print(f"\n[OK] Response appears to be REAL AI-generated content!")
                print(f"    No mock data patterns detected.")
                
                # Show some text objects
                print(f"\n  Text objects:")
                for i, obj in enumerate(objects):
                    if obj.get('type') == 'text':
                        print(f"    {i+1}. {obj.get('text', 'N/A')[:50]}")
                
                return True
        else:
            print(f"\n[X] Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n[X] Exception: {type(e).__name__}")
        print(f"Message: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_backend_endpoint()
    
    print("\n" + "=" * 70)
    if success:
        print("  SUCCESS: Real LLM is being used!")
    else:
        print("  FAILURE: Mock data is being returned!")
    print("=" * 70)


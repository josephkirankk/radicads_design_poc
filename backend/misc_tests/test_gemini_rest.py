"""
Test Gemini API using direct REST API calls vs SDK.

This script compares:
1. Direct REST API call (using requests)
2. Python SDK call (using google.genai)

Usage:
    cd backend
    uv run python misc_tests/test_gemini_rest.py
"""

import os
import sys
import json
import asyncio
import requests
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from google import genai


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_rest_api():
    """Test using direct REST API call."""
    print_section("TEST 1: Direct REST API Call")
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say 'REST API works!' in exactly those words."
                    }
                ]
            }
        ]
    }
    
    print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10]}...")
    print(f"URL: {url}")
    print(f"Making REST API call...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"[OK] Status: {response.status_code}")
            print(f"[OK] Response: {text}")
            return True
        else:
            print(f"[X] Status: {response.status_code}")
            print(f"[X] Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"[X] Exception: {type(e).__name__}")
        print(f"[X] Message: {str(e)}")
        return False


def test_sdk_sync():
    """Test using Python SDK (synchronous)."""
    print_section("TEST 2: Python SDK (Synchronous)")
    
    print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10]}...")
    print(f"Model: {settings.GEMINI_MODEL_NAME}")
    print(f"SDK Version: {genai.__version__ if hasattr(genai, '__version__') else 'Unknown'}")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print("[OK] Client initialized")
        
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents="Say 'SDK works!' in exactly those words."
        )
        
        print(f"[OK] Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"[X] Exception: {type(e).__name__}")
        print(f"[X] Message: {str(e)}")
        
        # Print detailed error info
        if hasattr(e, '__dict__'):
            print(f"[X] Error details: {e.__dict__}")
        
        return False


async def test_sdk_async():
    """Test using Python SDK (asynchronous)."""
    print_section("TEST 3: Python SDK (Asynchronous)")
    
    print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10]}...")
    print(f"Model: {settings.GEMINI_MODEL_NAME}")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print("[OK] Client initialized")
        
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents="Say 'Async SDK works!' in exactly those words."
        )
        
        print(f"[OK] Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"[X] Exception: {type(e).__name__}")
        print(f"[X] Message: {str(e)}")
        
        # Print detailed error info
        if hasattr(e, '__dict__'):
            print(f"[X] Error details: {e.__dict__}")
        
        return False


async def main():
    """Run all tests."""
    print_section("GEMINI API COMPARISON TEST")
    print(f"Comparing REST API vs Python SDK")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    # Test 1: REST API
    rest_works = test_rest_api()
    
    # Test 2: SDK Sync
    sdk_sync_works = test_sdk_sync()
    
    # Test 3: SDK Async
    sdk_async_works = await test_sdk_async()
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"REST API:        {'[OK]' if rest_works else '[X]'}")
    print(f"SDK Sync:        {'[OK]' if sdk_sync_works else '[X]'}")
    print(f"SDK Async:       {'[OK]' if sdk_async_works else '[X]'}")
    
    if rest_works and not sdk_sync_works:
        print("\n" + "!" * 70)
        print("  REST API works but SDK fails!")
        print("  This suggests an issue with the Python SDK configuration.")
        print("!" * 70)
    elif rest_works and sdk_sync_works:
        print("\n" + "=" * 70)
        print("  All tests passed! API key is valid.")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())


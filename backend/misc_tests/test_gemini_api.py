"""
Test script for Gemini API integration.

This script tests the Gemini API by:
1. Loading the API key from the .env file
2. Making a simple test call to verify the API key works
3. Testing the layout generation flow (prompt -> brief -> design)

Usage:
    cd backend
    uv run python misc_tests/test_gemini_api.py
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.schemas.ai_models import DesignBrief


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_api_key_validity():
    """Test if the API key is valid by making a simple call."""
    print_section("TEST 1: API Key Validity")
    
    print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10]}...")
    print(f"API Key length: {len(settings.GEMINI_API_KEY)}")
    print(f"Model: {settings.GEMINI_MODEL_NAME}")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print("✓ Client initialized successfully")
        
        # Make a simple test call
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents="Say 'Hello, API is working!' in exactly those words."
        )
        
        print(f"✓ API call successful!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"✗ API call failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False


async def test_prompt_to_brief():
    """Test converting a prompt to a design brief."""
    print_section("TEST 2: Prompt to Brief Conversion")
    
    test_prompt = "Create an Instagram post for a tech startup launch with blue and purple gradient, modern minimalist style"
    print(f"Test prompt: {test_prompt}")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        enhanced_prompt = f"""
You are a professional graphic designer. Analyze the following design request and create a structured design brief.

Design Request: {test_prompt}

Create a design brief that includes:
- A catchy, concise headline (max 6 words)
- An optional subheadline for supporting text
- Visual focus elements (what should stand out)
- Layout style (modern, minimal, bold, etc.)
- Color scheme with primary, secondary, and accent colors
"""
        
        print("Calling Gemini API...")
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=enhanced_prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": DesignBrief.model_json_schema(),
            }
        )
        
        # Parse and validate
        brief_obj = DesignBrief.model_validate_json(response.text)
        brief_dict = brief_obj.model_dump()
        
        print("✓ Brief generated successfully!")
        print(f"\nBrief Details:")
        print(f"  Headline: {brief_dict.get('headline')}")
        print(f"  Subheadline: {brief_dict.get('subheadline')}")
        print(f"  Layout Style: {brief_dict.get('layout_style')}")
        print(f"  Visual Focus: {', '.join(brief_dict.get('visual_focus', []))}")
        print(f"  Colors:")
        colors = brief_dict.get('color_scheme', {})
        print(f"    Primary: {colors.get('primary')}")
        print(f"    Secondary: {colors.get('secondary')}")
        print(f"    Accent: {colors.get('accent')}")
        
        return True, brief_dict
        
    except Exception as e:
        print(f"✗ Brief generation failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False, None


async def test_brief_to_design(brief: dict):
    """Test converting a brief to Fabric.js design JSON."""
    print_section("TEST 3: Brief to Design Conversion")
    
    if not brief:
        print("⊘ Skipping - no brief available from previous test")
        return False
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        design_prompt = f"""
You are a professional graphic designer creating a design in Fabric.js format.

Design Brief:
- Headline: {brief.get('headline')}
- Subheadline: {brief.get('subheadline', 'N/A')}
- Layout Style: {brief.get('layout_style')}
- Canvas Size: 1080x1080 pixels

Create a Fabric.js JSON with proper structure including version, objects array, and background.
"""
        
        print("Calling Gemini API...")
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=design_prompt,
            config={
                "response_mime_type": "application/json",
            }
        )
        
        # Parse the JSON
        design_json = json.loads(response.text)
        
        print("✓ Design generated successfully!")
        print(f"\nDesign Details:")
        print(f"  Version: {design_json.get('version', 'N/A')}")
        print(f"  Background: {design_json.get('background', 'N/A')}")
        print(f"  Number of objects: {len(design_json.get('objects', []))}")
        
        if design_json.get('objects'):
            print(f"\n  Objects:")
            for i, obj in enumerate(design_json['objects'][:5], 1):  # Show first 5
                print(f"    {i}. Type: {obj.get('type')}, Text: {obj.get('text', 'N/A')[:30]}")
        
        return True
        
    except Exception as e:
        print(f"✗ Design generation failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print_section("GEMINI API TEST SUITE")
    print(f"Testing Gemini API integration for Radic Backend")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    # Test 1: API Key Validity
    api_valid = test_api_key_validity()
    
    if not api_valid:
        print("\n" + "!" * 70)
        print("  API key is invalid or expired. Please update your .env file.")
        print("  Get a new key from: https://makersuite.google.com/app/apikey")
        print("!" * 70)
        return
    
    # Test 2: Prompt to Brief
    brief_success, brief = await test_prompt_to_brief()
    
    # Test 3: Brief to Design
    if brief_success:
        await test_brief_to_design(brief)
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"✓ API Key Valid: {api_valid}")
    print(f"✓ Prompt to Brief: {brief_success}")
    print(f"✓ Brief to Design: {brief_success}")  # Only runs if brief succeeds
    
    if api_valid and brief_success:
        print("\n🎉 All tests passed! The Gemini API integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())


"""Test script to list available Gemini models and test generation"""
import asyncio
from google import genai

API_KEY = "AIzaSyAAD5TdEPiKCDe8H3g_6EJa48SWbIj6rYY"

async def main():
    client = genai.Client(api_key=API_KEY)
    
    print("=== Listing Available Models ===\n")
    try:
        # List all models
        models = await client.aio.models.list()
        for model in models:
            print(f"Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Supported Methods: {', '.join(model.supported_generation_methods)}")
            print()
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Test a few model names
    test_models = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest",
    ]
    
    print("\n=== Testing Models ===\n")
    for model_name in test_models:
        print(f"Testing {model_name}...")
        try:
            response = await client.aio.models.generate_content(
                model=model_name,
                contents="Say hello"
            )
            print(f"  ✅ SUCCESS: {response.text[:50]}...")
        except Exception as e:
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg:
                print(f"  ❌ QUOTA EXHAUSTED")
            elif "NOT_FOUND" in error_msg:
                print(f"  ❌ NOT FOUND")
            else:
                print(f"  ❌ ERROR: {error_msg[:100]}")
        print()

if __name__ == "__main__":
    asyncio.run(main())

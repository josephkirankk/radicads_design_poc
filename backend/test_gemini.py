from google import genai
from app.core.config import settings
import asyncio

print("\n=== DIAGNOSING GEMINI AI ISSUE ===\n")

# Test 1: Client initialization
print("1. Testing client initialization...")
try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    print("   ✓ Client created successfully")
    print(f"   API Key length: {len(settings.GEMINI_API_KEY)}")
except Exception as e:
    print(f"   ✗ Client creation failed: {e}")
    exit(1)

# Test 2: Simple sync call
print("\n2. Testing simple synchronous call...")
try:
    resp = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents='Say hello in 3 words'
    )
    print(f"   ✓ Sync call successful!")
    print(f"   Response: {resp.text[:100]}")
except Exception as e:
    print(f"   ✗ Sync call failed: {str(e)[:300]}")

# Test 3: Async call
print("\n3. Testing async call (like in our service)...")
async def test_async():
    try:
        resp = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents='Say goodbye in 3 words'
        )
        print(f"   ✓ Async call successful!")
        print(f"   Response: {resp.text[:100]}")
        return True
    except Exception as e:
        print(f"   ✗ Async call failed: {str(e)[:300]}")
        return False

success = asyncio.run(test_async())

if success:
    print("\n✅ DIAGNOSIS: Gemini API is working!")
    print("   The issue is likely in the service implementation.")
else:
    print("\n❌ DIAGNOSIS: Gemini API calls are failing!")
    print("   Check the API key or network connection.")

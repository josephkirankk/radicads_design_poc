from google import genai
from app.core.config import settings

print("\n=== CHECKING API KEY AND ERROR DETAILS ===\n")

client = genai.Client(api_key=settings.GEMINI_API_KEY)

try:
    resp = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents='Hello'
    )
    print(f"✓ Success: {resp.text}")
except Exception as e:
    print(f"✗ Error Type: {type(e).__name__}")
    print(f"✗ Full Error: {e}")
    
    # Try with correct model name
    print("\n--- Trying with gemini-1.5-flash instead ---")
    try:
        resp2 = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents='Hello'
        )
        print(f"✓ Success with 1.5-flash: {resp2.text[:50]}")
    except Exception as e2:
        print(f"✗ Also failed: {e2}")

import requests
import json

# Test the generate design endpoint
url = "http://localhost:8000/api/v1/ai/layout/generate"
payload = {
    "prompt": "Create a modern tech startup ad with blue colors"
}

print("Testing real API call...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

response = requests.post(url, json=payload)
print(f"\nStatus Code: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.json(), indent=2))

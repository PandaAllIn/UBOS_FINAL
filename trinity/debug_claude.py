
import sys
import os
from dotenv import load_dotenv

# Load env manually to verify
load_dotenv("/etc/janus/trinity.env")
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"DEBUG: ANTHROPIC_API_KEY present? {bool(api_key)}")
if api_key:
    print(f"DEBUG: Key prefix: {api_key[:15]}...")

try:
    import anthropic
    print("DEBUG: anthropic imported successfully")
except ImportError as e:
    print(f"DEBUG: anthropic import failed: {e}")

try:
    client = anthropic.Anthropic(api_key=api_key)
    print("DEBUG: Anthropic client initialized successfully")
    
    # Test simple call
    print("DEBUG: Attempting API call...")
    resp = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[{"role": "user", "content": "Ping"}]
    )
    print(f"DEBUG: Response: {resp.content[0].text}")
except Exception as e:
    print(f"DEBUG: Client init/call failed: {e}")

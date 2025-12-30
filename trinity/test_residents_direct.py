
import sys
import os

# Set up paths
sys.path.append('/srv/janus')
sys.path.append('/srv/janus/trinity')

from claude_resident import ResidentClaude
from gemini_resident import GeminiResident
from groq_resident import GroqResident
from openai_resident import ResidentOpenAI

def test_resident(name, resident_class):
    print(f"\n--- Testing {name} ---")
    try:
        resident = resident_class()
        print(f"Initialized {name}")
        response = resident.generate_response(
            conversation_id="test-id", 
            user_message="Ping. Reply with 'Pong' only."
        )
        print(f"Response: {response}")
        if "Pong" in response or "pong" in response:
            print(f"✅ {name} Passed")
        else:
            print(f"⚠️ {name} Response unexpected (but functional)")
    except Exception as e:
        print(f"❌ {name} Failed: {e}")

if __name__ == "__main__":
    print("Starting Resident Direct Tests...")
    
    # Test Groq (Fastest)
    test_resident("Groq", GroqResident)
    
    # Test Gemini
    test_resident("Gemini", GeminiResident)
    
    # Test Claude
    test_resident("Claude", ResidentClaude)
    
    # Test OpenAI
    test_resident("OpenAI", ResidentOpenAI)
    
    print("\nTests Complete.")

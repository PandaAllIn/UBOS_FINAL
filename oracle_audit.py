
import sys
import time
from pathlib import Path

# Add trinity to the python path
trinity_path = Path('/srv/janus/trinity/')
sys.path.insert(0, str(trinity_path))

from oracle_bridge import OracleBridge
from config import load_configuration
from dotenv import load_dotenv

def measure_time(func, *args, **kwargs):
    """Measures the execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def main():
    """Tests all OracleBridge endpoints."""
    print("--- Oracle Bridge Verification ---")

    # Explicitly load the environment file
    load_dotenv("/srv/janus/config/.env")
    _, api_keys = load_configuration()

    if not all([api_keys.perplexity, api_keys.wolfram, api_keys.data_commons, api_keys.groq]):
        print("❌ Critical API keys are missing. Aborting test.")
        return

    bridge = OracleBridge(api_keys)

    # --- Perplexity Test ---
    print("\n[1] Testing Perplexity (research)...")
    try:
        result, duration = measure_time(bridge.research, "Latest EU digital infrastructure funding programs 2025")
        if "error" not in result.lower() and "unavailable" not in result.lower():
            print(f"✅ Status: Success")
            print(f"   Response Time: {duration:.2f}s")
            print(f"   Sample Output: {result[:150].strip()}...")
        else:
            print(f"❌ Status: Failed")
            print(f"   Response: {result}")
    except Exception as e:
        print(f"❌ Status: Exception - {e}")

    # --- Wolfram Alpha Test ---
    print("\n[2] Testing Wolfram Alpha...")
    try:
        result, duration = measure_time(bridge.wolfram, "GDP of Andalusia Spain")
        if "error" not in result.lower() and "unavailable" not in result.lower():
            print(f"✅ Status: Success")
            print(f"   Response Time: {duration:.2f}s")
            print(f"   Sample Output: {result.strip()}")
        else:
            print(f"❌ Status: Failed")
            print(f"   Response: {result}")
    except Exception as e:
        print(f"❌ Status: Exception - {e}")

    # --- DataCommons Test ---
    print("\n[3] Testing DataCommons...")
    try:
        # First, resolve the place to get a DCID
        place_name = "Malaga, Spain"
        dcid_result, _ = measure_time(bridge.resolve_place, place_name)
        dcid = dcid_result.strip()
        if "dcid:" not in dcid:
             print(f"❌ Status: Failed to resolve DCID for {place_name}")
             print(f"   Response: {dcid_result}")
        else:
            result, duration = measure_time(bridge.query_economics, dcid)
            if "error" not in result.lower() and "unavailable" not in result.lower():
                print(f"✅ Status: Success")
                print(f"   Response Time: {duration:.2f}s")
                print(f"   Sample Output: {result.strip()}")
            else:
                print(f"❌ Status: Failed")
                print(f"   Response: {result}")
    except Exception as e:
        print(f"❌ Status: Exception - {e}")


    # --- Groq API Test ---
    print("\n[4] Testing Groq API (fast_think)...")
    try:
        result, duration = measure_time(bridge.fast_think, "Summarize the following text: The quick brown fox jumps over the lazy dog.")
        if "error" not in result.lower() and "unavailable" not in result.lower():
            print(f"✅ Status: Success")
            print(f"   Response Time: {duration:.2f}s")
            print(f"   Sample Output: {result.strip()}")
        else:
            print(f"❌ Status: Failed")
            print(f"   Response: {result}")
    except Exception as e:
        print(f"❌ Status: Exception - {e}")


if __name__ == "__main__":
    main()

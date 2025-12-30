
import requests
import time
import json

def main():
    """Tests the OpenAI resident's model switching capabilities."""
    print("--- OpenAI Resident Model Audit ---")

    base_url = "http://localhost:9085"
    prompt = "Explain the concept of 'separation of powers' in a democracy in 50 words."

    task_types = ["fast", "flagship", "reasoning"]

    for task in task_types:
        print(f"\n[+] Testing task_type: {task}")
        payload = {
            "prompt": prompt,
            "task_type": task,
            "temperature": 0.5,
            "max_tokens": 100
        }
        try:
            start_time = time.time()
            response = requests.post(f"{base_url}/inference", json=payload)
            duration = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Success")
                print(f"     Model Used: {data.get('model')}")
                print(f"     Response Time: {duration:.2f}s")
                print(f"     Response: {data.get('response', '').strip()}")
            else:
                print(f"  ❌ Failed with status {response.status_code}")
                print(f"     Response: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    main()

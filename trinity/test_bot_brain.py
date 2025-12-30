
import sys
import os

# Add the trinity directory to path
sys.path.append('/srv/janus/trinity')

from janus_orchestrator import plan_from_text, DelegationPlan

test_cases = [
    ("/use claude strategy for spain", "override", "claude"),
    ("@gemini check system status", "override", "gemini"),
    ("what is the strategy for monetization?", "keyword", "claude"),
    ("deploy the new code", "keyword", "gemini"),
    ("quick summary of news", "keyword", "perplexity"), # News -> Perplexity
    ("quick draft of an email", "keyword", "groq"), # Quick/Draft -> Groq
    ("write me a poem", "keyword", "openai"), # Default fallthrough
    ("/oracle perplexity xylella in spain", "oracle", "perplexity")
]

print("Running Bot Brain Tests...")
failed = 0
for text, expected_mode, expected_target in test_cases:
    plan = plan_from_text(text)
    if not plan:
        print(f"FAIL: '{text}' -> None")
        failed += 1
        continue
    
    if plan.mode == expected_mode and plan.target == expected_target:
        print(f"PASS: '{text}' -> {plan.mode}:{plan.target}")
    else:
        print(f"FAIL: '{text}' -> {plan.mode}:{plan.target} (Expected {expected_mode}:{expected_target})")
        failed += 1

if failed == 0:
    print("\nALL TESTS PASSED")
else:
    print(f"\n{failed} TESTS FAILED")

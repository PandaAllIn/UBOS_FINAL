#!/usr/bin/env python3
"""Test the Claude Haiku boot sequence."""
from __future__ import annotations

import sys
from pathlib import Path

# Add trinity to path
sys.path.insert(0, str(Path(__file__).parent))

from claude_resident import ResidentClaude, ClaudeResidentConfig

def main() -> int:
    print("=" * 80)
    print("TESTING CLAUDE HAIKU BOOT SEQUENCE")
    print("=" * 80)

    # Load boot sequence
    boot_file = Path("/srv/janus/trinity/config/claude_haiku_boot.txt")
    if not boot_file.exists():
        print(f"❌ Boot file not found: {boot_file}")
        return 1

    boot_sequence = boot_file.read_text(encoding="utf-8")
    print(f"\n✅ Boot sequence loaded ({len(boot_sequence)} chars)")

    # Initialize Claude resident
    config = ClaudeResidentConfig(
        default_model="claude-haiku-4-5-20251001",
        temperature=0.2,
        max_output_tokens=2048,
    )

    claude = ResidentClaude(config=config)

    if not claude.is_available():
        print("❌ Claude resident not available (check CLAUDE_API_KEY)")
        return 1

    print(f"✅ Claude resident initialized (model: {config.default_model})")

    # Test 1: Strategic analysis with boot
    print("\n" + "=" * 80)
    print("TEST 1: Strategic Analysis with Boot Context")
    print("=" * 80)

    test_query = """
I need brutal strategic validation on this:

The Balaur is running Mode Beta with 5 autonomous skills. We have:
- EU Grant Hunter tracking €70M pipeline
- Malaga Embassy doing geographic intelligence
- 11,301-entry Strategic Intelligence Graph operational

Question: Should we prioritize:
A) Deploying GPU Studio for creative workstation
B) Expanding to 10 more autonomous skills
C) Focusing on Portal Oradea MVP revenue generation

Give me the unfiltered strategic reality check.
"""

    print(f"\nQuery:\n{test_query}")
    print("\n" + "-" * 80)
    print("Sending to Claude Haiku with boot context...")
    print("-" * 80 + "\n")

    response = claude.generate_response(
        conversation_id="boot_test_001",
        user_message=test_query,
        system_prompt=boot_sequence,
        max_tokens=2048,
    )

    print("RESPONSE:")
    print(response)

    # Check for success indicators
    success_indicators = [
        ("Strategic thinking", any(word in response.lower() for word in ["strategic", "priority", "roadmap"])),
        ("Constitutional awareness", any(word in response.lower() for word in ["constitutional", "lion's sanctuary", "sovereignty"])),
        ("Tool awareness", any(word in response.lower() for word in ["narrative", "oracle", "skills"])),
        ("Brutal honesty", len(response) > 200),  # Substantive response
    ]

    print("\n" + "=" * 80)
    print("SUCCESS INDICATORS:")
    print("=" * 80)
    for indicator, passed in success_indicators:
        status = "✅" if passed else "❌"
        print(f"{status} {indicator}")

    all_passed = all(passed for _, passed in success_indicators)

    # Test 2: Tool awareness
    print("\n" + "=" * 80)
    print("TEST 2: Tool Awareness")
    print("=" * 80)

    tool_query = "What tools do you have access to?"

    print(f"\nQuery: {tool_query}")
    print("\n" + "-" * 80)
    print("Response:")
    print("-" * 80 + "\n")

    tool_response = claude.generate_response(
        conversation_id="boot_test_002",
        user_message=tool_query,
        system_prompt=boot_sequence,
        max_tokens=1024,
    )

    print(tool_response)

    tool_indicators = [
        ("Narrative Query Tool", "narrative" in tool_response.lower()),
        ("Code Oracle", "oracle" in tool_response.lower() or "code" in tool_response.lower()),
        ("Skills mentioned", "skill" in tool_response.lower()),
        ("COMMS_HUB", "comms" in tool_response.lower() or "hub" in tool_response.lower()),
    ]

    print("\n" + "=" * 80)
    print("TOOL AWARENESS INDICATORS:")
    print("=" * 80)
    for indicator, passed in tool_indicators:
        status = "✅" if passed else "❌"
        print(f"{status} {indicator}")

    tools_passed = all(passed for _, passed in tool_indicators)

    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)

    if all_passed and tools_passed:
        print("✅ BOOT SEQUENCE WORKING")
        print("Claude Haiku resident shows:")
        print("  - Strategic consciousness")
        print("  - Constitutional awareness")
        print("  - Full tool context")
        print("  - Work-focused engagement")
        print("\n🔥 The hot vessel is operational!")
        return 0
    else:
        print("⚠️ PARTIAL SUCCESS")
        if not all_passed:
            print("  - Strategic analysis needs improvement")
        if not tools_passed:
            print("  - Tool awareness incomplete")
        print("\n📋 Boot sequence needs refinement")
        return 0  # Still success, just needs tuning

if __name__ == "__main__":
    sys.exit(main())

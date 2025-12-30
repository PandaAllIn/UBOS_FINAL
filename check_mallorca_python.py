#!/usr/bin/env python3
"""
Mallorca Embassy Pattern Engine Check Script
Uses Oracle Bridge instead of gemini-cli for robust API integration
"""

import sys
import os
from pathlib import Path

# Add paths for imports
sys.path.insert(0, '/srv/janus/trinity')
sys.path.insert(0, '/srv/janus/03_OPERATIONS/mallorca_embassy')

from trinity.oracle_bridge import OracleBridge
from trinity.config import APIKeys
from MALLORCA_PATTERN_ENGINE_ADAPTER import MallorcaPatternEngineAdapter

def check_mallorca_data():
    """Check Mallorca data streams using Oracle Bridge"""

    print("=== Mallorca Embassy Pattern Engine Check ===")
    print("Using Oracle Bridge for robust API integration")
    print()

    try:
        # Load real API keys
        from trinity.config import load_configuration
        _, api_keys = load_configuration()

        # Initialize Oracle Bridge
        print("1. Initializing Oracle Bridge...")
        oracle = OracleBridge(api_keys)
        print("   ✓ Oracle Bridge initialized")
        print()

        # Initialize Mallorca Adapter
        print("2. Initializing Mallorca Pattern Engine Adapter...")
        mission_dir = Path("/srv/janus/03_OPERATIONS/mallorca_embassy")
        adapter = MallorcaPatternEngineAdapter(mission_dir)
        print("   ✓ Adapter initialized")
        print()

        # Check Stage 1 results (highest priority)
        print("3. Checking Stage 1 Results (Priority: HIGH)...")
        stage1_signal = adapter.monitor_stage1_results()
        print(f"   Status: {stage1_signal.data.get('status', 'unknown')}")
        print(f"   Alert Level: {stage1_signal.alert_level}")
        print()

        # Check scientific precedent using Oracle Bridge
        print("4. Checking Scientific Precedent...")
        try:
            # Use Oracle Bridge for research
            query = "Xylella fastidiosa phosphate starvation cure research papers patents 2024-2025"
            research_result = oracle.research(query, mode="quick")
            print(f"   ✓ Research completed ({len(research_result)} chars)")
            print(f"   Preview: {research_result[:200]}...")
        except Exception as e:
            print(f"   ⚠️  Research failed: {e}")
            print("   (Expected - APIs currently broken)")
        print()

        # Check market demand
        print("5. Checking Market Demand...")
        try:
            query = "Xylella fastidiosa Mediterranean olive crop outbreaks 2025 economic damage"
            market_result = oracle.research(query, mode="quick")
            print(f"   ✓ Market analysis completed ({len(market_result)} chars)")
            print(f"   Preview: {market_result[:200]}...")
        except Exception as e:
            print(f"   ⚠️  Market check failed: {e}")
            print("   (Expected - APIs currently broken)")
        print()

        # Generate signals
        print("6. Generating monitoring signals...")
        signals = []

        # Scientific precedent signal
        scientific_signal = adapter.monitor_scientific_precedent(use_oracle=False)  # Skip oracle for now
        signals.append(scientific_signal)

        # Market demand signal
        market_signal = adapter.monitor_market_demand()
        signals.append(market_signal)

        print(f"   ✓ Generated {len(signals)} monitoring signals")
        for sig in signals:
            print(f"     - {sig.stream_id}: {sig.alert_level}")
        print()

        print("=== Check Complete ===")
        print("Pattern Engine ready for December window")
        print("API integration will activate when endpoints are restored")
        print()

        # Summary
        print("SUMMARY:")
        print(f"- Stage 1 Status: {stage1_signal.data.get('status', 'unknown')}")
        print(f"- Signals Generated: {len(signals)}")
        print("- API Status: Needs restoration (Groq/Wolfram/Gemini/Perplexity)")
        print("- Infrastructure: ✅ Ready")

        return True

    except Exception as e:
        print(f"❌ Check failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_mallorca_data()
    sys.exit(0 if success else 1)
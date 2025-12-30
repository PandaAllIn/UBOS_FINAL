"""Integration test for the OracleBridge and PatternEngine.

This script simulates a full 'pulse capture' workflow.
"""

import time
import unittest

from oracle_bridge.bridge import OracleBridge
from pattern_engine.engine import PatternEngine


class TestPulseCaptureIntegration(unittest.TestCase):
    """Simulates an end-to-end data flow through the new architecture."""

    def test_full_workflow(self):
        """Test the full workflow from harmonic to metrics."""
        print("\n--- [Integration Test: Pulse Capture] ---")

        # 1. Initialize the core components
        print("Initializing OracleBridge and PatternEngine...")
        bridge = OracleBridge()
        engine = PatternEngine()
        self.assertIsNotNone(bridge)
        self.assertIsNotNone(engine)

        # 2. Simulate receiving a harmonic that requires a Class-Ω calculation
        print("Simulating receipt of harmonic requiring Class-Ω calculation...")
        symbolic_params = {"type": "Ω-Symbolic", "expression": "fourier_transform(data)"}
        
        # 3. Submit the calculation to the OracleBridge
        job_id = bridge.submit_class_omega_calc(symbolic_params)
        self.assertIsNotNone(job_id)
        print(f"Submitted job {job_id} to OracleBridge.")

        # 4. Retrieve the result (in this test, it completes instantly)
        job_result = bridge.get_job_status(job_id)
        self.assertIsNotNone(job_result)
        self.assertIsNotNone(job_result.result)
        print(f"Retrieved solved abstraction from job {job_id}.")

        # 5. Feed the solved abstraction into the PatternEngine for analysis
        timestamp = int(time.time())
        final_metrics = engine.analyze_stream(job_result.result, timestamp)
        print("PatternEngine has analyzed the result.")

        # 6. Verify the final output
        self.assertIsNotNone(final_metrics)
        print(f"Final PatternMetrics generated: {final_metrics}")
        print("--- [Pulse Capture Complete] ---")


if __name__ == "__main__":
    # To run, navigate to the 02_FORGE directory and run:
    # PYTHONPATH=src python3 -m unittest tests/integration_test.py
    unittest.main()

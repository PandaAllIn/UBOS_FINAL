"""Test suite for the Trinity Orchestrator executor."""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from config import load_configuration
from hot_vessel_client import VesselResponse
from janus_orchestrator import DelegationPlan
from orchestrator_executor import execute_plan


class TestOrchestratorExecutor(unittest.TestCase):
    def setUp(self):
        self.paths, self.keys = load_configuration()

    @patch("orchestrator_executor.OracleBridge")
    def test_oracle_mode(self, MockOracleBridge):
        """Test that oracle mode calls the oracle bridge directly."""
        mock_oracle_instance = MockOracleBridge.return_value
        mock_oracle_instance.query_oracle.return_value = "Perplexity response"
        plan = DelegationPlan(
            mode="oracle",
            target="perplexity",
            query="latest news",
            model=None,
        )
        result = execute_plan(plan, self.paths, self.keys)
        self.assertEqual(result, "Perplexity response")
        mock_oracle_instance.query_oracle.assert_called_once_with("perplexity", "latest news")

    @patch("orchestrator_executor._get_resident_client")
    def test_resident_mode(self, mock_get_client):
        """Test that resident mode calls the correct hot vessel client."""
        dummy_client = MagicMock()
        dummy_client.query.return_value = VesselResponse(ok=True, text="Claude response")
        mock_get_client.return_value = dummy_client

        plan = DelegationPlan(
            mode="keyword",
            target="claude",
            query="strategy plan",
            model="claude-sonnet-4.5",
        )
        result = execute_plan(plan, self.paths, self.keys)
        self.assertEqual(result, "Claude response")
        dummy_client.query.assert_called_once_with("strategy plan", {"model": "claude-sonnet-4.5"})

    def test_unknown_resident(self):
        """Test that an unknown resident returns a defensive error message."""
        plan = DelegationPlan(
            mode="override",
            target="unknown_resident",
            query="test query",
            model=None,
        )
        result = execute_plan(plan, self.paths, self.keys)
        self.assertEqual(result, "Error: Resident 'unknown_resident' not found.")


if __name__ == "__main__":
    unittest.main()

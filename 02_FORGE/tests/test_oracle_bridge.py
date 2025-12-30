"""Unit tests for the OracleBridge skeleton."""

import unittest

from oracle_bridge.bridge import OracleBridge, OracleJob, JobStatus


class TestOracleBridgeSkeleton(unittest.TestCase):
    """Tests the basic structure and functionality of the OracleBridge."""

    def setUp(self):
        """Set up the test case."""
        self.bridge = OracleBridge()
        self.dummy_params = {"expression": "2+2"}

    def test_bridge_initialization(self):
        """Test that the OracleBridge initializes correctly."""
        self.assertIsInstance(self.bridge, OracleBridge)
        self.assertIsInstance(self.bridge.jobs, dict)

    def test_submit_class_omega_calc(self):
        """Test the submission of a Class-Ω job."""
        job_id = self.bridge.submit_class_omega_calc(self.dummy_params)
        self.assertIn(job_id, self.bridge.jobs)
        
        job = self.bridge.jobs[job_id]
        self.assertIsInstance(job, OracleJob)
        self.assertEqual(job.status, JobStatus.COMPLETED) # Placeholder immediately completes
        self.assertIsNotNone(job.result)

    def test_get_job_status(self):
        """Test retrieving the status of a job."""
        job_id = self.bridge.submit_class_omega_calc(self.dummy_params)
        retrieved_job = self.bridge.get_job_status(job_id)

        self.assertIsNotNone(retrieved_job)
        self.assertEqual(retrieved_job.job_id, job_id)
        self.assertEqual(retrieved_job.status, JobStatus.COMPLETED)

    def test_query_datacommons(self):
        """Test the placeholder for DataCommons query."""
        result = self.bridge.query_datacommons("test query")
        self.assertIn("historical_data", result)


if __name__ == "__main__":
    # To run, navigate to the 02_FORGE directory and run:
    # PYTHONPATH=src python3 -m unittest tests/test_oracle_bridge.py
    unittest.main()

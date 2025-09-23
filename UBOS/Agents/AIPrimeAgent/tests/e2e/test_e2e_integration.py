"""E2E integration test (skipped by default).

Requires RUN_UBOS_E2E=1 and valid API keys:
- GEMINI_API_KEY for Librarian
- PERPLEXITY_API_KEY for Research Agent CLI
"""

from pathlib import Path
import json
import os
import subprocess
import sys
import time

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


pytestmark = pytest.mark.e2e


@pytest.mark.skipif(
    os.getenv("RUN_UBOS_E2E") != "1" or not os.getenv("GEMINI_API_KEY") or not os.getenv("PERPLEXITY_API_KEY"),
    reason="RUN_UBOS_E2E=1 and API keys required",
)
def test_e2e_prime_with_real_agents(tmp_path: Path):  # pragma: no cover - networked integration
    books_path = Path(PROJECT_ROOT).parents[2] / "SystemFundamentals" / "Books"
    env = os.environ.copy()
    env["UBOS_BOOKS_PATH"] = str(books_path)

    # Start Librarian server
    ml_cmd = [
        sys.executable,
        "-c",
        "from master_librarian.api.app import create_app; app=create_app(); app.run(host='127.0.0.1', port=5020)",
    ]
    ml_env = env.copy()
    ml_env["PYTHONPATH"] = str((PROJECT_ROOT / "../KnowledgeAgent/MasterLibrarianAgent").resolve())
    ml = subprocess.Popen(ml_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ml_env)
    time.sleep(2)

    try:
        transcript = tmp_path / "transcript.jsonl"
        prime_cmd = [
            sys.executable,
            "-m",
            "ai_prime_agent.cli",
            "research-synthesize",
            "--query",
            "Deployment roadmap for UBOS multi-agent system",
            "--depth",
            "medium",
            "--librarian-url",
            "http://127.0.0.1:5020",
            "--research-cli",
            str((PROJECT_ROOT / "../ResearchAgent/ubos_research_agent.py").resolve()),
            "--transcript",
            str(transcript),
        ]
        prime_env = env.copy()
        prime_env["PYTHONPATH"] = str((PROJECT_ROOT).resolve())
        out = subprocess.check_output(prime_cmd, env=prime_env, text=True, timeout=180)
        data = json.loads(out)
        assert data.get("consultation", {}).get("recommendations"), "Expected Librarian recommendations"
        assert data.get("research", {}).get("citations"), "Expected Perplexity citations"
        assert (transcript.exists() and transcript.stat().st_size > 0), "Transcript not written"
    finally:
        ml.terminate()
        try:
            ml.wait(timeout=5)
        except Exception:
            ml.kill()


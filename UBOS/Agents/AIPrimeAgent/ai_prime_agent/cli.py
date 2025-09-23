"""
AI Prime Agent CLI (MVP)

Philosophy: Strategic Starting Points
Purpose: Run the Research & Synthesize pilot with minimal setup.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_prime_agent.blueprint.schema import StrategicBlueprint, validate_blueprint_dict, load_blueprint
from ai_prime_agent.orchestrator import AIPrimeAgent
from ai_prime_agent.adapters import knowledge as knowledge_adapter
from ai_prime_agent.adapters import research as research_adapter
from ai_prime_agent.orchestrator.workflows import research_synthesize


def _minimal_blueprint() -> StrategicBlueprint:
    return validate_blueprint_dict(
        {
            "blueprint_metadata": {
                "schema_version": "1.0",
                "document_version": "1.0.0",
                "last_updated_utc": "2025-09-22T10:00:00Z",
                "review_cadence_days": 7,
                "ubos_alignment": ["Blueprint Thinking", "Strategic Pause"],
            },
            "missionStatement": "Coordinate agents to multiply capacity.",
            "corePrinciples": [
                {"principleId": "UBOS-P-01", "statement": "Blueprint Thinking"}
            ],
            "activeGoals": [],
            "agentRegistry": [],
            "guardrails": {},
        }
    )


def main() -> None:  # pragma: no cover - CLI utility
    parser = argparse.ArgumentParser(description="UBOS AI Prime Agent CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    rs = sub.add_parser("research-synthesize", help="Run the Research & Synthesize workflow")
    rs.add_argument("--query", required=True, help="Research query")
    rs.add_argument("--depth", choices=["quick", "medium", "deep"], default="medium")
    rs.add_argument("--blueprint", help="Path to blueprint JSON/YAML file")
    rs.add_argument("--transcript", help="Path to write JSONL transcript")
    rs.add_argument("--report-dir", help="Directory to write report artifacts (JSON/MD/Mermaid)")
    # Optional real adapters
    rs.add_argument("--librarian-url", help="Master Librarian base URL for REST adapter (e.g., http://127.0.0.1:5000)")
    rs.add_argument("--librarian-auth", help="Bearer token for Librarian REST")
    rs.add_argument("--librarian-timeout", type=float, default=30.0, help="Timeout (s) for Librarian REST adapter")
    rs.add_argument("--research-cli", help="Path to ubos_research_agent.py for CLI adapter")
    rs.add_argument("--python", default="python3", help="Python executable for CLI adapter")
    rs.add_argument("--research-timeout", type=float, default=60.0, help="Timeout (s) for Research CLI adapter")

    args = parser.parse_args()

    if args.command == "research-synthesize":
        bp = load_blueprint(args.blueprint) if args.blueprint else _minimal_blueprint()
        prime = AIPrimeAgent(blueprint=bp)
        comps = prime.components
        if args.transcript:
            from ai_prime_agent.telemetry.transcript import TranscriptLogger
            logger = TranscriptLogger(args.transcript)
            comps.bus.add_observer(logger.append)

        # Register adapters: choose real adapters if args provided, else defaults
        if args.research_cli:
            from ai_prime_agent.adapters.research_cli import register_cli_with_prime as register_research_cli
            register_research_cli(
                agent_id="A-re-cli",
                registry=comps.registry,
                register_handler=prime.register_adapter,
                python_exe=args.python,
                agent_script=args.research_cli,
                timeout=args.research_timeout,
            )
        else:
            research_adapter.register_with_prime(agent_id="A-re-001", registry=comps.registry, register_handler=prime.register_adapter)

        if args.librarian_url:
            from ai_prime_agent.adapters.librarian_http import register_http_with_prime as register_librarian_http
            register_librarian_http(
                agent_id="A-ml-http",
                registry=comps.registry,
                register_handler=prime.register_adapter,
                base_url=args.librarian_url,
                auth_token=args.librarian_auth,
                timeout=args.librarian_timeout,
            )
        else:
            knowledge_adapter.register_with_prime(agent_id="A-ml-001", registry=comps.registry, register_handler=prime.register_adapter)

        result = research_synthesize.run(prime, query=args.query, depth=args.depth)
        if args.report_dir:
            from ai_prime_agent.reporting.reporter import write_report
            artifacts = write_report(result, args.report_dir)
            result["artifacts"] = artifacts
        print(json.dumps(result, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()

from __future__ import annotations

from janus_orchestrator import (
    DelegationPlan,
    keyword_route,
    parse_mention_command,
    parse_use_command,
    plan_from_text,
)


def test_parse_use_command_with_model_returns_override() -> None:
    plan = parse_use_command("/use openai:gpt-5-mini handle this request")
    assert plan is not None
    assert plan.mode == "override"
    assert plan.target == "openai"
    assert plan.model == "gpt-5-mini"
    assert plan.query == "handle this request"


def test_parse_use_command_invalid_target_returns_none() -> None:
    plan = parse_use_command("/use randommodel do the thing")
    assert plan is None


def test_parse_mention_command_routes_to_perplexity() -> None:
    plan = parse_mention_command("@perplexity Provide latest sources on Mode Beta")
    assert plan is not None
    assert plan.mode == "oracle"
    assert plan.target == "perplexity"
    assert plan.query.startswith("Provide latest sources")


def test_keyword_route_directs_web_queries_to_perplexity() -> None:
    plan = keyword_route("Give me the latest market news with citations")
    assert plan.target == "perplexity"
    assert plan.mode == "keyword"


def test_keyword_route_directs_coding_queries_to_openai_codex() -> None:
    plan = keyword_route("Please refactor this code snippet for better tests")
    assert plan.target == "openai"
    assert plan.model == "gpt-5-codex"


def test_plan_from_text_prioritizes_use_command_over_keywords() -> None:
    text = "/use claude craft a strategic roadmap even though this mentions code"
    plan = plan_from_text(text)
    assert isinstance(plan, DelegationPlan)
    assert plan.target == "claude"
    assert plan.mode == "override"


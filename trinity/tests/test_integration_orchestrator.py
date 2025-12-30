from __future__ import annotations

from dataclasses import dataclass

from janus_orchestrator import DelegationPlan, plan_from_text


class FakeOracleBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def research(self, query: str) -> str:
        self.calls.append(("perplexity", query))
        return "perplexity-result"

    def wolfram(self, query: str) -> str:
        self.calls.append(("wolfram", query))
        return "wolfram-result"

    def fast_think(self, query: str) -> str:
        self.calls.append(("groq", query))
        return "groq-result"


@dataclass
class FakeResident:
    name: str

    def __post_init__(self) -> None:
        self.calls: list[tuple[str, str, str | None]] = []

    def generate_response(self, conversation_id: str, query: str, model: str | None = None) -> str:
        self.calls.append((conversation_id, query, model))
        return f"{self.name}:{query}"


class Dispatcher:
    def __init__(self) -> None:
        self.oracle = FakeOracleBridge()
        self.claude = FakeResident("claude")
        self.gemini = FakeResident("gemini")

    def dispatch(self, text: str) -> tuple[DelegationPlan, str]:
        plan = plan_from_text(text)
        result = self._execute(plan)
        return plan, result

    def _execute(self, plan: DelegationPlan) -> str:
        if plan.mode in {"override", "keyword"}:
            if plan.target == "claude":
                return self.claude.generate_response("conv", plan.query, plan.model)
            if plan.target == "gemini":
                return self.gemini.generate_response("conv", plan.query, plan.model)
            if plan.target == "groq":
                return self.oracle.fast_think(plan.query)
            if plan.target == "perplexity":
                return self.oracle.research(plan.query)
            if plan.target == "wolfram":
                return self.oracle.wolfram(plan.query)
            if plan.target == "fast":
                return self.oracle.fast_think(plan.query)
        if plan.mode == "oracle":
            if plan.target == "perplexity":
                return self.oracle.research(plan.query)
            if plan.target == "wolfram":
                return self.oracle.wolfram(plan.query)
            if plan.target == "fast":
                return self.oracle.fast_think(plan.query)
        raise AssertionError(f"Unhandled plan: {plan}")


def test_latest_ai_news_routes_to_perplexity():
    dispatcher = Dispatcher()
    plan, result = dispatcher.dispatch("latest AI news")
    assert plan.mode == "keyword"
    assert plan.target == "perplexity"
    assert dispatcher.oracle.calls[-1] == ("perplexity", "latest AI news")
    assert result == "perplexity-result"


def test_compute_derivative_routes_to_wolfram():
    dispatcher = Dispatcher()
    plan, result = dispatcher.dispatch("compute derivative of x^2")
    assert plan.target == "wolfram"
    assert dispatcher.oracle.calls[-1][0] == "wolfram"
    assert "wolfram" in result


def test_strategy_query_routes_to_claude_resident():
    dispatcher = Dispatcher()
    plan, result = dispatcher.dispatch("strategy for Phase 4")
    assert plan.target == "claude"
    assert dispatcher.claude.calls[-1][1] == "strategy for Phase 4"
    assert result.startswith("claude:")


def test_deploy_query_routes_to_gemini_resident():
    dispatcher = Dispatcher()
    plan, result = dispatcher.dispatch("deploy this service to production")
    assert plan.target == "gemini"
    assert dispatcher.gemini.calls[-1][1] == "deploy this service to production"
    assert result.startswith("gemini:")


def test_quick_summary_routes_to_groq_fast_think():
    dispatcher = Dispatcher()
    plan, result = dispatcher.dispatch("quick summary please")
    assert plan.target == "groq"
    assert dispatcher.oracle.calls[-1] == ("groq", "quick summary please")
    assert result == "groq-result"

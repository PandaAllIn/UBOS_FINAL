from __future__ import annotations

from dataclasses import dataclass

import pytest

from resident_toolkit import (
    PromptWithTools,
    ToolEnvironment,
    enrich_prompt_with_tools,
)


@dataclass
class DummyLibrarian:
    responses: dict[str, str]

    def read_file(self, path: str) -> str:
        return self.responses.get(path, "")

    def list_files(self, directory: str) -> list[str]:
        return [f"{directory}/file1.txt", f"{directory}/file2.txt"]

    def search_content(self, pattern: str, directory: str) -> dict[str, list[str]]:
        return {f"{directory}/match.txt": [f"1: {pattern} found"]}


@dataclass
class DummyOracle:
    def fast_think(self, prompt: str) -> str:
        return f"fast:{prompt}"

    def query_oracle(self, target: str, query: str) -> str:
        return f"{target}:{query}"


@pytest.fixture
def tool_env() -> ToolEnvironment:
    return ToolEnvironment(
        librarian=DummyLibrarian(responses={"/srv/janus/README.md": "Welcome to Janus"}),
        oracle=DummyOracle(),
    )


def test_enrich_prompt_without_tools(tool_env: ToolEnvironment) -> None:
    result = enrich_prompt_with_tools("Explain the forge mantra.", tool_env)
    assert isinstance(result, PromptWithTools)
    assert result.prompt == "Explain the forge mantra."
    assert result.tool_context == ""
    assert result.executed_commands == ()


def test_enrich_prompt_with_librarian(tool_env: ToolEnvironment) -> None:
    prompt = "Provide summary.\n[TOOL: librarian.read_file('/srv/janus/README.md')]"
    result = enrich_prompt_with_tools(prompt, tool_env)
    assert "Tool Output" in result.prompt
    assert "Welcome to Janus" in result.tool_context
    assert result.executed_commands == ("librarian.read_file('/srv/janus/README.md')",)


def test_enrich_prompt_with_oracle(tool_env: ToolEnvironment) -> None:
    prompt = "[TOOL: oracle.fast_think('speed run')]"
    result = enrich_prompt_with_tools(prompt, tool_env)
    assert result.prompt.startswith("[Tool Output]")
    assert "fast:speed run" in result.tool_context
    assert result.executed_commands == ("oracle.fast_think('speed run')",)


def test_enrich_prompt_handles_errors(tool_env: ToolEnvironment) -> None:
    prompt = "Check.\n[TOOL: oracle.unknown('x')]"
    result = enrich_prompt_with_tools(prompt, tool_env)
    assert "ERROR" in result.tool_context
    assert result.executed_commands == ("oracle.unknown('x')",)

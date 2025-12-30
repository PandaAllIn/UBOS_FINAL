from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from typing import Any, Iterable, List, Tuple

from config import load_configuration
from intelligence_tools import intel_lookup
from master_librarian_adapter import MasterLibrarianAdapter
from oracle_bridge import OracleBridge

TOOL_PATTERN = re.compile(r"\[TOOL:\s*(?P<command>.+?)\s*\]", re.IGNORECASE | re.DOTALL)
MAX_RESULT_CHARS = 4000

LIBRARIAN_METHODS = {"read_file", "list_files", "search_content"}
ORACLE_METHODS = {
    "fast_think",
    "wolfram",
    "research",
    "quick_research",
    "deep_research",
    "reason",
    "query_demographics",
    "query_economics",
    "resolve_place",
    "query_oracle",
}
INTELLIGENCE_METHODS = {"lookup"}


@dataclass(frozen=True)
class ToolEnvironment:
    librarian: MasterLibrarianAdapter
    oracle: OracleBridge
    intelligence: "IntelligenceFacade"


class IntelligenceFacade:
    """Lightweight wrapper exposing intelligence lookup to residents."""

    def lookup(
        self,
        category: str,
        filters: dict | None = None,
        query: str | None = None,
        limit: int = 10,
        sort_by: str = "relevance",
    ) -> list[dict]:
        return intel_lookup(category, filters=filters, query=query, limit=limit, sort_by=sort_by)


@dataclass(frozen=True)
class PromptWithTools:
    prompt: str
    tool_context: str
    executed_commands: Tuple[str, ...]


def initialize_tool_environment() -> ToolEnvironment:
    """Instantiate shared tool adapters for residents."""
    paths, keys = load_configuration()
    return ToolEnvironment(
        librarian=MasterLibrarianAdapter(paths),
        oracle=OracleBridge(keys),
        intelligence=IntelligenceFacade(),
    )


def enrich_prompt_with_tools(prompt: str, env: ToolEnvironment) -> PromptWithTools:
    """Detect tool requests in the prompt, execute them, and inject results."""
    if not prompt:
        return PromptWithTools(prompt="", tool_context="", executed_commands=())

    matches = list(TOOL_PATTERN.finditer(prompt))
    if not matches:
        return PromptWithTools(prompt=prompt.strip(), tool_context="", executed_commands=())

    executed: List[str] = []
    contexts: List[str] = []

    for match in matches:
        command = match.group("command").strip()
        executed.append(command)
        context = _execute_tool_command(command, env)
        contexts.append(context)

    stripped_prompt = TOOL_PATTERN.sub("", prompt).strip()
    base_prompt = stripped_prompt

    tool_context = "\n\n".join(contexts)
    if base_prompt:
        final_prompt = f"{base_prompt}\n\n[Tool Output]\n{tool_context}"
    else:
        final_prompt = f"[Tool Output]\n{tool_context}"

    return PromptWithTools(
        prompt=final_prompt,
        tool_context=tool_context,
        executed_commands=tuple(executed),
    )


def _execute_tool_command(command: str, env: ToolEnvironment) -> str:
    try:
        callable_obj, display_name = _resolve_callable(command, env)
        result = callable_obj()
        formatted = _format_result(result)
        return f"Command: {display_name}\nResult:\n{formatted}"
    except Exception as exc:  # pragma: no cover - ensures graceful degradation
        return f"Command: {command}\nResult: ERROR - {exc}"


def _resolve_callable(command: str, env: ToolEnvironment) -> Tuple[Any, str]:
    try:
        expression = ast.parse(command, mode="eval").body
    except SyntaxError as exc:
        raise ValueError(f"Invalid tool syntax: {command}") from exc

    if not isinstance(expression, ast.Call):
        raise ValueError(f"Tool command must be a call expression: {command}")

    func = expression.func
    if not isinstance(func, ast.Attribute) or not isinstance(func.value, ast.Name):
        raise ValueError(f"Unsupported tool target in command: {command}")

    target = func.value.id
    method_name = func.attr

    if target == "librarian" and method_name in LIBRARIAN_METHODS:
        callable_target = getattr(env.librarian, method_name)
    elif target == "oracle" and method_name in ORACLE_METHODS:
        callable_target = getattr(env.oracle, method_name)
    elif target == "intelligence" and method_name in INTELLIGENCE_METHODS:
        callable_target = getattr(env.intelligence, method_name)
    else:
        raise ValueError(f"Unsupported tool command: {target}.{method_name}")

    args, kwargs = _parse_arguments(expression.args, expression.keywords, command)

    def _invocation() -> Any:
        return callable_target(*args, **kwargs)

    return _invocation, f"{target}.{method_name}({', '.join(_arg_display(args, kwargs))})"


def _parse_arguments(
    args: Iterable[ast.expr],
    keywords: Iterable[ast.keyword],
    command: str,
) -> Tuple[List[Any], dict]:
    parsed_args: List[Any] = []
    parsed_kwargs: dict[str, Any] = {}

    for arg in args:
        parsed_args.append(_convert_literal(arg, command))

    for kw in keywords:
        if kw.arg is None:
            raise ValueError(f"Keyword unpacking not supported in tool command: {command}")
        parsed_kwargs[kw.arg] = _convert_literal(kw.value, command)

    return parsed_args, parsed_kwargs


def _convert_literal(node: ast.expr, command: str) -> Any:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (str, int, float, bool)) or node.value is None:
            return node.value
    if isinstance(node, ast.JoinedStr):
        parts: List[str] = []
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                raise ValueError(f"f-strings not supported in tool command: {command}")
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                raise ValueError(f"Unsupported f-string component in tool command: {command}")
        return "".join(parts)
    raise ValueError(f"Unsupported argument in tool command: {command}")


def _format_result(result: Any) -> str:
    if isinstance(result, (dict, list, tuple, set)):
        text = json.dumps(result, indent=2, default=str)
    else:
        text = str(result)

    if len(text) > MAX_RESULT_CHARS:
        return f"{text[:MAX_RESULT_CHARS]}...\n[truncated]"
    return text


def _arg_display(args: Iterable[Any], kwargs: dict[str, Any]) -> List[str]:
    parts = [repr(arg) for arg in args]
    parts.extend(f"{key}={value!r}" for key, value in kwargs.items())
    return parts

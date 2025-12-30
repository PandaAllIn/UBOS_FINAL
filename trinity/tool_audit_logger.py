from __future__ import annotations

import json
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar

from trinity.config import load_configuration

P = ParamSpec("P")
R = TypeVar("R")

_paths, _ = load_configuration()
LOG_PATH = _paths.log_dir / "tool_audit.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

MAX_FIELD_LENGTH = 400


def _truncate(value: str) -> str:
    if len(value) <= MAX_FIELD_LENGTH:
        return value
    return value[:MAX_FIELD_LENGTH] + "..."


def _normalise(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return _truncate(repr(value))


def _serialise_args(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    serialised: dict[str, Any] = {}
    if args:
        serialised["args"] = [_normalise(arg) for arg in args]
    if kwargs:
        serialised["kwargs"] = {key: _normalise(value) for key, value in kwargs.items()}
    return serialised


def _write_record(record: dict[str, Any]) -> None:
    record.setdefault("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        json.dump(record, handle)
        handle.write("\n")


def audit_tool_call(tool_name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator that records tool invocations to the audit log."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            component: str | None = None
            call_args = args
            if args and hasattr(args[0], func.__name__):
                component = args[0].__class__.__name__
                call_args = args[1:]
            serialised = _serialise_args(call_args, kwargs)
            started = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                duration = time.perf_counter() - started
                _write_record(
                    {
                        "tool": tool_name,
                        "status": "error",
                        "duration_seconds": round(duration, 6),
                        "error": _truncate(str(exc)),
                        "parameters": serialised,
                        "component": component,
                    }
                )
                raise
            else:
                duration = time.perf_counter() - started
                record: dict[str, Any] = {
                    "tool": tool_name,
                    "status": "success",
                    "duration_seconds": round(duration, 6),
                    "parameters": serialised,
                    "component": component,
                }
                preview = _normalise(result)
                if preview is not None:
                    record["result_preview"] = preview
                _write_record(record)
                return result

        return wrapper

    return decorator


__all__ = ["audit_tool_call"]

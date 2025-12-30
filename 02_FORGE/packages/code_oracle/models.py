"""Data models for the Code Oracle graph."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass(slots=True)
class CallReference:
    """Represents a call site within a function."""

    raw: str
    kind: str
    module: str | None = None
    symbol: str | None = None


@dataclass(slots=True)
class FunctionRecord:
    """Metadata for a function or method definition."""

    function_id: str
    module_path: str
    module_name: str
    qualname: str
    calls: List[CallReference] = field(default_factory=list)
    call_targets: Dict[str, str] = field(default_factory=dict)
    resolved_calls: Set[str] = field(default_factory=set)
    docstring: str | None = None


@dataclass(slots=True)
class ModuleRecord:
    """Metadata for a Python module in the repository."""

    relative_path: str
    module_name: str
    imports: Set[str] = field(default_factory=set)
    alias_map: Dict[str, str] = field(default_factory=dict)
    functions: Dict[str, FunctionRecord] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)


@dataclass(slots=True)
class CodeOracleGraph:
    """Aggregated view of modules and functions for queries."""

    workspace_root: str
    modules_by_path: Dict[str, ModuleRecord]
    modules_by_name: Dict[str, ModuleRecord]
    functions: Dict[str, FunctionRecord]
    module_dependencies: Dict[str, Set[str]]
    module_dependents: Dict[str, Set[str]]
    function_calls: Dict[str, Set[str]]
    function_called_by: Dict[str, Set[str]]

"""Query interface for the Code Oracle graph."""
from __future__ import annotations

from pathlib import Path
from .analyzer import CodebaseAnalyzer
from .models import CodeOracleGraph, FunctionRecord, ModuleRecord


class CodeOracle:
    """Facade that exposes dependency queries over the codebase."""

    def __init__(self, workspace_root: Path | None = None, graph: CodeOracleGraph | None = None) -> None:
        self.workspace_root = workspace_root or Path(__file__).resolve().parents[3]
        self.graph = graph or CodebaseAnalyzer(self.workspace_root).build()

    # ------------------------------------------------------------------ Public API
    def get_dependencies(self, target: str) -> dict[str, object]:
        module_path, function_id = self._resolve_target(target)
        if function_id is None:
            module_record = self._get_module(module_path)
            return {
                "target": module_path,
                "type": "module",
                "dependencies": {
                    "imports": sorted(module_record.imports),
                    "internal_modules": sorted(module_record.dependencies),
                    "external_modules": sorted(
                        dep for dep in module_record.imports if dep not in self.graph.modules_by_name
                    ),
                },
                "defined_functions": sorted(module_record.functions.keys()),
            }

        function_record = self.graph.functions[function_id]
        module_record = self._get_module(module_path)

        resolved_modules = {
            self.graph.functions[callee].module_path for callee in function_record.resolved_calls
        }

        referenced_modules = {
            self.graph.modules_by_name[call.module].relative_path
            if call.module in self.graph.modules_by_name
            else call.module
            for call in function_record.calls
            if call.module
        }
        unresolved_calls = [
            call.raw for call in function_record.calls if call.raw not in function_record.call_targets
        ]

        payload = {
            "target": function_id,
            "type": "function",
            "dependencies": {
                "modules": sorted(resolved_modules | referenced_modules),
                "functions": sorted(function_record.resolved_calls),
                "unresolved_calls": sorted(set(unresolved_calls)),
                "module_imports": sorted(module_record.imports),
            },
        }
        return payload

    def get_dependents(self, target: str) -> dict[str, object]:
        module_path, function_id = self._resolve_target(target)
        if function_id is None:
            module_record = self._get_module(module_path)
            dependents = sorted(self.graph.module_dependents.get(module_path, set()))
            module_function_ids = [record.function_id for record in module_record.functions.values()]
            dependent_functions: set[str] = set()
            for function in module_function_ids:
                dependent_functions.update(self.graph.function_called_by.get(function, set()))
            return {
                "target": module_path,
                "type": "module",
                "dependents": {
                    "modules": dependents,
                    "functions": sorted(dependent_functions),
                },
            }

        dependents = sorted(self.graph.function_called_by.get(function_id, set()))
        return {
            "target": function_id,
            "type": "function",
            "dependents": {
                "functions": dependents,
                "modules": sorted({self.graph.functions[f].module_path for f in dependents}),
            },
        }

    def get_call_graph(self, target: str) -> dict[str, object]:
        module_path, function_id = self._resolve_target(target)
        if function_id is None:
            raise ValueError("get_call_graph expects a function target in the form 'path/to/file.py::function_name'")

        outbound = sorted(self.graph.function_calls.get(function_id, set()))
        inbound = sorted(self.graph.function_called_by.get(function_id, set()))
        function_record = self.graph.functions[function_id]
        unresolved = [
            call.raw for call in function_record.calls if call.raw not in function_record.call_targets
        ]

        return {
            "target": function_id,
            "type": "function",
            "call_graph": {
                "outbound": [
                    {"function": fn_id, "module": self.graph.functions[fn_id].module_path} for fn_id in outbound
                ],
                "inbound": [
                    {"function": fn_id, "module": self.graph.functions[fn_id].module_path} for fn_id in inbound
                ],
                "unresolved": sorted(set(unresolved)),
            },
        }

    # ------------------------------------------------------------------ Target resolution helpers
    def _resolve_target(self, target: str) -> tuple[str, str | None]:
        raw = target.strip()
        if "::" in raw:
            path_component, symbol = raw.split("::", 1)
            module_path = self._resolve_module_path(path_component.strip())
            function_id = self._resolve_function_id(module_path, symbol.strip())
            return module_path, function_id
        module_path = self._resolve_module_path(raw)
        return module_path, None

    def _resolve_module_path(self, raw_path: str) -> str:
        candidate = raw_path.replace("\\", "/")
        if candidate.startswith("./"):
            candidate = candidate[2:]

        attempts = [candidate]
        if not candidate.startswith("02_FORGE/"):
            attempts.extend(
                [
                    f"02_FORGE/{candidate}",
                    f"02_FORGE/src/{candidate}",
                    f"02_FORGE/scripts/{candidate}",
                ]
            )

        for attempt in attempts:
            if attempt in self.graph.modules_by_path:
                return attempt

        absolute = Path(candidate)
        if absolute.is_absolute():
            try:
                rel = absolute.relative_to(self.workspace_root).as_posix()
                if rel in self.graph.modules_by_path:
                    return rel
            except ValueError:
                pass

        fallback = (self.workspace_root / candidate).resolve()
        try:
            rel = fallback.relative_to(self.workspace_root).as_posix()
            if rel in self.graph.modules_by_path:
                return rel
        except ValueError:
            pass

        raise KeyError(f"Unknown module path '{raw_path}'")

    def _resolve_function_id(self, module_path: str, symbol: str) -> str:
        module_record = self._get_module(module_path)
        cleaned = symbol.strip()
        if cleaned in module_record.functions:
            return module_record.functions[cleaned].function_id

        simple = cleaned.split(".")[-1]
        matches = [record for name, record in module_record.functions.items() if name.split(".")[-1] == simple]
        if len(matches) == 1:
            return matches[0].function_id

        raise KeyError(f"Function '{symbol}' not found in module '{module_path}'")

    def _get_module(self, module_path: str) -> ModuleRecord:
        try:
            return self.graph.modules_by_path[module_path]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"Module '{module_path}' not indexed") from exc

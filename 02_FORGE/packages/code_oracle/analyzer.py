"""Static analyzer that builds the Code Oracle graph."""
from __future__ import annotations

import ast
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

from .models import CallReference, CodeOracleGraph, FunctionRecord, ModuleRecord
from .utils import attribute_to_dotted, iter_python_files, module_name_from_path, normalise_path

LOGGER = logging.getLogger(__name__)


class ModuleParser(ast.NodeVisitor):
    """AST visitor that extracts imports, alias maps, and call relationships."""

    def __init__(self, file_path: Path, module_name: str) -> None:
        self.file_path = file_path
        self.module_name = module_name
        self.relative_path = normalise_path(file_path)
        self.module_record = ModuleRecord(relative_path=self.relative_path, module_name=module_name)
        self.class_stack: list[str] = []
        self.function_stack: list[str] = []
        self.module_function_names: set[str] = set()
        self.class_method_names: dict[str, set[str]] = defaultdict(set)
        self.class_names: set[str] = set()

    # ------------------------------------------------------------------ Imports
    def visit_Import(self, node: ast.Import) -> None:  # pragma: no cover - trivial
        for alias in node.names:
            module = alias.name
            self.module_record.imports.add(module)
            root = module.split(".")[0]
            self.module_record.imports.add(root)
            name = alias.asname or root
            self.module_record.alias_map.setdefault(name, module)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pragma: no cover - trivial
        if any(alias.name == "*" for alias in node.names):
            return
        resolved_module = self._resolve_from_module(node)
        for alias in node.names:
            base_module = resolved_module or alias.name.split(".")[0]
            if base_module:
                self.module_record.imports.add(base_module)
            alias_name = alias.asname or alias.name
            if resolved_module:
                self.module_record.alias_map.setdefault(alias_name, f"{resolved_module}.{alias.name}")
            else:
                self.module_record.alias_map.setdefault(alias_name, alias.name)

    # ------------------------------------------------------------------ Classes
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_names.add(node.name)
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    # ---------------------------------------------------------------- Functions
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._register_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._register_function(node)

    # ---------------------------------------------------------------- Helpers
    def parse(self, source: str) -> ModuleRecord:
        tree = ast.parse(source, filename=str(self.file_path))
        self.visit(tree)
        return self.module_record

    def _resolve_from_module(self, node: ast.ImportFrom) -> str:
        base = node.module or ""
        if node.level == 0:
            return base

        parts = self.module_name.split(".")
        if node.level > len(parts):
            prefix: list[str] = []
        else:
            prefix = parts[: -node.level]
        if base:
            prefix.append(base)
        return ".".join(part for part in prefix if part)

    def _current_qualname(self, func_name: str) -> str:
        components: list[str] = []
        if self.class_stack:
            components.extend(self.class_stack)
        if self.function_stack:
            components.extend(self.function_stack)
        components.append(func_name)
        return ".".join(components)

    def _register_function(self, node: ast.AST) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name
        else:  # pragma: no cover - defensive
            return

        qualname = self._current_qualname(func_name)
        function_id = f"{self.relative_path}::{qualname}"
        docstring = ast.get_docstring(node)

        if self.class_stack:
            self.class_method_names[self.class_stack[-1]].add(func_name)
        self.module_function_names.add(func_name)

        self.function_stack.append(func_name)
        calls = self._collect_calls(node)
        self.function_stack.pop()

        record = FunctionRecord(
            function_id=function_id,
            module_path=self.relative_path,
            module_name=self.module_name,
            qualname=qualname,
            calls=calls,
            docstring=docstring,
        )
        self.module_record.functions[qualname] = record

        # Continue visiting child nodes to handle nested functions/classes
        self.generic_visit(node)

    def _collect_calls(self, node: ast.AST) -> list[CallReference]:
        references: list[CallReference] = []
        current_class = self.class_stack[-1] if self.class_stack else None

        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                ref = self._describe_call(inner.func, current_class=current_class)
                if ref:
                    references.append(ref)
        return references

    def _describe_call(self, target: ast.AST, current_class: Optional[str]) -> CallReference | None:
        if isinstance(target, ast.Name):
            name = target.id
            if name in self.module_record.alias_map:
                return CallReference(raw=name, kind="module", module=self.module_record.alias_map[name], symbol=None)
            if name in self.module_function_names:
                return CallReference(raw=name, kind="function_local", module=self.module_name, symbol=name)
            return CallReference(raw=name, kind="identifier", module=None, symbol=name)

        dotted = attribute_to_dotted(target)
        if not dotted:
            return CallReference(raw=type(target).__name__, kind="unknown", module=None, symbol=None)

        parts = dotted.split(".")
        base = parts[0]
        tail = parts[1:]
        remainder = ".".join(tail) if tail else None
        raw = dotted

        if base == "self" and current_class and tail:
            symbol = f"{current_class}.{tail[0]}"
            return CallReference(raw=raw, kind="method", module=self.module_name, symbol=symbol)

        if base in self.module_record.alias_map:
            module = self.module_record.alias_map[base]
            symbol = remainder
            return CallReference(raw=raw, kind="module_attr", module=module, symbol=symbol)

        if base in self.class_names and tail:
            symbol = f"{base}.{tail[0]}"
            return CallReference(raw=raw, kind="method", module=self.module_name, symbol=symbol)

        if base in self.module_function_names:
            return CallReference(raw=raw, kind="function_local", module=self.module_name, symbol=raw)

        return CallReference(raw=raw, kind="identifier", module=None, symbol=raw)


class CodebaseAnalyzer:
    """Builds the graph representation for the Code Oracle."""

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.src_root = workspace_root / "02_FORGE" / "src"
        self.scripts_root = workspace_root / "02_FORGE" / "scripts"
        self.packages_root = workspace_root / "02_FORGE" / "packages"

    def build(self) -> CodeOracleGraph:
        modules_by_path: Dict[str, ModuleRecord] = {}
        modules_by_name: Dict[str, ModuleRecord] = {}
        functions: Dict[str, FunctionRecord] = {}
        module_dependencies: Dict[str, Set[str]] = defaultdict(set)
        module_dependents: Dict[str, Set[str]] = defaultdict(set)
        function_calls: Dict[str, Set[str]] = defaultdict(set)
        function_called_by: Dict[str, Set[str]] = defaultdict(set)
        simple_name_index: Dict[str, Set[str]] = defaultdict(set)
        module_functions_by_name: Dict[str, Dict[str, FunctionRecord]] = defaultdict(dict)

        for file_path in iter_python_files(self.src_root, self.scripts_root, self.packages_root):
            try:
                source = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                source = file_path.read_text(encoding="utf-8", errors="ignore")

            module_name = module_name_from_path(
                file_path,
                self.src_root,
                self.scripts_root,
                packages_roots=(self.packages_root,),
            )
            parser = ModuleParser(file_path=file_path.relative_to(self.workspace_root), module_name=module_name)
            try:
                module_record = parser.parse(source)
            except SyntaxError as exc:  # pragma: no cover - defensive for generated artefacts
                LOGGER.warning("Skipping %s due to parse error: %s", file_path, exc)
                continue

            modules_by_path[module_record.relative_path] = module_record
            modules_by_name[module_record.module_name] = module_record

            for qualname, function_record in module_record.functions.items():
                functions[function_record.function_id] = function_record
                simple_name = qualname.split(".")[-1]
                simple_name_index[simple_name].add(function_record.function_id)
                function_map = module_functions_by_name[module_record.module_name]
                function_map[qualname] = function_record
                function_map.setdefault(simple_name, function_record)


            module_dependencies[module_record.relative_path].update(module_record.imports)

        # Resolve module dependencies to actual known modules
        for module_path, imports in module_dependencies.items():
            resolved: set[str] = set()
            for imported in imports:
                if imported in modules_by_name:
                    resolved.add(modules_by_name[imported].relative_path)
            modules_by_path[module_path].dependencies = resolved
            for dep in resolved:
                module_dependents[dep].add(module_path)

        # Resolve function call targets
        for module_record in modules_by_path.values():
            module_functions = module_functions_by_name.get(module_record.module_name, {})
            for function_record in module_record.functions.values():
                for call in function_record.calls:
                    target_id = self._resolve_call_reference(
                        call,
                        module_record,
                        modules_by_name,
                        module_functions_by_name,
                        simple_name_index,
                    )
                    if target_id:
                        function_record.resolved_calls.add(target_id)
                        function_record.call_targets[call.raw] = target_id
                        function_calls[function_record.function_id].add(target_id)
                        function_called_by[target_id].add(function_record.function_id)

        return CodeOracleGraph(
            workspace_root=normalise_path(self.workspace_root),
            modules_by_path=modules_by_path,
            modules_by_name=modules_by_name,
            functions=functions,
            module_dependencies={k: set(v) for k, v in module_dependencies.items()},
            module_dependents={k: set(v) for k, v in module_dependents.items()},
            function_calls={k: set(v) for k, v in function_calls.items()},
            function_called_by={k: set(v) for k, v in function_called_by.items()},
        )

    # ------------------------------------------------------------------ Helpers
    def _resolve_call_reference(
        self,
        call: CallReference,
        module_record: ModuleRecord,
        modules_by_name: Dict[str, ModuleRecord],
        module_functions_by_name: Dict[str, Dict[str, FunctionRecord]],
        simple_name_index: Dict[str, Set[str]],
    ) -> Optional[str]:
        """Attempt to map a CallReference to a known function identifier."""

        # Direct module + symbol resolution
        if call.module and call.symbol:
            candidates = self._lookup_candidates(call.module, call.symbol, modules_by_name, module_functions_by_name)
            if candidates:
                return candidates[0]

        # Local module resolution
        if call.module == module_record.module_name and call.symbol:
            qualname = call.symbol
            func = module_record.functions.get(qualname)
            if func:
                return func.function_id

        # Simple name fallback within same module
        if call.symbol:
            simple = call.symbol.split(".")[-1]
            local_candidate = module_record.functions.get(simple)
            if local_candidate:
                return local_candidate.function_id

            matching = simple_name_index.get(simple)
            if matching and len(matching) == 1:
                return next(iter(matching))

        return None

    def _lookup_candidates(
        self,
        module_name: str,
        symbol: str,
        modules_by_name: Dict[str, ModuleRecord],
        module_functions_by_name: Dict[str, Dict[str, FunctionRecord]],
    ) -> List[str]:
        components = symbol.split(".")
        candidates: list[str] = []

        potential_modules = [module_name]
        for i in range(1, len(components)):
            potential_modules.append(f"{module_name}.{'.'.join(components[:i])}")

        function_name = components[-1]
        method_name = ".".join(components[-2:]) if len(components) > 1 else function_name

        for candidate_module in potential_modules:
            if candidate_module not in modules_by_name:
                continue
            function_map = module_functions_by_name.get(candidate_module, {})
            for key in (symbol, method_name, function_name):
                if key in function_map:
                    candidates.append(function_map[key].function_id)
                    break
            if candidates:
                break

        return candidates

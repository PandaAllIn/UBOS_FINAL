"""Utility helpers for the Code Oracle."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable, List, Sequence


def iter_python_files(*roots: Path) -> Iterable[Path]:
    """Yield Python files under the given roots."""
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            yield path


def module_name_from_path(
    path: Path,
    src_root: Path,
    scripts_root: Path,
    packages_roots: Sequence[Path] | None = None,
) -> str:
    """Derive a Python module name from a filesystem path."""
    if path.is_dir():
        raise ValueError("Path to module must be a file")
    if path.suffix != ".py":
        raise ValueError("Path must point to a Python file")

    search_roots: list[tuple[Path, Path | None]] = [
        (src_root, None),
        (scripts_root, Path("scripts")),
    ]
    if packages_roots:
        for pkg_root in packages_roots:
            search_roots.append((pkg_root, Path("packages")))

    relative = path
    for root, prefix in search_roots:
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        relative = rel if prefix is None else prefix / rel
        break

    parts = list(relative.parts)
    if not parts:
        return path.stem

    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]  # strip ".py"

    return ".".join(parts) if parts else "__init__"


def attribute_to_dotted(node: ast.AST) -> str | None:
    """Convert nested attribute expressions to a dotted string."""
    parts: List[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def normalise_path(path: Path) -> str:
    return str(path.as_posix())

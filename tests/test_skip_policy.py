"""Keep test skips centralized in the shared lane helper."""

from __future__ import annotations

import ast
from pathlib import Path


TESTS = Path(__file__).parent
SHARED_HELPER = TESTS / "lanes.py"
SKIP_NAMES = {"skip", "skipif", "importorskip"}


def _skip_references(tree: ast.Module) -> list[tuple[int, str]]:
    pytest_modules = {"pytest"}
    imported_skip_names: set[str] = set()
    pytest_mark_names = {"mark"}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "pytest":
                    pytest_modules.add(alias.asname or "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                local = alias.asname or alias.name
                if alias.name in SKIP_NAMES:
                    imported_skip_names.add(local)
                elif alias.name == "mark":
                    pytest_mark_names.add(local)

    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in imported_skip_names:
                found.append((node.lineno, func.id))
            elif isinstance(func, ast.Attribute) and func.attr in SKIP_NAMES:
                owner = func.value
                if isinstance(owner, ast.Name) and owner.id in pytest_modules:
                    found.append((node.lineno, ast.unparse(func)))
                elif (
                    isinstance(owner, ast.Attribute)
                    and owner.attr in pytest_mark_names
                    and isinstance(owner.value, ast.Name)
                    and owner.value.id in pytest_modules
                ):
                    found.append((node.lineno, ast.unparse(func)))
                elif isinstance(owner, ast.Name) and owner.id in pytest_mark_names and func.attr in {"skip", "skipif"}:
                    found.append((node.lineno, ast.unparse(func)))
        elif isinstance(node, ast.Attribute) and node.attr in {"skip", "skipif"}:
            owner = node.value
            if (
                isinstance(owner, ast.Attribute)
                and owner.attr in pytest_mark_names
                and isinstance(owner.value, ast.Name)
                and owner.value.id in pytest_modules
            ):
                found.append((node.lineno, ast.unparse(node)))

    return found


def test_skip_apis_are_confined_to_shared_lane_helper() -> None:
    violations = []
    for path in sorted(TESTS.rglob("*.py")):
        if path == SHARED_HELPER:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        violations.extend(
            f"{path.relative_to(TESTS)}:{line}: {reference}"
            for line, reference in _skip_references(tree)
        )

    assert not violations, "test skip APIs must live in tests/lanes.py:\n" + "\n".join(violations)

"""Static D69 restoration gate; the service row calls this before pytest."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_COMMIT = "9502c321b6884235bcd040364d2bc8431caf6a87"
DONOR_COMMITS = (
    "fdeef9ca2d550e3c561419c2cf96f653afba73cf",
    "f453dac68699cf9e719cd0bf81bc64a806c76017",
)
FINAL_REFS = {
    "cli": "tl/integration",
    "sdk": "tl/agt-F-D69-unchanged-sdk-1605",
    "other": "tl/agt-F-D69-unchanged-other-1605",
}
MANIFEST = Path("evidence/d69-restored47.json")


def _dump(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def _body_dump(function: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    return _dump(ast.Module(body=function.body, type_ignores=[]))


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _functions(source: str) -> dict[str, list[ast.FunctionDef | ast.AsyncFunctionDef]]:
    result: dict[str, list[ast.FunctionDef | ast.AsyncFunctionDef]] = defaultdict(list)
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name].append(node)
    return result


def _parameter_count(function: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    for decorator in function.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        target = decorator.func
        if not (
            isinstance(target, ast.Attribute)
            and target.attr == "parametrize"
            and isinstance(target.value, ast.Attribute)
            and target.value.attr == "mark"
        ):
            continue
        if len(decorator.args) < 2:
            raise AssertionError(f"malformed parametrize on {function.name}")
        values = decorator.args[1]
        if not isinstance(values, (ast.List, ast.Tuple)):
            raise AssertionError(f"non-finite parametrize on {function.name}")
        return len(values.elts)
    return 0


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=root, text=True).strip()


def _source(root: Path, path: str, ref: str | None) -> str:
    if ref is None:
        return (root / path).read_text(encoding="utf-8")
    return subprocess.check_output(
        ("git", "show", f"{ref}:{path}"), cwd=root, text=True
    )


def _require_ancestor(root: Path, commit: str, head: str) -> None:
    result = subprocess.run(
        ("git", "merge-base", "--is-ancestor", commit, head), cwd=root
    )
    if result.returncode:
        raise AssertionError(f"required donor is not an ancestor of {head}: {commit}")


def check(
    root: Path,
    *,
    manifest_path: Path,
    require_donors: bool,
    inspect_refs: bool = False,
) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest["rows"]
    if manifest["counts"] != {
        "rows": 47,
        "functions": 34,
        "parameterized_rows": 20,
        "nonparameterized_rows": 27,
        "slices": {"cli": 14, "sdk": 16, "other": 17},
    }:
        raise AssertionError(f"manifest counts changed: {manifest['counts']}")
    selectors = [row["selector"] for row in rows]
    if len(selectors) != len(set(selectors)):
        raise AssertionError("duplicate restored selector")
    head = _git(root, "rev-parse", "HEAD")
    tree = _git(root, "rev-parse", "HEAD^{tree}")
    parents = _git(root, "rev-list", "--parents", "-n", "1", "HEAD")
    _require_ancestor(root, BASE_COMMIT, head)
    if require_donors:
        for donor in DONOR_COMMITS:
            _require_ancestor(root, donor, head)

    by_path: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_path[row["path"]].append(row)
    file_hashes = {}
    functions_seen: set[tuple[str, str]] = set()
    for path, path_rows in by_path.items():
        refs = {FINAL_REFS[row["slice"]] for row in path_rows} if inspect_refs else {None}
        if len(refs) != 1:
            raise AssertionError(f"mixed final refs for {path}")
        source = _source(root, path, refs.pop())
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        expected_file_hashes = {row["final_file_sha256"] for row in path_rows}
        if expected_file_hashes != {digest}:
            raise AssertionError(f"source hash mismatch for {path}: {digest}")
        file_hashes[path] = digest
        functions = _functions(source)
        grouped: Counter[tuple[str, str]] = Counter()
        for row in path_rows:
            function = functions.get(row["current_function"], [])
            if len(function) != 1:
                raise AssertionError(
                    f"expected one discovered function {path}::{row['current_function']}"
                )
            function = function[0]
            if _sha(_body_dump(function)) != row["body_ast_sha256"]:
                raise AssertionError(f"body AST mismatch: {row['selector']}")
            if _sha(_dump(function.args)) != row["args_ast_sha256"]:
                raise AssertionError(f"args AST mismatch: {row['selector']}")
            decorators = "\n".join(_dump(node) for node in function.decorator_list)
            if _sha(decorators) != row["decorators_ast_sha256"]:
                raise AssertionError(f"decorator AST mismatch: {row['selector']}")
            grouped[(row["current_function"], row["parameterized"])] += 1
            functions_seen.add((path, row["current_function"]))
        for (function_name, parameterized), count in grouped.items():
            function = functions[function_name][0]
            actual = _parameter_count(function)
            if bool(actual) != bool(parameterized) or (actual and actual != count):
                raise AssertionError(
                    f"selector partition mismatch {path}::{function_name}: "
                    f"rows={count}, decorator_cases={actual}"
                )

    if len(functions_seen) != 34:
        raise AssertionError(f"function partition mismatch: {len(functions_seen)}")
    return {
        "status": "PASS",
        "task": "F/D69",
        "head": head,
        "tree": tree,
        "parents": parents,
        "rows": len(rows),
        "functions": len(functions_seen),
        "parameterized_rows": sum(bool(row["parameterized"]) for row in rows),
        "file_hashes": file_hashes,
        "donors_required": require_donors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-preflight", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.service_preflight == args.inspect:
        parser.error("choose exactly one of --service-preflight or --inspect")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    manifest = (args.manifest or root / MANIFEST).resolve()
    try:
        result = check(
            root,
            manifest_path=manifest,
            require_donors=args.service_preflight,
            inspect_refs=args.inspect,
        )
    except (AssertionError, OSError, subprocess.CalledProcessError) as exc:
        print(f"D69_PREFLIGHT_FAIL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

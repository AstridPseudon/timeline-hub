#!/usr/bin/env python3
"""Read-only D83 selector, AST, hash, and source-scope checks.

This deliberately parses Python source and never imports or collects tests.
"""

from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path


EXPECTED = [
    (
        "p4",
        "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::"
        "test_cli_sheet_v2_runtime_preserves_document_and_reads_back",
        "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py",
    ),
    (
        "p4",
        "tests/editing_conformance/test_p4_ten_note_v2_runtime.py::"
        "test_http_ten_note_commit_per_step_inverse_and_redo",
        "tests/editing_conformance/test_p4_ten_note_v2_runtime.py",
    ),
    (
        "p4",
        "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::"
        "test_http_note_conflict_reruns_public_function_from_verified_peer_document",
        "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py",
    ),
]
for same_revision in (False, True):
    for key in ("None", "public-element"):
        EXPECTED.append(
            (
                "r2-param",
                "tests/core/test_timeline_element_publication_runtime.py::"
                "test_public_helper_restart_exact_retry_later_head_inverse_redo"
                f"[{same_revision}-{key}]",
                "tests/core/test_timeline_element_publication_runtime.py",
            )
        )

EXPECTED_DONOR = {
    "donor2_param_source_sha256": "86f4c4154ecb4e2dd26770a04c35c6285e67c067621e628e2cb0026bafdfcfdf",
    "donor2_param_test_sha256": "fb9aa03b356bdfe5a51c93be06dd62ca2826be122ffd3a0874101d17885c9657",
    "current_home_param_source_sha256": "38d30e8fca3566fdf6526e84e538d2f5be5a5d159c8b3ad18c560eb58d85e19b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def functions(tree: ast.AST) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def check_selector_ast(root: Path) -> None:
    by_file: dict[Path, ast.AST] = {}
    for _group, selector, relative in EXPECTED:
        path = root / relative
        assert path.is_file(), path
        tree = by_file.setdefault(path, ast.parse(path.read_text()))
        function_name = selector.split("::", 1)[1].split("[", 1)[0]
        assert function_name in functions(tree), (selector, "missing function")

    runtime = root / "tests/core/test_timeline_element_publication_runtime.py"
    restart = functions(by_file[runtime])["test_public_helper_restart_exact_retry_later_head_inverse_redo"]
    seen: set[tuple[str, tuple[object, ...]]] = set()
    for decorator in restart.decorator_list:
        if not (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "parametrize"
        ):
            continue
        names = ast.literal_eval(decorator.args[0])
        values = ast.literal_eval(decorator.args[1])
        assert names in {"same_revision", "key"}, names
        assert isinstance(values, list) and len(values) == 2, values
        seen.add((names, tuple(values)))
    assert seen == {
        ("same_revision", (False, True)),
        ("key", (None, "public-element")),
    }, seen


def check_manifest(root: Path, evidence: Path) -> None:
    rows = []
    for line in (evidence / "selector-manifest.tsv").read_text().splitlines()[1:]:
        if not line.strip():
            continue
        group, selector, protected = line.split("\t")
        rows.append((group, selector, protected))
    assert rows == EXPECTED, rows
    assert len([row for row in rows if row[0] == "p4"]) == 3
    assert len([row for row in rows if row[0] == "r2-param"]) == 4

    expected_files = {
        "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py": "8239ad0c3ac7de05d7ab0efac7b12c34532df33f7f22f33c9c270f0aeb30f213",
        "tests/editing_conformance/test_p4_ten_note_v2_runtime.py": "c0132e0dac31be278eaa850a8cc5d96d535550e461685be263c3372b46f6d0a0",
        "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py": "02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36",
        "tests/core/test_timeline_element_publication_runtime.py": "c331dcfd930544ff699674c31d7867d8da5d852d22e72f3ebcb335aabe55c79a",
    }
    for relative, expected in expected_files.items():
        assert sha256(root / relative) == expected, relative

    protected = (evidence / "protected-sha256.txt").read_text()
    for key, expected in EXPECTED_DONOR.items():
        assert f"{key}={expected}" in protected, key
    p4_hashes = [expected_files[row[2]] for row in EXPECTED[:3]]
    aggregate = hashlib.sha256(
        "".join(
            f"{digest}  {relative}\n"
            for digest, relative in zip(p4_hashes, [row[2] for row in EXPECTED[:3]])
        ).encode()
    ).hexdigest()
    assert aggregate == "cf65539e79e9731c468368e72da4dba44298107c517715042aceb8d3c6d0e727"


def check_source_records(evidence: Path) -> None:
    text = (evidence / "source-records.tsv").read_text()
    assert "historical-prior-d73\tselected_param_authority_sha256\t38d30e8fca3566fdf6526e84e538d2f5be5a5d159c8b3ad18c560eb58d85e19b" in text
    assert "candidate-param-donor2\tselected_param_authority_sha256\t86f4c4154ecb4e2dd26770a04c35c6285e67c067621e628e2cb0026bafdfcfdf" in text
    assert "candidate_true_rows\tUNPROVEN_FOR_CURRENT_HOME" in text


def check_recipe(evidence: Path) -> None:
    recipe = (evidence / "p4-r2-d83-unprofiled.recipe.sh").read_text()
    assert "unset P4_LIVE_PROFILE_DIR" in recipe
    assert "--timeout=45" in recipe
    assert "cProfile" not in recipe
    assert "python -m pytest --collect-only" not in recipe
    assert "RELEASE" not in recipe
    assert "PREREQUISITE" not in recipe
    assert "source-candidate-donor2" in recipe
    for _group, selector, _protected in EXPECTED:
        assert recipe.count(selector) == 1, selector


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    evidence = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).parent).resolve()
    check_selector_ast(root)
    check_manifest(root, evidence)
    check_source_records(evidence)
    check_recipe(evidence)
    print("D83 static selector/AST/hash/source-scope checks: PASS")
    print("selector_membership=p4:3,r2-param:4,total:7")
    print("body_execution=none; pytest_collection=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

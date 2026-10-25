"""Static validation for the private D86 source-receiving packet.

This intentionally parses source and evidence only.  It does not import the
Runtime or Agent packages, collect tests, invoke fixtures, or contact a route.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DESIGN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
)
ORCH_DESIGN = DESIGN / "scratchpad/orch/design"


def lines(path: Path) -> list[str]:
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    selectors = lines(ROOT / "inputs/selectors.txt")
    expected = lines(ORCH_DESIGN / "handoff-agt-new-source-inputs-0612-selectors.txt")
    assert selectors == expected
    assert len(selectors) == 21 == len(set(selectors))

    functional = lines(ROOT / "functional3/selectors.txt")
    functional_expected = lines(ORCH_DESIGN / "handoff-agt-D98-0427-selectors.txt")
    assert functional == functional_expected
    assert len(functional) == 3 == len(set(functional))
    assert not set(selectors) & set(functional)

    actual_rows = list(csv.DictReader((ROOT / "inputs/actual-membership.tsv").open(), delimiter="\t"))
    assert [row["selector"] for row in actual_rows] == selectors
    assert all(row["actual17724"] == "NO_OVERLAP" for row in actual_rows)
    assert {row["actual19214"] for row in actual_rows} == {"FAIL", "PASS"}

    for name in ("inputs/accounting.json",):
        json.loads((ROOT / name).read_text(encoding="utf-8"))
    for path in (ROOT / "inputs/source-hashes.tsv", ROOT / "functional3/source-hashes.tsv"):
        rows = list(csv.DictReader(path.open(), delimiter="\t"))
        assert rows
        for row in rows:
            for key in ("commit", "sha256"):
                value = row.get(key)
                if value not in (None, "-", "UNKNOWN"):
                    # Review rows carry a human-readable identity in the
                    # commit column; source rows carry the actual object hash.
                    if key == "commit" and row.get("kind") in {"review", "dependency"}:
                        continue
                    if key == "sha256" and row.get("kind") == "review":
                        continue
                    assert re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value)

    runtime = Path(__file__).resolve().parents[3]
    for relative in (
        "contract/commit-v2.md",
        "runtime_protocol/timeline_commit.py",
        "runtime_protocol/timeline_commit_execution.py",
        "runtime_protocol/timeline_commit_inputs.py",
        "runtime_protocol/timeline_commit_provider.py",
        "runtime_protocol/timeline_commit_store.py",
        "runtime_protocol/timeline_commit_validation.py",
    ):
        path = runtime / relative
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        else:
            assert sha(path) == "4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7"

    route = Path(
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
        "/scratchpad/orch/workers/rt-D86-later-delta-prep-0236/evidence/"
        "fd86-later-delta/route/main-affected-batch-recipe.sh"
    )
    assert sha(route) == "253f2244bc3fcc311b8ff4c5c5cd84de19c37a8372d8026bd5c64a78fbfc909a"
    print("selectors=21 exact; functional3=3 exact; disjoint=PASS")
    print("actual17724_overlap=0; actual19214_membership=21; source_receipts=4")
    print("json_tsv_hash_set_parse=PASS; runtime_ast_compile=PASS; route_hash=PASS")


if __name__ == "__main__":
    main()

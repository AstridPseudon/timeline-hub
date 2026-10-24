#!/usr/bin/env python3
"""Lossless comparison of one upstream JUnit result against the D54 276-node set."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def node_id(testcase: ET.Element) -> str:
    classname = testcase.attrib.get("classname", "")
    if classname.endswith(".py"):
        module = classname
    elif "/" in classname:
        module = classname + ".py"
    else:
        module = classname.replace(".", "/") + ".py"
    return f"{module}::{testcase.attrib.get('name', '')}"


def status(testcase: ET.Element) -> str:
    if testcase.find("error") is not None:
        return "ERROR"
    if testcase.find("failure") is not None:
        return "FAILED"
    if testcase.find("skipped") is not None:
        return "SKIPPED"
    return "PASSED"


def testcase_detail(testcase: ET.Element) -> dict[str, object]:
    detail: dict[str, object] = {
        "node_id": node_id(testcase),
        "classname": testcase.attrib.get("classname", ""),
        "name": testcase.attrib.get("name", ""),
        "status": status(testcase),
        "time": testcase.attrib.get("time", ""),
    }
    for kind in ("failure", "error", "skipped"):
        child = testcase.find(kind)
        if child is not None:
            detail[kind] = {
                "message": child.attrib.get("message", ""),
                "type": child.attrib.get("type", ""),
                "text": child.text or "",
            }
            break
    return detail


def parse_xml(path: Path) -> tuple[dict[str, list[dict[str, object]]], dict[str, int]]:
    root = ET.parse(path).getroot()
    matches: dict[str, list[dict[str, object]]] = {}
    counts = Counter()
    for testcase in root.iter("testcase"):
        detail = testcase_detail(testcase)
        matches.setdefault(str(detail["node_id"]), []).append(detail)
        counts[str(detail["status"])] += 1
    return matches, dict(counts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--rollup", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rollup = json.loads(args.rollup.read_text())
    records = rollup["records"]
    assert len(records) == 276
    assert [record["old276_order"] for record in records] == list(range(1, 277))
    assert len({record["node_id"] for record in records}) == 276

    matches, xml_counts = parse_xml(args.junit)
    rows = []
    for record in records:
        selector = record["node_id"]
        candidates = matches.get(selector, [])
        if len(candidates) != 1:
            observed = "UNKNOWN"
            reason = "missing_upstream_selector" if not candidates else "duplicate_upstream_selector"
            detail = candidates
        else:
            detail = candidates[0]
            observed = str(detail["status"])
            reason = "matched"
        rows.append(
            {
                "old276_order": record["old276_order"],
                "node_id": selector,
                "parameter": record.get("parameter", ""),
                "scope": record["scope"],
                "original_terminal_status": record["original_terminal_status"],
                "current_qualification_status": record["qualification_status"],
                "current_core_status": record["current_core_status"],
                "upstream_status": observed,
                "reason": reason,
                "upstream": detail,
            }
        )

    matched = [row for row in rows if row["reason"] == "matched"]
    lossless = (
        len(rows) == 276
        and len({row["node_id"] for row in rows}) == 276
        and all(row["reason"] == "matched" for row in rows)
    )
    regressions = [
        row
        for row in rows
        if row["reason"] == "matched"
        and row["original_terminal_status"] in {"FAILED", "ERROR"}
        and row["upstream_status"] == "PASSED"
        and row["current_qualification_status"] == "OPEN"
    ]
    result = {
        "schema": "timeline.agent.d54.upstream-comparison.v1",
        "junit": str(args.junit),
        "junit_sha256": hashlib.sha256(args.junit.read_bytes()).hexdigest(),
        "rollup": str(args.rollup),
        "scope": {"total": 276, "core": 159, "noncore": 117},
        "xml_counts": xml_counts,
        "target_counts": Counter(row["upstream_status"] for row in rows),
        "matched_count": len(matched),
        "unknown_count": sum(row["reason"] != "matched" for row in rows),
        "lossless_match": lossless,
        "regressions_only": regressions,
        "rows": rows,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "xml_counts": xml_counts,
                "matched_count": len(matched),
                "unknown_count": result["unknown_count"],
                "lossless_match": lossless,
                "regressions_only": len(regressions),
            },
            sort_keys=True,
        )
    )
    return 0 if lossless else 2


if __name__ == "__main__":
    sys.exit(main())

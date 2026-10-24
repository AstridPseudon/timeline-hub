#!/usr/bin/env python3
"""Extract bounded, source-addressed traces from the retained Farm log.

This is intentionally a standalone evidence tool.  It does not import the
Agent package, run pytest, inspect the environment, or classify a failure.
The Farm operator supplies the original log and the three published node-ID
lists.  The original log is only read; it is never rewritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

EXPECTED_LOG_SHA256 = "06d435fed2622a4d9a8680e1071a650d5e34272090b08af5fe3ba0bd274dea06"

PUBLISHED_INPUTS = {
    "closed_historical": {
        "expected_basename": (
            "agt-farm-diff-0626-closed-historical-172-farm-failed-possible-regression.txt"
        ),
        "expected_sha256": "aeff099ae728712c35b58d8b3de0386cba39ff7f0ff7d064a40bc1981cb8aeef",
        "expected_lines": 88,
    },
    "closed_newer": {
        "expected_basename": (
            "agt-farm-diff-0626-closed-newer-proof-30-farm-failed-not-backdated.txt"
        ),
        "expected_sha256": "440583ed6724c4407845a06a1b1dffe135320a8f53446d2ef0ccba8e4bbf51b6",
        "expected_lines": 8,
    },
    "errored": {
        "expected_basename": "agt-farm-diff-0626-unresolved-farm-errored-187.txt",
        "expected_sha256": "0d63c121c5c9f526eb89b86816a56d444d00c09055ad8cd4ce0d6ccf1d176125",
        "expected_lines": 187,
    },
}

MAX_TRACE_LINES = 240
MAX_TRACE_BYTES = 48 * 1024

RETAINED_CHECKPOINT_COUNTS = {
    "failed_summary": 288,
    "failed_list_lines": 281,
    "failed_list_missing_from_summary": 7,
    "errored_list_lines": 187,
    "closed_failures_in_this_manifest": 96,
}

# Redact whole lines that look like credentials or package-index settings.
# The raw source digest and offsets still refer to the unredacted source.
SECRET_LINE_RE = re.compile(
    r"(?ix)"
    r"(?:\b(?:api[_ -]?key|access[_ -]?key|secret|password|passwd|token|authorization)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\b(?:api[_ -]?key|access[_ -]?key|secret|password|passwd|token)\b"
    r"\s+[A-Za-z0-9._~+/=-]{8,}"
    r"|\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"
    r"|\b(?:extra[_ -]?index[_ -]?url|index[_ -]?url|pip[_ -]?index[_ -]?url)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\b(?:aws_access_key_id|aws_secret_access_key|npm[_ -]?token)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\b(?:codex|openai|anthropic)[-_]?(?:api[_ -]?key|token|secret)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\bhttps?://[^\s/@:]+:[^\s/@]+@)"
)

HEADER_RE = re.compile(r"^\s*_+\s+(?P<body>.+?)\s+_+\s*$")
SEPARATOR_RE = re.compile(
    r"^\s*=+\s+(?:FAILURES|ERRORS|short test summary info|warnings summary)\s*=+\s*$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LogLine:
    number: int
    start: int
    end: int
    text: str

    @property
    def content(self) -> str:
        return self.text.rstrip("\r\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def hash_path(path: Path) -> tuple[str | None, str | None]:
    """Return (digest, error) without exposing file contents in errors."""

    try:
        with path.open("rb") as handle:
            digest = hashlib.sha256()
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
            return digest.hexdigest(), None
    except OSError as exc:
        return None, f"{type(exc).__name__}: {exc}"


def read_id_file(role: str, path: Path) -> tuple[dict, list[str]]:
    expected = PUBLISHED_INPUTS[role]
    record = {
        "role": role,
        "path": str(path),
        "expected_basename": expected["expected_basename"],
        "expected_sha256": expected["expected_sha256"],
        "expected_line_count": expected["expected_lines"],
        "actual_sha256": None,
        "line_count": None,
    }
    errors: list[str] = []
    try:
        data = path.read_bytes()
    except OSError as exc:
        errors.append(f"{role}: cannot read published ID file: {type(exc).__name__}: {exc}")
        record["error"] = "missing_or_unreadable"
        return record, errors

    actual_hash = sha256_bytes(data)
    record["actual_sha256"] = actual_hash
    if actual_hash != expected["expected_sha256"]:
        errors.append(f"{role}: published ID file SHA-256 mismatch")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{role}: published ID file is not valid UTF-8 at byte {exc.start}")
        record["error"] = "invalid_utf8"
        return record, errors

    ids = text.splitlines()
    record["line_count"] = len(ids)
    if len(ids) != expected["expected_lines"]:
        errors.append(
            f"{role}: expected {expected['expected_lines']} exact node IDs, found {len(ids)}"
        )
    if any(not node_id or "\x00" in node_id for node_id in ids):
        errors.append(f"{role}: blank or NUL-containing node ID")
    record["ids"] = ids
    return record, errors


def decode_log_lines(data: bytes) -> list[LogLine]:
    """Decode strict UTF-8 while preserving byte offsets for every line."""

    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        raise

    lines: list[LogLine] = []
    offset = 0
    for number, raw_line in enumerate(data.splitlines(keepends=True), start=1):
        end = offset + len(raw_line)
        lines.append(LogLine(number, offset, end, raw_line.decode("utf-8")))
        offset = end
    if offset < len(data):
        raw_line = data[offset:]
        lines.append(LogLine(len(lines) + 1, offset, len(data), raw_line.decode("utf-8")))
    return lines


def header_body(content: str) -> str | None:
    match = HEADER_RE.match(content)
    return match.group("body").strip() if match else None


def header_kind(content: str, node_id: str) -> str | None:
    """Recognize only pytest section headers, never short-summary lines."""

    body = header_body(content)
    if body is None:
        return None
    test_name = node_id.rsplit("::", 1)[-1]
    for kind, prefix in (
        ("setup", "ERROR at setup of "),
        ("teardown", "ERROR at teardown of "),
        ("call", "ERROR at call of "),
    ):
        if body.startswith(prefix) and body[len(prefix) :] in (node_id, test_name):
            return kind
    if body in (node_id, test_name):
        return "failure"
    return None


def source_path_hits(lines: Sequence[LogLine], start: int, end: int, source_path: str) -> list[int]:
    """Find traceback/source references to the exact file part of a node ID."""

    exact_source = re.compile(
        r"(?<![A-Za-z0-9_./-])" + re.escape(source_path) + r"(?=[:\s\]\)])"
    )
    return [
        index
        for index in range(start, end)
        if exact_source.search(lines[index].content)
    ]


def section_end(lines: Sequence[LogLine], start: int) -> int:
    for index in range(start + 1, len(lines)):
        content = lines[index].content
        if header_body(content) is not None or SEPARATOR_RE.match(content):
            return index
    return len(lines)


def bounded_end(lines: Sequence[LogLine], start: int, natural_end: int) -> tuple[int, bool]:
    limit = min(natural_end, start + MAX_TRACE_LINES)
    index = start
    while index < limit and lines[index].end - lines[start].start <= MAX_TRACE_BYTES:
        index += 1
    truncated = index < natural_end
    if index == start:
        # A pathological single line is not emitted partially: retaining only
        # the header keeps the byte range exact and the result bounded.
        index = min(start + 1, natural_end)
        truncated = True
    return index, truncated


def redact_trace(lines: Sequence[LogLine], start: int, end: int) -> tuple[str, int]:
    chunks: list[str] = []
    redactions = 0
    for line in lines[start:end]:
        text = line.text
        if SECRET_LINE_RE.search(line.content):
            redactions += 1
            newline = "\n" if text.endswith("\n") else ""
            if text.endswith("\r\n"):
                newline = "\r\n"
            chunks.append("[REDACTED SECRET/TOKEN/INDEX-URL LINE]" + newline)
        else:
            chunks.append(text)
    return "".join(chunks), redactions


def all_byte_occurrences(haystack: bytes, needle: bytes, limit: int = 32) -> list[int]:
    offsets: list[int] = []
    offset = 0
    while len(offsets) < limit:
        found = haystack.find(needle, offset)
        if found < 0:
            break
        offsets.append(found)
        offset = found + max(len(needle), 1)
    return offsets


def extract_record(
    node_id: str,
    lines: Sequence[LogLine],
    source_data: bytes,
    *,
    require_setup: bool = False,
) -> dict:
    source_path = node_id.split("::", 1)[0]
    candidates: list[tuple[int, int, str, list[int]]] = []
    for index, line in enumerate(lines):
        kind = header_kind(line.content, node_id)
        if kind is None or (require_setup and kind != "setup"):
            continue
        natural_end = section_end(lines, index)
        source_hits = source_path_hits(lines, index, natural_end, source_path)
        full_node_id_in_header = node_id in line.content
        if not full_node_id_in_header and not source_hits:
            continue
        candidates.append((index, natural_end, kind, source_hits))

    base = {
        "original_id": node_id,
        "source_file": source_path,
        "matching_criteria": (
            "one pytest underscore header whose exact node ID or exact test-name "
            "matches, plus an exact source-file reference in the same bounded section; "
            "short-summary lines are never sections"
        ),
        "evidence_kind": "setup_header_section" if require_setup else "failure_section",
        "cause_classification": "unknown_not_classified",
        "pass_classification": "unknown_not_inferred",
        "source_offsets": None,
        "source_slice_sha256": None,
        "bounded_trace_sha256": None,
        "redaction_count": 0,
        "bounded_trace": None,
    }
    if len(candidates) != 1:
        base["status"] = "ambiguous" if candidates else "missing"
        base["match_reason"] = (
            "multiple exact header/source matches"
            if candidates
            else "no unique exact pytest header/source-file match"
        )
        base["candidate_offsets"] = [
            {"start_byte": lines[item[0]].start, "end_byte": lines[item[1] - 1].end}
            for item in candidates
        ]
        base["unmatched_node_id_byte_offsets"] = all_byte_occurrences(
            source_data, node_id.encode("utf-8")
        )
        return base

    start, natural_end, kind, source_hits = candidates[0]
    end, truncated = bounded_end(lines, start, natural_end)
    start_byte = lines[start].start
    end_byte = lines[end - 1].end
    raw_trace = source_data[start_byte:end_byte]
    redacted_trace, redaction_count = redact_trace(lines, start, end)
    base.update(
        {
            "status": "found",
            "header_kind": kind,
            "header_line": lines[start].number,
            "source_match_lines": [lines[index].number for index in source_hits],
            "source_offsets": {
                "start_byte": start_byte,
                "end_byte_exclusive": end_byte,
                "start_line": lines[start].number,
                "end_line": lines[end - 1].number,
            },
            "trace_truncated": truncated,
            "source_slice_sha256": sha256_bytes(raw_trace),
            "bounded_trace_sha256": sha256_bytes(redacted_trace.encode("utf-8")),
            "redaction_count": redaction_count,
            "bounded_trace": redacted_trace,
        }
    )
    return base


def input_error_manifest(command: str, inputs: dict, errors: Iterable[str]) -> dict:
    return {
        "schema": "timeline.farm-trace-manifest.v1",
        "status": "input_error",
        "cli_command": command,
        "expected_log_sha256": EXPECTED_LOG_SHA256,
        "retained_checkpoint_counts": RETAINED_CHECKPOINT_COUNTS,
        "inputs": inputs,
        "errors": list(errors),
        "note": "No trace or cause classification is produced from invalid or missing input.",
    }


def write_manifest(output_dir: Path, manifest: dict) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "farm-trace-manifest.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only extraction of bounded pytest traces from the retained Farm log. "
            "Requires the exact published 88, 8, and 187 ID files."
        )
    )
    parser.add_argument("--log-path", required=True, type=Path, help="Existing Farm log; never rewritten.")
    parser.add_argument("--closed-historical", required=True, type=Path, help="Published 88-ID file.")
    parser.add_argument("--closed-newer", required=True, type=Path, help="Published 8-ID file.")
    parser.add_argument("--errored", required=True, type=Path, help="Published 187-ID setup-error file.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for the JSON manifest.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    actual_argv = list(sys.argv[1:] if argv is None else argv)
    command = shlex.join(["python3", "evidence/extract_farm_traces.py", *actual_argv])
    args = parse_args(actual_argv)

    paths = {
        "closed_historical": args.closed_historical,
        "closed_newer": args.closed_newer,
        "errored": args.errored,
    }
    input_records: dict[str, dict] = {}
    errors: list[str] = []
    id_lists: dict[str, list[str]] = {}
    for role, path in paths.items():
        record, file_errors = read_id_file(role, path)
        input_records[role] = record
        errors.extend(file_errors)
        if "ids" in record:
            id_lists[role] = record["ids"]

    all_closed = id_lists.get("closed_historical", []) + id_lists.get("closed_newer", [])
    if len(all_closed) == 96 and len(set(all_closed)) != 96:
        errors.append("closed ID files contain duplicate node IDs")
    if len(set(id_lists.get("errored", []))) != len(id_lists.get("errored", [])):
        errors.append("errored ID file contains duplicate node IDs")

    log_record = {
        "path": str(args.log_path),
        "expected_sha256": EXPECTED_LOG_SHA256,
        "before_sha256": None,
        "after_sha256": None,
        "immutable_before_after": False,
    }
    input_records["log"] = log_record
    before_hash, before_error = hash_path(args.log_path)
    log_record["before_sha256"] = before_hash
    if before_error:
        errors.append(f"log: cannot read or hash source log: {before_error}")
    elif before_hash != EXPECTED_LOG_SHA256:
        errors.append("log: source SHA-256 does not match the required Farm26511 digest")

    source_data: bytes | None = None
    source_text: str | None = None
    if not errors:
        try:
            source_data = args.log_path.read_bytes()
            source_text = source_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"log: invalid UTF-8 at byte {exc.start}; no faithful trace can be emitted")
        except OSError as exc:
            errors.append(f"log: cannot read source log: {type(exc).__name__}: {exc}")

    if source_data is not None:
        after_hash, after_error = hash_path(args.log_path)
        log_record["after_sha256"] = after_hash
        if after_error:
            errors.append(f"log: cannot re-hash source log after read: {after_error}")
        log_record["immutable_before_after"] = (
            before_hash == after_hash == EXPECTED_LOG_SHA256 and after_error is None
        )
        if not log_record["immutable_before_after"]:
            errors.append("log: source changed or could not be verified byte-identical before/after read")

    if errors or source_data is None or source_text is None:
        manifest = input_error_manifest(command, input_records, errors)
        try:
            write_manifest(args.output_dir, manifest)
        except OSError as exc:
            print(f"input_error: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print("input_error: see farm-trace-manifest.json", file=sys.stderr)
        return 2

    try:
        lines = decode_log_lines(source_data)
    except UnicodeDecodeError as exc:
        manifest = input_error_manifest(
            command,
            input_records,
            [f"log: invalid UTF-8 at byte {exc.start}; no faithful trace can be emitted"],
        )
        write_manifest(args.output_dir, manifest)
        print("input_error: invalid UTF-8 in source log", file=sys.stderr)
        return 2

    closed_records = [
        extract_record(node_id, lines, source_data)
        for node_id in all_closed
    ]
    setup_records = [
        extract_record(node_id, lines, source_data, require_setup=True)
        for node_id in id_lists["errored"]
    ]
    counts = {
        "closed_total": len(closed_records),
        "closed_found": sum(item["status"] == "found" for item in closed_records),
        "closed_ambiguous": sum(item["status"] == "ambiguous" for item in closed_records),
        "closed_missing": sum(item["status"] == "missing" for item in closed_records),
        "setup_error_total": len(setup_records),
        "setup_excerpt_found": sum(item["status"] == "found" for item in setup_records),
        "setup_excerpt_ambiguous": sum(item["status"] == "ambiguous" for item in setup_records),
        "setup_excerpt_missing": sum(item["status"] == "missing" for item in setup_records),
    }
    manifest = {
        "schema": "timeline.farm-trace-manifest.v1",
        "status": "complete",
        "cli_command": command,
        "expected_log_sha256": EXPECTED_LOG_SHA256,
        "source_log": input_records["log"],
        "retained_checkpoint_counts": RETAINED_CHECKPOINT_COUNTS,
        "retained_format": (
            "pytest-xdist terminal output: underscore-delimited failure/setup headers and "
            "bounded sections ending at the next header or summary separator"
        ),
        "published_id_sources": {
            role: {key: value for key, value in record.items() if key != "ids"}
            for role, record in input_records.items()
            if role != "log"
        },
        "counts": counts,
        "closed_failure_records": closed_records,
        "setup_error_records": setup_records,
        "classification_note": (
            "This tool preserves evidence only. Causes, environment/regression status, and PASS "
            "are deliberately unknown and must be classified by the Agent worker from the raw evidence."
        ),
    }
    try:
        target = write_manifest(args.output_dir, manifest)
    except OSError as exc:
        print(f"output_error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

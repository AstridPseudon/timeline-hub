#!/usr/bin/env python3
"""Extract bounded, source-addressed traces from the retained Farm log.

This is intentionally a standalone management-evidence tool for the Farm Lead
to run once against an existing retained log.  It does not import the Agent
package, run pytest, inspect the environment, or classify a failure.  There is
no product caller.  The operator supplies the original log and the three
published node-ID lists.  The original log is only read; it is never rewritten.

Supported CLI::

    python3 evidence/extract_farm_traces.py --log-path LOG \
        --closed-historical CLOSED_HISTORICAL --closed-newer CLOSED_NEWER \
        --errored ERRORED --output-dir OUTPUT_DIR
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
    "historical_closed_uncredited": 88,
    "newer_closed_uncredited": 8,
}

FROZEN_SCOPE = {
    "label": "frozen202/65",
    "official_current_census": {"closed": 202, "open": 65},
    "manifest_closed_subset": {
        "historical": 88,
        "newer": 8,
        "total": 96,
        "attribution": "uncredited",
    },
    "caller": {
        "kind": "standalone_management_evidence_tool",
        "operator": "FARM LEAD",
        "run_count": "once against an existing retained log",
        "product_caller": "none; no production caller is required",
    },
}

CHECKPOINT_RECONCILIATION = {
    "original_checkpoint_failed": 288,
    "retained_failure_lines": 281,
    "missing_from_retained_failure_lines": 7,
    "equation": "281 retained failure lines + 7 missing lines = 288 checkpoint failures",
    "setup_lines": 187,
}

OUTPUT_POLICY = {
    "max_trace_lines": MAX_TRACE_LINES,
    "max_trace_bytes": MAX_TRACE_BYTES,
    "trace_bound": (
        "The emitted source slice is at most max_trace_bytes and max_trace_lines; "
        "an oversized first line ends at the UTF-8 byte boundary inside that line."
    ),
    "offsets": (
        "start_byte and end_byte_exclusive address the exact unredacted source bytes; "
        "end_byte_exclusive is the true truncation boundary."
    ),
    "trace_content": "Unmodified retained bytes except disclosed whole-line redactions.",
    "redaction": {
        "whole_line": True,
        "criteria": [
            "credential/token/secret/password/authorization assignments or bearer values",
            "credentialed HTTP(S) URLs",
            "Looking in indexes: lines, including uncredentialed URLs",
            "index-url, extra-index-url, pip-index-url, pypi-url, and UV index settings",
            "AWS access/secret keys, npm tokens, and Codex/OpenAI/Anthropic key settings",
        ],
        "replacement": "[REDACTED SECRET/TOKEN/INDEX-URL LINE]",
    },
    "classification": {
        "cause": "unknown_not_classified",
        "pass": "unknown_not_inferred",
        "missing_or_ambiguous": "unknown; no pass, environment, or regression inference",
    },
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
    r"|\b(?:pip[_ -]?(?:extra[_ -]?)?index[_ -]?url|pypi[_ -]?url|uv[_ -]?(?:default[_ -]?)?index[_ -]?url)\b"
    r"\s*(?:=|:|\s)\s*\S+"
    r"|(?:^|\s)--(?:extra-)?index-url\s+(?:=\s*)?\S+"
    r"|\b(?:aws_access_key_id|aws_secret_access_key|npm[_ -]?token)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\b(?:codex|openai|anthropic)[-_]?(?:api[_ -]?key|token|secret)\b"
    r"\s*(?:=|:)\s*\S+"
    r"|\bhttps?://[^\s/@:]+:[^\s/@]+@"
    r"|^\s*looking\s+in\s+indexes\s*:)"
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


def read_bytes_snapshot(path: Path) -> tuple[bytes | None, str | None, str | None]:
    """Return the exact bytes read, their digest, and a bounded error."""
    try:
        data = path.read_bytes()
        return data, sha256_bytes(data), None
    except OSError as exc:
        return None, None, f"{type(exc).__name__}: {exc}"


def read_id_file(role: str, path: Path) -> tuple[dict, list[str]]:
    expected = PUBLISHED_INPUTS[role]
    record = {
        "role": role,
        "path": str(path),
        "expected_basename": expected["expected_basename"],
        "expected_sha256": expected["expected_sha256"],
        "expected_line_count": expected["expected_lines"],
        "before_sha256": None,
        "used_sha256": None,
        "after_sha256": None,
        "immutable_before_after": False,
        "line_count": None,
    }
    errors: list[str] = []
    data, used_hash, read_error = read_bytes_snapshot(path)
    record["before_sha256"] = used_hash
    record["used_sha256"] = used_hash
    if read_error:
        errors.append(f"{role}: cannot read published ID file: {read_error}")
        record["error"] = "missing_or_unreadable"
        return record, errors

    if used_hash != expected["expected_sha256"]:
        errors.append(f"{role}: published ID file SHA-256 mismatch")

    after_data, after_hash, after_error = read_bytes_snapshot(path)
    record["after_sha256"] = after_hash
    record["immutable_before_after"] = (
        after_error is None and after_data == data and after_hash == used_hash
    )
    if after_error:
        errors.append(f"{role}: cannot re-read published ID file after parsing: {after_error}")
    elif not record["immutable_before_after"]:
        errors.append(f"{role}: published ID file changed during the read")

    if not record["immutable_before_after"]:
        record["error"] = "mutated_during_read"

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


def utf8_prefix_length(text: str, byte_limit: int) -> int:
    """Return a strict UTF-8 character boundary no larger than byte_limit."""

    encoded = text.encode("utf-8")
    if len(encoded) <= byte_limit:
        return len(encoded)
    while byte_limit and (encoded[byte_limit] & 0xC0) == 0x80:
        byte_limit -= 1
    return byte_limit


def bounded_end(
    lines: Sequence[LogLine], start: int, natural_end: int
) -> tuple[int, int, bool, str]:
    """Return (end line, end byte, truncated, boundary) for one trace."""

    limit = min(natural_end, start + MAX_TRACE_LINES)
    byte_limit = lines[start].start + MAX_TRACE_BYTES
    index = start
    while index < limit and lines[index].end <= byte_limit:
        index += 1
    truncated = index < natural_end
    if index == start:
        # Keep the source slice bounded even when the first line is oversized.
        # The end offset is therefore allowed to fall inside that line.
        index = start + 1
        end_byte = lines[start].start + utf8_prefix_length(
            lines[start].text, MAX_TRACE_BYTES
        )
        return index, end_byte, True, "byte_limit_inside_line"

    end_byte = lines[index - 1].end
    boundary = "line"
    if index == limit and limit < natural_end:
        truncated = True
        boundary = "line_limit"
    elif index < natural_end:
        boundary = "byte_limit"
    return index, end_byte, truncated, boundary


def redact_trace(
    lines: Sequence[LogLine], source_data: bytes, start: int, end: int, end_byte: int
) -> tuple[str, int]:
    chunks: list[str] = []
    redactions = 0
    for line in lines[start:end]:
        if line.start >= end_byte:
            break
        raw = source_data[line.start : min(line.end, end_byte)]
        text = raw.decode("utf-8")
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
    end, end_byte, truncated, boundary = bounded_end(lines, start, natural_end)
    start_byte = lines[start].start
    raw_trace = source_data[start_byte:end_byte]
    redacted_trace, redaction_count = redact_trace(lines, source_data, start, end, end_byte)
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
            "trace_boundary": boundary,
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
        "supported_cli": (
            "python3 evidence/extract_farm_traces.py --log-path LOG "
            "--closed-historical CLOSED_HISTORICAL --closed-newer CLOSED_NEWER "
            "--errored ERRORED --output-dir OUTPUT_DIR"
        ),
        "scope": FROZEN_SCOPE,
        "expected_log_sha256": EXPECTED_LOG_SHA256,
        "retained_checkpoint_counts": RETAINED_CHECKPOINT_COUNTS,
        "checkpoint_reconciliation": CHECKPOINT_RECONCILIATION,
        "output_policy": OUTPUT_POLICY,
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
        "used_sha256": None,
        "after_sha256": None,
        "immutable_before_after": False,
    }
    input_records["log"] = log_record
    source_data, source_hash, source_error = read_bytes_snapshot(args.log_path)
    log_record["before_sha256"] = source_hash
    log_record["used_sha256"] = source_hash
    if source_error:
        errors.append(f"log: cannot read source log: {source_error}")
    elif source_hash != EXPECTED_LOG_SHA256:
        errors.append("log: source SHA-256 does not match the required Farm26511 digest")

    after_data, after_hash, after_error = read_bytes_snapshot(args.log_path)
    log_record["after_sha256"] = after_hash
    log_record["immutable_before_after"] = (
        source_error is None
        and after_error is None
        and after_data == source_data
        and after_hash == source_hash
    )
    if after_error:
        errors.append(f"log: cannot re-read source log after parsing snapshot: {after_error}")
    elif not log_record["immutable_before_after"]:
        errors.append("log: source changed during the read")

    if errors or source_data is None:
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
        "supported_cli": (
            "python3 evidence/extract_farm_traces.py --log-path LOG "
            "--closed-historical CLOSED_HISTORICAL --closed-newer CLOSED_NEWER "
            "--errored ERRORED --output-dir OUTPUT_DIR"
        ),
        "scope": FROZEN_SCOPE,
        "expected_log_sha256": EXPECTED_LOG_SHA256,
        "source_log": input_records["log"],
        "retained_checkpoint_counts": RETAINED_CHECKPOINT_COUNTS,
        "checkpoint_reconciliation": CHECKPOINT_RECONCILIATION,
        "output_policy": OUTPUT_POLICY,
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
            "are deliberately unknown; absence from this retained log cannot prove PASS, "
            "environment-only failure, or regression."
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

"""Offline controls for the owner-installed WC6 capture attachment."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path

import pytest

from tests.helpers import run_wc6_completion_capture as runner


def test_wc6_runner_guards_argv_helper_sink_budgets_and_retention(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    helper = Path(runner.__file__).with_name(runner.HELPER_NAME)
    assert runner.verify_helper(helper, helper.parent) == helper

    altered_dir = tmp_path / "altered"
    altered_dir.mkdir()
    altered = altered_dir / runner.HELPER_NAME
    altered.write_bytes(helper.read_bytes() + b"\n")
    with pytest.raises(runner.AttachmentRefused, match="hash mismatch"):
        runner.verify_helper(altered, altered_dir)
    with pytest.raises(runner.AttachmentRefused, match="origin mismatch"):
        runner.verify_helper(helper, tmp_path)

    monkeypatch.setattr(runner, "_git", lambda *args: "wrong-source")
    with pytest.raises(runner.AttachmentRefused, match="Agent source guard mismatch"):
        runner.verify_pinned_sources(tmp_path, tmp_path)

    sink = runner.verify_sink(tmp_path / "packet.jsonl", tmp_path)
    outside = tmp_path.parent / "packet.jsonl"
    with pytest.raises(runner.AttachmentRefused, match="outside TMPDIR"):
        runner.verify_sink(outside, tmp_path)

    command = runner.pytest_command(sink)
    assert command[0] == runner.sys.executable
    assert command[1:4] == ["-P", "-m", "pytest"]
    assert "--timeout=45" in command and "-m" in command and "integration" in command
    assert command[-1] == runner.ORIGINAL
    assert runner.MAX_PACKET_BYTES == 4 * 1024 * 1024
    with pytest.raises(runner.AttachmentRefused, match="exact WC6 selector"):
        runner.main(["other-test.py::test_not_wc6"])

    missing_output = io.BytesIO()
    assert runner.retain_packet(tmp_path / "missing.jsonl", 1, missing_output) == (1, "missing")
    assert b"WC6_COMPLETION_PACKET_MISSING" in missing_output.getvalue()
    missing_success = io.BytesIO()
    assert runner.retain_packet(tmp_path / "missing-success.jsonl", 0, missing_success) == (
        runner.MISSING_PACKET_EXIT,
        "missing",
    )

    packet = b'{"phase":"capture.end","selected":true}\n'
    sink.write_bytes(packet)
    retained = io.BytesIO()
    assert runner.retain_packet(sink, 7, retained) == (7, "complete")
    log = retained.getvalue()
    start = log.index(b"\n") + 1
    end = log.index(b"\nWC6_COMPLETION_PACKET_END", start)
    assert log[start : end + 1] == packet
    assert hashlib.sha256(packet).hexdigest().encode() in log

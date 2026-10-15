"""Small platform checks for V6; the full journey is the merge gate."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import sys

from astrid.core.dev import journey
from astrid.core.dev.journey import JourneyFailure, Runner, _doctor_ready, _find_output, select_reference_realm
from astrid.core.gateway.dev_operator import main as dev_main


def test_reference_realm_is_selected_from_catalog_without_copying(tmp_path: Path) -> None:
    reference = tmp_path / "reference"
    realm = reference / "runtime" / "realms" / "realm-1"
    realm.mkdir(parents=True)
    (realm / "realm.sqlite3").write_bytes(b"frozen database")
    (reference / "runtime" / "catalog.json").write_text(json.dumps({
        "selected_realm_id": "realm-1", "realms": [{"realm_id": "realm-1", "data_root": str(realm)}],
    }))
    before = sorted(p.name for p in tmp_path.rglob("*"))
    assert select_reference_realm(reference) == ("realm-1", realm)
    assert sorted(p.name for p in tmp_path.rglob("*")) == before


def test_clone_refuses_catalog_outside_reference(tmp_path: Path) -> None:
    reference = tmp_path / "reference"
    realm = reference / "runtime" / "realms" / "realm-1"
    realm.mkdir(parents=True)
    (realm / "realm.sqlite3").write_bytes(b"db")
    (reference / "runtime" / "catalog.json").write_text(json.dumps({
        "selected_realm_id": "realm-1", "realms": [{"realm_id": "realm-1", "data_root": str(tmp_path / "other")}],
    }))
    with pytest.raises(JourneyFailure, match="reference: catalog realm"):
        select_reference_realm(reference)


def test_doctor_requires_healthy_runtime_and_usable_renderer_node() -> None:
    assert _doctor_ready({"healthy": True, "renderer_node": {"status": "ok"}})
    assert not _doctor_ready({"healthy": False, "renderer_node": {"status": "ok"}})
    assert not _doctor_ready({"renderer_node": {"status": "unknown"}})
    assert not _doctor_ready({"ok": False, "renderer_node": {"status": "ok"}})


def test_render_output_is_actual_prefixed_file(tmp_path: Path) -> None:
    output = tmp_path / "123-v6-1-abc.mp4"
    output.write_bytes(b"video")
    assert _find_output(tmp_path, "v6-1-abc.mp4") == output
    with pytest.raises(JourneyFailure, match="found 0"):
        _find_output(tmp_path, "v6-1-abc.mp4", exclude={output})
    with pytest.raises(JourneyFailure, match="found 0"):
        _find_output(tmp_path, "missing.mp4")


def test_public_dev_journey_help(capsys) -> None:
    with pytest.raises(SystemExit) as exit_info:
        dev_main(["journey", "--help"])
    assert exit_info.value.code == 0
    assert "--reference" in capsys.readouterr().out


def test_public_journey_refusal_writes_phase_summary(tmp_path: Path, capsys) -> None:
    summary = tmp_path / "result.json"
    assert dev_main(["journey", "--tier", "smoke", "--reference", str(tmp_path / "missing"),
                     "--timeline", "film/main", "--summary", str(summary)]) == 1
    assert json.loads(summary.read_text())["ok"] is False
    assert "FAIL" in summary.with_suffix(".txt").read_text()
    assert "journey:" in capsys.readouterr().err


def test_slow_phase_is_reported_at_the_end_not_killed(tmp_path: Path, monkeypatch) -> None:
    # A command over its budget (but not hung) completes; the overrun is collected for the end.
    monkeypatch.setitem(journey.PHASE_BUDGETS, "adopt", 0.3)
    runner = Runner(tmp_path, tmp_path / "summary.json")
    argv = [sys.executable, "-c", "import time, json; time.sleep(0.8); print(json.dumps({'ok': True}))"]
    assert runner.phase("adopt", lambda: runner.command("adopt", argv, {})) == {"ok": True}
    assert runner.budget_violations and runner.budget_violations[0].startswith("adopt:")


def test_hung_command_is_stopped_at_the_hang_limit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setitem(journey.PHASE_BUDGETS, "adopt", 0.2)
    runner = Runner(tmp_path, tmp_path / "summary.json")
    argv = [sys.executable, "-c", "import time; time.sleep(30)"]
    with pytest.raises(JourneyFailure, match="hung"):
        runner.phase("adopt", lambda: runner.command("adopt", argv, {}))


def test_a_failed_run_keeps_log_tails_but_not_credentials(tmp_path: Path) -> None:
    runtime = tmp_path / "root" / "data" / "runtime"
    (runtime / "credentials").mkdir(parents=True)
    (runtime / "credentials" / "token.json").write_text("secret")
    (runtime / "runtime.log").write_bytes(b"x" * (journey.EVIDENCE_TAIL_BYTES + 10) + b"END")
    kept = journey._keep_failure_logs(tmp_path / "root", tmp_path / "summary.json")
    assert kept == str(tmp_path / "summary-evidence")
    tail = (tmp_path / "summary-evidence" / "runtime.log").read_bytes()
    assert tail.endswith(b"END") and len(tail) == journey.EVIDENCE_TAIL_BYTES
    assert not (tmp_path / "summary-evidence" / "credentials").exists()
    assert journey._keep_failure_logs(tmp_path / "empty", tmp_path / "s2.json") is None


def _ps(*rows):
    return [{"pid": p, "ppid": pp, "pgid": p, "command": c} for p, pp, c in rows]


def test_run_id_is_found_anywhere_in_a_large_result() -> None:
    run_id = "ab" * 16
    doc = {"ok": True, "outputs": {"artifacts": [{"n": i} for i in range(5000)]}, "data": [{"x": {"run_id": run_id}}]}
    assert journey.find_run_id(doc) == run_id
    assert journey.find_run_id({"run_id": "short"}) is None
    assert journey.find_run_id({"ok": True}) is None


def test_json_output_tolerates_a_preamble_but_not_garbage() -> None:
    assert journey.parse_json_output('notice: warming up\n{"ok": true, "n": [1, 2]}\n') == {"ok": True, "n": [1, 2]}
    assert journey.parse_json_output('{"ok": true}') == {"ok": True}
    with pytest.raises(json.JSONDecodeError):
        journey.parse_json_output("no json here")


def test_render_processes_are_the_hosts_remotion_descendants_only() -> None:
    rows = _ps((10, 1, "python -m astrid.core.execution.generic_host run"), (11, 10, "python worker"),
               (12, 11, "node remotion render"), (13, 12, "Google Chrome Headless Shell"),
               (20, 1, "node remotion render"), (30, 10, "ffmpeg -i x"))
    assert [r["pid"] for r in journey.render_processes(rows, 10)] == [12, 13, 30]
    assert [r["pid"] for r in journey.descendants(rows, 10)] == [11, 12, 13, 30]
    assert journey.render_processes(rows, 99) == []


def test_duplicate_path_repeats_every_entry() -> None:
    doubled = journey.with_duplicate_path("/a:/b")
    assert doubled.split(":") == ["/a", "/b", "/a", "/b"]
    assert journey.with_duplicate_path("") == ""


def test_host_record_and_liveness(tmp_path: Path) -> None:
    import os
    assert journey.read_host(tmp_path) == {}
    runtime = tmp_path / "data" / "runtime"
    runtime.mkdir(parents=True)
    (runtime / "generic-host.json").write_text(json.dumps({"pid": os.getpid()}))
    assert journey.read_host(tmp_path)["pid"] == os.getpid()
    assert journey.pid_alive(os.getpid()) and not journey.pid_alive(None) and not journey.pid_alive(2**22 + 12345)


def test_wait_for_returns_when_true_or_falsy_at_deadline() -> None:
    calls = iter([0, 0, "yes"])
    assert journey.wait_for(lambda: next(calls), 5, interval=0.01) == "yes"
    assert not journey.wait_for(lambda: False, 0.05, interval=0.01)


def test_the_probe_file_is_inside_the_host_source_closure() -> None:
    # The source-change phase appends to journey.py; that must change the host's closure digest.
    from astrid.core.execution.generic_host import source_checkout_closure
    checkout = Path(journey.__file__).resolve().parents[3]
    before = source_checkout_closure(checkout)["digest"]
    path = Path(journey.__file__)
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"\n# probe\n")
        assert source_checkout_closure(checkout)["digest"] != before
    finally:
        path.write_bytes(original)
    assert source_checkout_closure(checkout)["digest"] == before


def test_full_tier_is_accepted_and_unknown_tier_refused(tmp_path: Path, capsys) -> None:
    summary = tmp_path / "r.json"
    assert dev_main(["journey", "--tier", "full", "--reference", str(tmp_path / "missing"),
                     "--timeline", "film/main", "--summary", str(summary)]) == 1
    assert "full" in summary.with_suffix(".txt").read_text()
    with pytest.raises(SystemExit):
        dev_main(["journey", "--tier", "bogus", "--reference", "x", "--timeline", "a/b", "--summary", "s"])

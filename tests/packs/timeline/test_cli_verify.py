"""``--timings``: the flag, and the breakdown plus p50/p95 printed from a local log."""
from __future__ import annotations

import argparse
import json

from astrid.packs.timeline import cli_verify


def test_the_timings_flag_parses():
    parser = argparse.ArgumentParser()
    cli_verify.add_timings_flag(parser)
    assert parser.parse_args([]).timings is False
    assert parser.parse_args(["--timings"]).timings is True
    assert "where the time went" in parser.format_help()


def test_print_timings_prints_the_breakdown_and_the_p50_p95_line(tmp_path, capsys):
    rows = [{"ok": True, "cold": False, "total_s": t} for t in (3.0, 4.0, 5.0)]
    rows += [{"ok": True, "cold": True, "total_s": 19.0}, {"ok": False, "cold": False, "total_s": 50.0}]
    (tmp_path / "timings.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    result = {"timing": {"total_s": 4.2, "read_s": 1.3, "media_s": 0.0, "render_s": 2.6, "page_s": 0.3,
                         "worker_overhead_s": 0.3, "cold": False, "retried": False,
                         "jobs": [{"name": "published", "seconds": 1.2, "queuedMs": 0.0, "selectMs": 500.0,
                                   "framesMs": 400.0, "requestMs": 1000.0, "ensureOwnerMs": 0.0},
                                  {"name": "working", "seconds": 1.1}]}}
    cli_verify.print_timings(result, root=tmp_path)
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "timings  total 4.2 s = startup/check 0.0 + read 1.3 + media 0.0 + capture 2.6 + page 0.3 (warm; no retry)"
    assert out[1] == ("         published: 1.2 s (owner: queued 0.0 · select 0.5 · frames 0.4 · request 1.0 · "
                      "ensure 0.0)")
    assert out[2] == "         working: 1.1 s   · worker start/overhead 0.3 s"
    assert out[3] == ("verify   p50 4.0 s · p95 19.0 s over the last 5 (warm 3: p50 4.0 / p95 5.0 · "
                      "cold 1: p50 19.0 / p95 19.0 · failures 1)")


def test_the_bench_script_has_help_and_no_side_effects_before_parsing():
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).resolve().parents[3] / "scripts" / "verify_lane_bench.py"
    done = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0 and "--same" in done.stdout and "--checkout" in done.stdout


def test_the_labels_flag_parses_for_check_and_verify():
    parser = argparse.ArgumentParser()
    cli_verify.add_labels_flag(parser)
    assert parser.parse_args([]).labels is False
    assert parser.parse_args(["--labels"]).labels is True
    assert "address" in parser.format_help()


def test_the_visualize_labels_shorthand_adds_the_labels_layer_once():
    parser = argparse.ArgumentParser()
    cli_verify.add_visualize_labels_flag(parser)
    assert parser.parse_args(["--labels"]).labels is True
    assert cli_verify.with_labels_layer(["sync"], True) == ["sync", "labels"]
    assert cli_verify.with_labels_layer(["labels", "sync"], True) == ["labels", "sync"]
    assert cli_verify.with_labels_layer(None, True) == ["labels"]
    assert cli_verify.with_labels_layer(["sync"], False) == ["sync"]
    assert cli_verify.with_labels_layer(None, False) is None

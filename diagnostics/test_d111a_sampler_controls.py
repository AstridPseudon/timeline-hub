"""Controls for distinct membership, overlap, observation gaps and value bytes."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

SPEC = importlib.util.spec_from_file_location("d111a_observer", Path(__file__).with_name("sitecustomize_d111a.py"))
assert SPEC is not None and SPEC.loader is not None
observer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(observer)


def test_recursion_is_one_membership_and_timestamp_is_retained(monkeypatch):
    code = SimpleNamespace(co_filename="/usr/lib/python3.13/copy.py", co_name="deepcopy", co_firstlineno=62)
    inner = SimpleNamespace(f_code=code, f_back=None)
    outer = SimpleNamespace(f_code=code, f_back=inner)
    request = {"samples": [], "missing_thread_samples": 0, "observer_cpu_ns": 0}
    class OneSample:
        done = False
        def is_set(self):
            return self.done
        def wait(self, interval):
            assert interval == 0.02
            self.done = True
    monkeypatch.setattr(observer, "STOP", OneSample())
    monkeypatch.setattr(observer, "ACTIVE", {99: request})
    monkeypatch.setattr(observer.sys, "_current_frames", lambda: {99: outer})
    observer.sample_stack()
    assert len(request["samples"]) == 1
    assert request["samples"][0]["frames"] == ["<stdlib>/copy.py:deepcopy:62"]
    assert request["samples"][0]["thread_id"] == 99
    assert request["samples"][0]["monotonic_ns"] > 0


def test_union_is_not_additive_and_gaps_remain_visible():
    request = {"start_ns": 0, "end_ns": 100_000_000, "samples": [
        {"monotonic_ns": 10_000_000, "frames": ["copy.py:deepcopy:62", "v.py:finite_json:18"]},
        {"monotonic_ns": 90_000_000, "frames": ["v.py:finite_json:18"]}],
        "values": [], "outer_calls": {}}
    result = observer.summarize(request)
    assert result["sample_total"] == 2
    assert result["deepcopy_finite_json_union_samples"] == 2
    assert result["deepcopy_finite_json_union_frequency"] == 1
    assert result["nominal_window_coverage_ns"] == 40_000_000
    assert result["uncovered_window_ns"] == 60_000_000
    assert result["max_gap_ns"] == 80_000_000
    assert all(row["sample_count"] <= 2 for row in result["top_inclusive_frames"])


def test_byte_accounting_repeated_and_distinct_values_and_exact_limit():
    request = {"values": [], "accounting_cpu_ns": 0, "accounting_wall_ns": 0}
    for value in ({"x": "é"}, {"x": "é"}, {"x": "a"}, object()):
        observer.account(request, "deepcopy", value, {"value_side": "argument[0]"})
    assert [row["bytes"] for row in request["values"]] == [10, 10, 9, None]
    assert request["values"][0]["sha256"] == request["values"][1]["sha256"]
    assert request["values"][0]["sha256"] != request["values"][2]["sha256"]
    assert request["values"][3]["exact_limit"] == "TypeError"

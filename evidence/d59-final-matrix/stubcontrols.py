#!/usr/bin/env python3
"""No-body D59 controls: one positive dispatch and zero poisoned dispatches."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("d59_matrix", HERE / "run-final-matrix.py")
assert SPEC and SPEC.loader
MATRIX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATRIX)


def ready_tuple(root: Path) -> tuple[Path, dict]:
    repos = {}
    for name in MATRIX.REPOS:
        checkout = root / f"checkout-{name}"
        checkout.mkdir()
        receipt = root / f"receipt-{name}.txt"
        receipt.write_text(f"{name} pinned receipt\n", encoding="utf-8")
        identity = ("a" if name == "agent" else "b") * 40
        tree = ("c" if name == "runtime" else "d") * 40
        repos[name] = {"sha": identity, "tree": tree, "source_path": str(checkout), "checkout_path": str(checkout), "checkout_receipt": str(receipt), "checkout_receipt_sha256": MATRIX.sha256(receipt), "checkout_head": identity, "checkout_tree": tree}
    d73 = root / "d73-source-tuple.json"
    d73.write_text(json.dumps({name: {"root": repos[name]["checkout_path"], "sha": repos[name]["sha"], "tree": repos[name]["tree"]} for name in MATRIX.REPOS}, sort_keys=True) + "\n", encoding="utf-8")
    value = {"version": 1, "status": "READY", "final_tuple_sha256": "FINAL_TUPLE_SHA256_PENDING", "d73_source_tuple": str(d73), "d73_tuple_sha256": MATRIX.sha256(d73), "repos": repos, "schema": {"digest": "sha256:" + "e" * 64, "path": "contract/schemas/timeline-config.schema.json"}, "manifest_bindings": {"agent.runtime.lock": "sha256:" + "f" * 64, "runtime.contract": "sha256:" + "0" * 64}, "test_receipts": [{"id": "source-preflight", "sha256": "sha256:" + "1" * 64}], "route_readiness": {route["id"]: "READY" for route in MATRIX.route_table()}, "render_environment": {"status": "PENDING", "receipt": None}}
    path = root / "tuple.json"
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    value["final_tuple_sha256"] = MATRIX.sha256(path)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    value["final_tuple_sha256"] = "FINAL_TUPLE_SHA256_PENDING"
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path, value


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="timeline-d59-controls-") as raw:
        root = Path(raw)
        tuple_path, value = ready_tuple(root)
        tuple_sha = MATRIX.sha256(tuple_path)
        value = MATRIX.load_tuple(tuple_path, tuple_sha, check_git=False)
        log = root / "dispatch.log"
        fake = root / "request-test"
        fake.write_text("#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$D59_LOG\"\nprintf '%s\\n' 'request-id=d59-stub-1'\n", encoding="utf-8")
        fake.chmod(0o755)
        import os
        os.environ["D59_LOG"] = str(log)
        route = next(item for item in MATRIX.route_table() if item["id"] == "runtime-core")
        planned = MATRIX.route_table()
        assert {item["id"] for item in planned} == {"app-p1", "app-p2", "app-p3", "app-core", "agent-p4", "agent-core", "agent-d77-render", "runtime-p5", "runtime-core", "composition-full"}
        assert all(MATRIX.route_plan(item, tuple_path, tuple_sha, HERE / "run-final-matrix.py")["argv"] for item in planned)
        output = MATRIX.dispatch(route, value, tuple_path, tuple_sha, root / "positive.json", fake, HERE / "run-final-matrix.py")
        assert output["returncode"] == 0
        assert log.read_text(encoding="utf-8").count("runtime full") == 1
        assert output["env"]["TIMELINE_FINAL_TUPLE_SHA256"] == tuple_sha
        before = log.read_text(encoding="utf-8")
        pending_route = next(item for item in MATRIX.route_table() if item["id"] == "agent-p4")
        value["route_readiness"]["agent-p4"] = "PENDING"
        try:
            MATRIX.dispatch(pending_route, value, tuple_path, tuple_sha, root / "pending.json", fake, HERE / "run-final-matrix.py")
        except ValueError:
            pass
        else:
            raise AssertionError("pending owner route was dispatched")
        assert log.read_text(encoding="utf-8") == before
        for bad in ("wrong-sha", "missing-input", "stale-checkout"):
            poisoned = json.loads(tuple_path.read_text(encoding="utf-8"))
            if bad == "wrong-sha":
                poisoned["repos"]["runtime"]["sha"] = "0" * 40
            elif bad == "missing-input":
                del poisoned["schema"]
            else:
                poisoned["repos"]["runtime"]["checkout_head"] = "0" * 40
            candidate = root / f"{bad}.json"
            candidate.write_text(json.dumps(poisoned, sort_keys=True) + "\n", encoding="utf-8")
            try:
                MATRIX.load_tuple(candidate, MATRIX.sha256(candidate), check_git=False)
            except ValueError:
                pass
            else:
                raise AssertionError(f"poison {bad} was accepted")
        assert log.read_text(encoding="utf-8") == before
    print("D59 stub controls PASS: positive dispatch count=1; poisoned dispatch count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

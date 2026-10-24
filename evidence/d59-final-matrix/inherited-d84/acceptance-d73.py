#!/usr/bin/env python3
"""Private, no-service D73 route acceptance stub.

It uses private fake request-checkout/request-test commands with the installed
argument shapes. The real dispatcher is never invoked.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).parent
SUBMIT = ROOT / "submit-final.py"
REPOS = ("agent", "runtime", "app", "composition")
WORK = Path("/home/user/work")


def fake_tools(directory: Path) -> tuple[Path, Path]:
    (directory / "done").mkdir(parents=True, exist_ok=True)
    checkout = directory / "request-checkout"
    checkout.write_text(
        """#!/usr/bin/env python3
import os, pathlib, sys
repo, sha, reason = sys.argv[1:]
root = pathlib.Path(os.environ["D73_DONE"])
root.mkdir(parents=True, exist_ok=True)
mode = os.environ.get("D73_MODE", "")
if mode == "drift" and repo == "runtime":
    sha = "0" * 40
home = pathlib.Path("/home/user/work") / repo
(root / f"checkout-{repo}-{sys.argv[2]}").write_text(
    f"created {home} (detached at {sha}, KEEP)\\n"
)
""",
        encoding="utf-8",
    )
    test = directory / "request-test"
    test.write_text(
        """#!/usr/bin/env python3
import os, pathlib, sys
pathlib.Path(os.environ["D73_TEST_LOG"]).write_text(
    "submitted after captured receipts\\n" + " ".join(sys.argv[1:]) + "\\n"
)
""",
        encoding="utf-8",
    )
    checkout.chmod(0o755)
    test.chmod(0o755)
    return checkout, test


def run(mode: str, root: Path) -> subprocess.CompletedProcess[str]:
    done = root / "done"
    checkout, test = fake_tools(root)
    env = {
        **__import__("os").environ,
        "D73_DONE": str(done),
        "D73_MODE": mode,
        "D73_TEST_LOG": str(root / "test.log"),
    }
    return subprocess.run(
        [
            "python3", str(SUBMIT),
            "--work-root", str(WORK),
            "--request-checkout", str(checkout),
            "--request-test", str(test),
            "--done-root", str(done),
            "--tuple", str(root / "tuple.json"),
            "--receipt", str(root / "receipt.json"),
            "--target", "integration:runtime",
            "--suite", "core-v2-final-integration",
            "--no-cache",
            "--checkout-timeout", "2",
        ],
        env=env, text=True, capture_output=True,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="timeline-d73-acceptance-") as raw:
        root = Path(raw)
        good = run("newer-home-midrun", root / "good")
        if good.returncode:
            raise SystemExit(f"good submit failed: {good.stderr}")
        receipt = json.loads((root / "good/receipt.json").read_text())
        events = receipt["events"]
        assert [event["event"] for event in events].count("capture") == 1
        assert [event["event"] for event in events].count("request-checkout") == 4
        assert [event["event"] for event in events].count("checkout-receipt") == 4
        assert events[-2]["event"] == "tuple"
        assert events[-1]["event"] == "request-test"
        assert (root / "good/test.log").is_file(), "request-test was not reached"
        assert events[-1]["argv"][1:] == [
            "integration:runtime", "core-v2-final-integration", "--no-cache",
        ]

        bad = run("drift", root / "bad")
        assert bad.returncode == 2, bad
        assert not (root / "bad/test.log").exists(), "hash drift reached request-test"
    print("D73 private acceptance PASS: one capture, four receipts before request; "
          "newer-home marker accepted; selected-checkout drift refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


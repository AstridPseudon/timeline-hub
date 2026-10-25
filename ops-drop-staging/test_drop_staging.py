#!/usr/bin/env python3
"""Bounded actual-CLI tests for the private drop-staging candidate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
CALLER = ROOT / "drop-staging"


def _manifest(evidence: Path, names: list[str]) -> None:
    rows = []
    for name in names:
        path = evidence / name
        rows.append(
            {
                "path": name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "mode": stat.S_IMODE(path.stat().st_mode),
            }
        )
    (evidence / "manifest.json").write_text(json.dumps({"schema_version": 1, "files": rows}) + "\n")


class DropStagingCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="drop-staging-")
        self.root = Path(self.temp.name)
        self.workers = self.root / "workers"
        self.worker = self.workers / "finished-worker"
        self.worker.mkdir(parents=True)
        (self.worker / "ended").write_text("done\n")
        evidence = self.worker / "evidence"
        evidence.mkdir()
        (evidence / "raw.txt").write_text("raw evidence\n")
        _manifest(evidence, ["raw.txt"])

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(CALLER), "--workers-root", str(self.workers), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def make_staging(self, name: str = "staging") -> Path:
        staging = self.worker / name
        (staging / "nested").mkdir(parents=True, exist_ok=True)
        (staging / "nested" / "frame.txt").write_text("frame\n")
        (staging / "mode.txt").write_text("mode\n")
        os.chmod(staging / "mode.txt", 0o640)
        return staging

    def test_finished_worker_packs_and_preserves_evidence(self) -> None:
        staging = self.make_staging()
        before = (self.worker / "evidence" / "raw.txt").read_bytes()
        result = self.run_cli("finished-worker", "staging")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "packed")
        self.assertFalse(staging.exists())
        archive = self.worker / "staging.tgz"
        self.assertTrue(archive.is_file())
        with tarfile.open(archive, "r:gz") as bundle:
            self.assertEqual(sorted(member.name for member in bundle.getmembers()), ["staging", "staging/mode.txt", "staging/nested", "staging/nested/frame.txt"])
        self.assertEqual((self.worker / "evidence" / "raw.txt").read_bytes(), before)
        self.assertTrue((self.worker / "evidence" / "manifest.json").is_file())
        self.assertTrue((self.worker / "staging-drop.log").is_file())

    def test_low_disk_uses_durable_fallback(self) -> None:
        staging = self.make_staging()
        result = self.run_cli("finished-worker", "staging", "--pack-reserve-bytes", str(1 << 60))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fallback")
        self.assertFalse(staging.exists())
        self.assertFalse((self.worker / "staging.tgz").exists())
        log = (self.worker / "staging-drop.log").read_text()
        self.assertIn('"action":"fallback"', log)
        self.assertIn('"evidence_verified":true', log)
        self.assertIn('"listing_sha256":', log)
        self.assertIn('"original_bytes":', log)

    def test_pack_is_idempotent_and_archive_collision_is_refused(self) -> None:
        staging = self.make_staging()
        first = self.run_cli("finished-worker", "staging")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second = self.run_cli("finished-worker", "staging")
        self.assertEqual(second.returncode, 2, second.stdout + second.stderr)
        self.assertIn("does not exist", second.stdout)
        self.assertFalse(staging.exists())

    def test_preexisting_archive_collision_refuses_before_removal(self) -> None:
        staging = self.make_staging()
        archive = self.worker / "staging.tgz"
        archive.write_bytes(b"reserved\n")
        result = self.run_cli("finished-worker", "staging")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("archive collision", result.stdout)
        self.assertTrue(staging.exists())
        self.assertEqual(archive.read_bytes(), b"reserved\n")

    def test_active_lease_and_symlink_descendant_refuse(self) -> None:
        staging = self.make_staging()
        notes = self.workers.parent / "managers" / "runtime" / "notes"
        notes.mkdir(parents=True)
        lease = notes / "runtime.lease"
        lease.write_text("finished-worker\n")
        result = self.run_cli("finished-worker", "staging")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("active lease", result.stdout)
        self.assertTrue(staging.exists())

        lease.unlink()
        (staging / "escape").symlink_to(self.root, target_is_directory=True)
        result = self.run_cli("finished-worker", "staging")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("symlink inside staging", result.stdout)
        self.assertTrue(staging.exists())

    def test_protected_descendant_refuses(self) -> None:
        staging = self.make_staging()
        (staging / "KEEP").write_text("hold\n")
        result = self.run_cli("finished-worker", "staging")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("protected marker inside staging", result.stdout)
        self.assertTrue(staging.exists())

    def test_refusals_leave_fixture_unchanged(self) -> None:
        cases = [
            ("running", lambda: (self.worker / "running").write_text("1\n"), "running marker"),
            ("not-ended", lambda: (self.worker / "ended").unlink(), "has not ended"),
            ("missing-manifest", lambda: (self.worker / "evidence" / "manifest.json").unlink(), "manifest"),
            ("bad-hash", lambda: (self.worker / "evidence" / "raw.txt").write_text("tampered\n"), "hash mismatch"),
            ("keep", lambda: (self.worker / "KEEP").write_text("hold\n"), "KEEP"),
        ]
        for name, setup, expected in cases:
            with self.subTest(name=name):
                staging = self.make_staging()
                setup()
                before = (staging / "nested" / "frame.txt").read_bytes()
                result = self.run_cli("finished-worker", "staging")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertTrue(staging.exists())
                self.assertEqual((staging / "nested" / "frame.txt").read_bytes(), before)
                # Give each subcase a fresh target and remove only this fixture's
                # own marker so later cases are independent.
                if (self.worker / "running").exists():
                    (self.worker / "running").unlink()
                if (self.worker / "KEEP").exists():
                    (self.worker / "KEEP").unlink()
                if not (self.worker / "ended").exists():
                    (self.worker / "ended").write_text("done\n")
                if not (self.worker / "evidence" / "manifest.json").exists():
                    (self.worker / "evidence" / "raw.txt").write_text("raw evidence\n")
                    _manifest(self.worker / "evidence", ["raw.txt"])
                elif name == "bad-hash":
                    (self.worker / "evidence" / "raw.txt").write_text("raw evidence\n")

    def test_outside_traversal_symlink_and_evidence_overlap_refuse(self) -> None:
        self.make_staging()
        outside = self.root / "outside"
        outside.mkdir()
        cases = [
            (("finished-worker", "../outside"), "traversal"),
            (("../finished-worker", "staging"), "worker"),
            (("finished-worker", "evidence"), "evidence"),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
        symlink = self.worker / "link-staging"
        symlink.symlink_to(outside, target_is_directory=True)
        result = self.run_cli("finished-worker", "link-staging")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("symlink", result.stdout)
        self.assertTrue(outside.exists())


if __name__ == "__main__":
    unittest.main()

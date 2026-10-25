"""Private request-child-venv schema-carrier controls; no real child or Store."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
REQUESTER = ROOT / "request-child-venv"


class RequestSchemaCarrierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="d139a-request-carrier-")
        self.root = Path(self.temporary.name)
        self.orch = self.root / "orch"
        (self.orch / "queue/pending").mkdir(parents=True)
        self.work = self.root / "work"
        self.work.mkdir()
        self.agent = self._checkout("agent", "AGENT = 1\n", "packages/python/agent.py")
        self.runtime = self._checkout(
            "runtime", "CLIENT = 1\n", "packages/python/astrid_runtime_client/__init__.py"
        )
        self.agent_sha = self._head(self.agent)
        self.runtime_sha = self._head(self.runtime)
        self.seed = self.root / "seed"
        self.seed.mkdir()
        self.schema_dist = self.root / "schema.dist-info"
        self.schema_dist.mkdir()
        self.manifest = self.root / "schema-source-manifest.json"
        self.manifest.write_text('{"source_tree":"synthetic"}\n')
        self.manifest_link = self.root / "schema-source-manifest-link.json"
        self.manifest_link.symlink_to(self.manifest)

    def tearDown(self):
        self.temporary.cleanup()

    def _checkout(self, name, content, relative):
        checkout = self.root / name
        checkout.mkdir()
        path = checkout / relative
        path.parent.mkdir(parents=True)
        path.write_text(content)
        subprocess.run(["git", "-C", str(checkout), "init", "-q"], check=True)
        subprocess.run(
            ["git", "-C", str(checkout), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(checkout), "config", "user.name", "D139 test"], check=True
        )
        subprocess.run(["git", "-C", str(checkout), "add", "."], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-qm",
                "synthetic source",
            ],
            check=True,
        )
        return checkout

    @staticmethod
    def _head(checkout):
        return subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
        ).strip()

    def _run(self, *arguments, root=None):
        root = root or self.root
        environment = {
            **os.environ,
            "CHILD_VENV_ORCH_ROOT": str(self.orch),
            "CHILD_VENV_WORK_ROOT": str(self.work),
            "CHILD_VENV_AGENT_CHECKOUT": str(self.agent),
            "CHILD_VENV_RUNTIME_CHECKOUT": str(self.runtime),
        }
        return subprocess.run(
            ["bash", str(REQUESTER), "venv-agent-child-d139-test", self.agent_sha, *arguments],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

    def _queue(self):
        return (self.orch / "queue/pending/childvenv-venv-agent-child-d139-test").read_text()

    def test_canonical_schema_pair_and_sources_are_carried_once(self):
        result = self._run(
            "OPS-proof",
            "remotion",
            "--source-carrier",
            str(self.agent),
            str(self.runtime),
            self.runtime_sha,
            "--dependency-wheelhouse",
            str(self.seed),
            "--schema-installed-distribution",
            str(self.schema_dist),
            "--schema-source-manifest",
            str(self.manifest),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self._queue().split()
        self.assertEqual(row[0], "CHILDVENV")
        self.assertEqual(row.count("--schema-installed-distribution"), 1)
        self.assertEqual(row.count("--schema-source-manifest"), 1)
        self.assertEqual(row.count("--source-carrier"), 1)
        self.assertEqual(row.count("--dependency-wheelhouse"), 1)
        self.assertEqual(row[row.index("--schema-installed-distribution") + 1], str(self.schema_dist))
        self.assertEqual(row[row.index("--schema-source-manifest") + 1], str(self.manifest))
        self.assertEqual(row[row.index("--source-carrier") + 3], self.runtime_sha)

    def test_daemon_word_split_delivers_the_same_arguments_to_maker_stub(self):
        result = self._run(
            "OPS-proof",
            "remotion",
            "--source-carrier",
            str(self.agent),
            str(self.runtime),
            self.runtime_sha,
            "--dependency-wheelhouse",
            str(self.seed),
            "--schema-installed-distribution",
            str(self.schema_dist),
            "--schema-source-manifest",
            str(self.manifest),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        stub = self.root / "maker-stub"
        captured = self.root / "maker-argv"
        stub.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$CAPTURE\"\n")
        stub.chmod(0o755)
        row = self._queue().rstrip("\n")
        forwarded = subprocess.run(
            [
                "bash",
                "-u",
                "-o",
                "pipefail",
                "-c",
                "row=$1; stub=$2; set -- $row; shift; \"$stub\" \"$@\"",
                "dispatcher",
                row,
                str(stub),
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "CAPTURE": str(captured)},
            check=False,
        )
        self.assertEqual(forwarded.returncode, 0, forwarded.stderr)
        delivered = captured.read_text().splitlines()
        expected = row.split()[1:]
        self.assertEqual(delivered, expected)

    def test_malformed_schema_inputs_refuse_without_queue_or_body(self):
        cases = (
            (
                "duplicate-installed",
                (
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
            (
                "duplicate-manifest",
                (
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.manifest),
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
            ("partial-installed", ("--schema-installed-distribution", str(self.schema_dist))),
            ("partial-manifest", ("--schema-source-manifest", str(self.manifest))),
            (
                "empty-installed",
                (
                    "--schema-installed-distribution",
                    "",
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
            (
                "unsafe-distribution",
                (
                    "--schema-installed-distribution",
                    str(self.root / "schema dist"),
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
            (
                "unsafe-manifest",
                (
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.root / "manifest with space.json"),
                ),
            ),
            (
                "symlink-manifest",
                (
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.manifest_link),
                ),
            ),
            (
                "missing-distribution",
                (
                    "--schema-installed-distribution",
                    str(self.root / "missing"),
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
            (
                "missing-manifest",
                (
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.root / "missing.json"),
                ),
            ),
            (
                "conflicting-farm",
                (
                    "--farm-distributions",
                    "--schema-installed-distribution",
                    str(self.schema_dist),
                    "--schema-source-manifest",
                    str(self.manifest),
                ),
            ),
        )
        for name, arguments in cases:
            with self.subTest(name=name):
                queue = self.orch / "queue/pending/childvenv-venv-agent-child-d139-test"
                queue.unlink(missing_ok=True)
                result = self._run(*arguments)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(queue.exists())
                self.assertFalse((self.work / "venv-agent-child-d139-test").exists())

    def test_schema_route_does_not_reuse_legacy_named_bench(self):
        target = self.work / "venv-agent-child-d139-test"
        target.mkdir()
        result = self._run(
            "--schema-installed-distribution",
            str(self.schema_dist),
            "--schema-source-manifest",
            str(self.manifest),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("existing same-name target", result.stderr)
        self.assertFalse(
            (self.orch / "queue/pending/childvenv-venv-agent-child-d139-test").exists()
        )

    def test_legacy_no_schema_queue_shape_is_unchanged(self):
        result = self._run("OPS-proof", "remotion")
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self._queue()
        self.assertNotIn("schema-installed-distribution", row)
        self.assertNotIn("schema-source-manifest", row)
        self.assertEqual(row.count("--source-carrier"), 1)
        self.assertEqual(row.count(self.agent_sha), 1)
        self.assertEqual(row.count(self.runtime_sha), 1)


if __name__ == "__main__":
    unittest.main()

"""Private source controls; no product test, import preflight, or central request."""

from __future__ import annotations

import json
import os
import runpy
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check import (
    AGENT,
    AGENT_PARENTS,
    AGENT_SHA,
    AGENT_TREE,
    FORK,
    ORCH,
    PYTEST,
    REQUIRED,
    RUNTIME,
    RUNTIME_SHA,
    RUNTIME_TREE,
    SELECTED,
    SUITES,
    agent_errors,
    census,
    manifest_errors,
    parse_manifest,
    tuple_errors,
)

HERE = Path(__file__).resolve().parent


class ManifestControls(unittest.TestCase):
    def test_key_value_not_json_preserves_equals_and_final_line(self):
        values = {key: "present" for key in REQUIRED}
        values.update(format="p4-d73-v1", service_versions="a=b,c=d")
        for repo in ("agent", "runtime", "app", "composition"):
            values.update({f"{repo}_sha": "a" * 40, f"{repo}_tree": "b" * 40})
        for key in (
            "profile_lock_sha",
            "profile_archive_sha",
            "profile_registry_sha",
            "original_p4_test_hash",
        ):
            values[key] = "c" * 64
        text = "# actual launcher format\n\n" + "\n".join(
            f"{key}={value}" for key, value in values.items()
        )
        self.assertEqual(parse_manifest(text), (values, []))
        self.assertTrue(parse_manifest(json.dumps(values))[1])

    def test_duplicate_malformed_empty_and_bad_tuple_refused_together(self):
        _, errors = parse_manifest(
            "format=p4-d73-v1\nagent_sha=bad\nagent_sha=other\nnode=\nnot a pair\n"
        )
        for expected in (
            "duplicate agent_sha",
            "malformed key=value",
            "missing node",
            "invalid agent_sha",
            "missing schema",
            "missing app_tree",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_no_manifest_census_lists_every_key_and_receiving_need(self):
        result = census({})
        for key in REQUIRED:
            self.assertIn(f"manifest missing {key}", result["source_errors"])
        self.assertFalse(result["source_ready"])
        self.assertEqual(result["status"], "NOT_READY")
        self.assertEqual(result["body"], "NOTRUN")
        for suite in SUITES:
            self.assertIn(f"central agent {suite}: row not installed", result["receiving_needs"])
        self.assertTrue(any("selected4: fresh" in need for need in result["receiving_needs"]))
        self.assertTrue(any("fork: fresh" in need for need in result["receiving_needs"]))
        self.assertTrue(any("interpreter/schema" in need for need in result["receiving_needs"]))

    def test_missing_many_paths_and_schema_collected_without_running_them(self):
        root = Path(tempfile.mkdtemp(prefix="d73-missing-", dir=os.environ["TMPDIR"]))
        values = {key: str(root / key) for key in ("python", "node", "profile", "schema")}
        errors = manifest_errors(values)
        for key in values:
            self.assertTrue(any(f"manifest {key}: missing absolute input" in e for e in errors))
        self.assertTrue(any("pinned source missing" in e for e in errors))
        self.assertTrue(any("node_modules" in e for e in errors))
        self.assertTrue(any("profile_lock" not in e and "package-lock.json" in e for e in errors))

    def test_wrong_own_node_tuple_is_never_relabelled(self):
        with patch("check.checkout_errors", return_value=[]):
            errors = manifest_errors(
                {"agent_sha": "a4e016b6" + "0" * 32, "runtime_sha": "5e9ad1c6" + "0" * 32}
            )
        self.assertTrue(any("agent_sha" in e for e in errors))
        self.assertTrue(any("runtime_sha" in e for e in errors))


class RunControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        errors = agent_errors()
        if errors:
            raise AssertionError(errors)
        cls.fixture = runpy.run_path(str(AGENT / "tests/sdk/test_p4_d73_pinned_launcher.py"))
        runner = (ORCH / "bin/test-run").read_text().splitlines()
        # Execute the real selection and selector validation, without its queue/snapshot writes.
        start = next(i for i, line in enumerate(runner) if line.startswith("CMD=$(awk"))
        end = next(i for i, line in enumerate(runner[start:], start) if line.startswith("HV="))
        cls.parser = "\n".join(runner[start:end])
        request = (ORCH / "bin/request-test").read_text().splitlines()
        cls.node_guard = next(line for line in request if line.startswith("case $S in *-nodes)"))

    def test_request_node_guard_requires_files(self):
        result = subprocess.run(
            ["bash", "-c", self.node_guard],
            env={"S": SUITES[0], "F": ""},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("need --files", result.stdout)

    def test_real_named_parser_run_positive17_and_poison_zero(self):
        for suite, selectors in zip(SUITES, (SELECTED, FORK), strict=True):
            with self.subTest(suite=suite):
                root = Path(tempfile.mkdtemp(prefix="d73-run-controls-", dir=os.environ["TMPDIR"]))
                self.exercise_route(suite, selectors, root)

    def exercise_route(self, suite, selectors, root):
        # Reuse the authentic reviewed fixture in place; no Agent file is copied or edited.
        agent, runtime, profile, manifest, _, preflight = self.fixture["_make_fixture"](root)
        values, errors = parse_manifest(manifest.read_text())
        self.assertEqual(errors, [])
        # Bind the fixture to the current merged source tuple. The fixture's Git shim remains
        # private and only supplies the reviewed launcher control's existing Git responses.
        values.update(
            agent_sha=AGENT_SHA,
            agent_tree=AGENT_TREE,
            agent_parents=AGENT_PARENTS,
            runtime_sha=RUNTIME_SHA,
            runtime_tree=RUNTIME_TREE,
            runtime_path=str(RUNTIME),
        )
        manifest.write_text("".join(f"{key}={value}\n" for key, value in values.items()))
        fake_git = root / "git"
        git_source = fake_git.read_text()
        for old, new in (
            (repr(str(runtime)), repr(str(RUNTIME))),
            (repr("c" * 40), repr(RUNTIME_SHA)),
            (repr("d" * 40), repr(RUNTIME_TREE)),
            (repr("a" * 40 + " " + "3" * 40 + " " + "4" * 40), repr(AGENT_PARENTS)),
            (repr("a" * 40), repr(AGENT_SHA)),
            (repr("b" * 40), repr(AGENT_TREE)),
        ):
            git_source = git_source.replace(old, new)
        fake_git.write_text(git_source)
        values, errors = parse_manifest(manifest.read_text())
        self.assertEqual(errors, [])
        self.assertEqual(tuple_errors(values), [])
        stub = root / "python"
        marker = root / "body-calls.jsonl"
        runtime = Path(values["runtime_path"])
        expected_env = {
            "PYTHONPATH": f"{agent}:{runtime}",
            "ASTRID_RUNTIME_CHECKOUT": str(runtime),
            "ASTRID_RUNTIME_SOURCE_ROOT": str(runtime),
            "ASTRID_REMOTION_PROJECT_DIR": str(profile),
            "ASTRID_NODE_EXECUTABLE": values["node"],
            "ASTRID_TEST_NODE_MODULES": f"{profile}/node_modules",
        }
        stub.write_text(
            "#!/usr/bin/python3\nimport json, os, sys\nfrom pathlib import Path\n"
            "if sys.argv[1:3] == ['-P', '-']:\n"
            f"    with open({str(preflight)!r}, 'a') as f: f.write(repr(os.environ.get('PYTHONNOUSERSITE')) + '\\n')\n"
            f"    if len(sys.argv) == 4: print({str(root / 'composition.tgz')!r})\n"
            "    raise SystemExit(0)\n"
            f"assert sys.argv[1:12] == {['-P', *PYTEST]!r}, sys.argv\n"
            f"assert all(os.environ.get(k) == v for k, v in {expected_env!r}.items())\n"
            "assert 'PYTHONNOUSERSITE' not in os.environ\n"
            f"assert Path.cwd() == Path({str(agent)!r})\n"
            "assert sys.argv[12].startswith('--junitxml=')\n"
            f"assert tuple(sys.argv[13:]) in ({SELECTED!r}, {FORK!r})\n"
            f"with open({str(marker)!r}, 'a') as f: f.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "Path(sys.argv[12].split('=', 1)[1]).write_text('<testsuite name=\"bounded-stub\" tests=\"0\"/>')\n"
            "raise SystemExit(17)\n"
        )
        # Only the pre-existing private fixture interpreter is replaced, never a shared install.
        stub.chmod(0o700)
        private_orch = root / "parser-input"
        (private_orch / "tests").mkdir(parents=True)
        # PATH is the sole control substitution beyond receipt placeholders: inject fixture git.
        rows = (
            (HERE / "suites.conf")
            .read_text()
            .replace("__P4_D73_AGENT_PATH__", shlex.quote(str(agent)))
            .replace("__P4_D73_MANIFEST__", shlex.quote(str(manifest)))
            .replace("__P4_D73_GUARD__", shlex.quote(str(HERE)))
            .replace("PATH=/usr/bin:/bin", f"PATH={shlex.quote(str(root) + ':/usr/bin:/bin')}")
        )
        (private_orch / "tests/suites.conf").write_text(rows)
        output = root / suite / "d66"
        env = {
            **os.environ,
            "O": str(private_orch),
            "repo": "agent",
            "suite": suite,
            "files": " ".join(selectors),
            "D66_OUTPUT_DIR": str(output),
        }
        parsed = subprocess.run(
            [
                "bash",
                "-c",
                'bad() { echo "$*" >&2; exit 1; };\n' + self.parser + '\nprintf "%s" "$CMD"',
            ],
            env=env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        subprocess.run(["bash", "-n", "-c", parsed], check=True)
        result = subprocess.run(
            ["bash", "-c", parsed], env=env, capture_output=True, text=True, check=False
        )
        (root / "positive.stdout").write_text(result.stdout)
        (root / "positive.stderr").write_text(result.stderr)
        self.assertEqual(result.returncode, 17, result.stdout + result.stderr)
        self.assertEqual(len(marker.read_text().splitlines()), 1)
        self.assertEqual(
            json.loads(marker.read_text()),
            ["-P", *PYTEST, f"--junitxml={output}/{suite}.xml", *selectors],
        )
        self.assertEqual((output / f"{suite}.body.exit").read_text(), "17\n")
        self.assertEqual((output / f"{suite}.preflight.exit").read_text(), "0\n")
        self.assertEqual((output / f"{suite}.request-id").read_text(), suite + "\n")
        self.assertEqual((output / f"{suite}.manifest").read_text(), manifest.read_text())
        for suffix in ("runmanifest", "command", "preflight.log", "body.log", "xml"):
            self.assertTrue((output / f"{suite}.{suffix}").is_file(), suffix)
        self.assertEqual(preflight.read_text().splitlines(), ["None", "None"])
        positive = manifest.read_text()
        # Every invalid manifest is rejected by the production row before the supported
        # launcher is invoked; no evidence directory is created by pre-admission.
        calls_before = len(marker.read_text().splitlines())
        preflight_before = preflight.read_text().splitlines()
        for label, invalid in (
            ("wrong-source", positive.replace(f"agent_path={values['agent_path']}", f"agent_path={root / 'foreign-agent'}")),
            ("wrong-lock", positive.replace(f"runtime_sha={values['runtime_sha']}", "runtime_sha=" + "0" * 40)),
            ("poison", positive.replace(f"agent_sha={values['agent_sha']}", "agent_sha=" + "0" * 40)),
            ("duplicate", positive + "format=p4-d73-v1\n"),
            ("malformed", positive + "not-a-key-value-line\n"),
        ):
            manifest.write_text(invalid)
            invalid_output = root / (suite + "-" + label) / "d66"
            refused = subprocess.run(
                ["bash", "-c", parsed],
                env={**env, "D66_OUTPUT_DIR": str(invalid_output)},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(refused.returncode, 0, label)
            self.assertIn("D73 pre-admission:", refused.stderr, label)
            self.assertEqual(len(marker.read_text().splitlines()), calls_before, label)
            self.assertEqual(preflight.read_text().splitlines(), preflight_before, label)
            self.assertFalse(invalid_output.exists(), label)
        manifest.write_text(positive)
        print(f"{suite}: run positive exit=17 calls=1; five pre-admission refusals calls=0")


if __name__ == "__main__":
    unittest.main(verbosity=2)

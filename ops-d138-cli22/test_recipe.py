"""Private D138 controls; no collection, import preflight, or central request."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from check import (
    AGENT,
    AGENT_PARENTS,
    AGENT_SHA,
    AGENT_TREE,
    APP,
    APP_PARENTS,
    APP_SHA,
    APP_TREE,
    COMPOSITION,
    COMPOSITION_PARENTS,
    COMPOSITION_SHA,
    COMPOSITION_TREE,
    LAUNCHER,
    LAUNCHER_SHA,
    LOCK,
    LOCK_RUNTIME_SHA,
    LOCK_RUNTIME_TREE,
    LOCK_SHA,
    ORCH,
    RETIRED_SENTINEL,
    RUNTIME_HELPER,
    RUNTIME_HELPER_SHA,
    RUNTIME,
    RUNTIME_PARENTS,
    RUNTIME_SHA,
    RUNTIME_TREE,
    SCHEMA_DIGEST,
    SELECTORS,
    SUITE,
    TEST_SOURCE,
    TEST_SOURCE_SHA,
    SYNC_SOURCE,
    SYNC_SOURCE_SHA,
    artifact_paths,
    manifest_errors,
    parse_manifest,
    suite_command,
)


def write_executable(path: Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")
    path.chmod(0o700)


def fixture_manifest(root: Path) -> tuple[Path, Path, Path, Path, dict[str, str]]:
    runtime = root / "runtime"
    app = root / "app"
    composition = root / "composition"
    for path in (runtime, app, composition):
        path.mkdir()
    profile = root / "profile"
    (profile / "node_modules").mkdir(parents=True)
    (profile / "package-lock.json").write_text("{}\n", encoding="utf-8")
    (profile / ".astrid-registry-state.json").write_text("{}\n", encoding="utf-8")
    archive = root / "composition.tgz"
    archive.write_bytes(b"private composition fixture\n")
    (profile / "package.json").write_text(
        json.dumps({"dependencies": {"@banodoco/timeline-composition": "file:../composition.tgz"}}),
        encoding="utf-8",
    )
    schema = root / "schema"
    schema.mkdir()
    marker = root / "body-calls"
    preflight = root / "preflight-calls"
    fake_git = root / "git"
    mapping = {
        str(AGENT): (AGENT_SHA, AGENT_TREE, AGENT_PARENTS),
        str(runtime): (RUNTIME_SHA, "d" * 40, ""),
        str(app): (APP_SHA, APP_TREE, ""),
        str(composition): (COMPOSITION_SHA, COMPOSITION_TREE, ""),
    }
    write_executable(
        fake_git,
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"mapping = {mapping!r}\n"
        "if sys.argv[1] != '-C': raise SystemExit(2)\n"
        "path, command = sys.argv[2], sys.argv[3:]\n"
        "sha, tree, parents = mapping[path]\n"
        "if command == ['rev-parse', 'HEAD']: print(sha)\n"
        "elif command == ['rev-parse', 'HEAD^{tree}']: print(tree)\n"
        "elif command == ['rev-list', '--parents', '-n', '1', 'HEAD']: print(parents)\n"
        "elif command == ['status', '--porcelain', '--untracked-files=all']: pass\n"
        "else: raise SystemExit(3)\n",
    )
    fake_python = root / "python"
    write_executable(
        fake_python,
        "#!/usr/bin/python3\nimport json, os, sys\n"
        f"preflight = {str(preflight)!r}\nmarker = {str(marker)!r}\n"
        "if sys.argv[1:3] == ['-P', '-']:\n"
        f"    open(preflight, 'a', encoding='utf-8').write(repr(os.environ.get('PYTHONNOUSERSITE')) + '\\n')\n"
        f"    if len(sys.argv) == 4: print({str(archive)!r})\n"
        "    raise SystemExit(0)\n"
        "open(marker, 'a', encoding='utf-8').write(json.dumps(sys.argv[1:]) + '\\n')\n"
        "raise SystemExit(17)\n",
    )
    fake_node = root / "node"
    write_executable(fake_node, "#!/bin/sh\nprintf '%s\\n' v20.19.4\n")
    original_hash = hashlib.sha256(
        subprocess.check_output(
            [
                "sha256sum",
                str(AGENT / "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py"),
                str(AGENT / "tests/editing_conformance/test_p4_ten_note_v2_runtime.py"),
                str(AGENT / "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py"),
            ]
        )
    ).hexdigest()
    values = {
        "format": "p4-d73-v1",
        "agent_sha": AGENT_SHA,
        "agent_tree": AGENT_TREE,
        "agent_parents": AGENT_PARENTS,
        "agent_path": str(AGENT),
        "runtime_sha": RUNTIME_SHA,
        "runtime_tree": "d" * 40,
        "runtime_path": str(runtime),
        "app_sha": APP_SHA,
        "app_tree": APP_TREE,
        "app_path": str(app),
        "composition_sha": COMPOSITION_SHA,
        "composition_tree": COMPOSITION_TREE,
        "composition_path": str(composition),
        "python": str(fake_python),
        "node": str(fake_node),
        "profile": str(profile),
        "schema": str(schema),
        "node_version": "v20.19.4",
        "profile_lock_sha": hashlib.sha256((profile / "package-lock.json").read_bytes()).hexdigest(),
        "profile_archive_sha": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "profile_registry_sha": hashlib.sha256((profile / ".astrid-registry-state.json").read_bytes()).hexdigest(),
        "composition_version": "0.0.14",
        "original_p4_test_hash": original_hash,
        "service_versions": "private-control",
        "junit_paths": str(root / "junit.xml"),
    }
    manifest = root / "manifest"
    manifest.write_text("\n".join(f"{key}={value}" for key, value in values.items()) + "\n", encoding="utf-8")
    return manifest, runtime, profile, marker, {"PATH": f"{root}:/usr/bin:/bin", "preflight": str(preflight)}


class SourceControls(unittest.TestCase):
    def test_exact22_conservation_and_integration_marker(self):
        self.assertEqual(len(SELECTORS), 22)
        self.assertEqual(len(set(SELECTORS)), 22)
        self.assertNotIn(RETIRED_SENTINEL, SELECTORS)
        source = ast.parse(TEST_SOURCE.read_text(encoding="utf-8"))
        self.assertTrue(any(
            isinstance(node, ast.Assign)
            and any(getattr(target, "id", None) == "pytestmark" for target in node.targets)
            and ast.unparse(node.value) == "pytest.mark.integration"
            for node in source.body
        ))
        names = {node.name for node in ast.walk(source) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        self.assertTrue({item.split("::", 1)[1].split("[", 1)[0] for item in SELECTORS} <= names)
        self.assertIn(RETIRED_SENTINEL.split("::", 1)[1], names)

    def test_runtime_adapter_cannot_mix_lock_and_manifest_sources(self):
        self.assertEqual(hashlib.sha256(RUNTIME_HELPER.read_bytes()).hexdigest(), RUNTIME_HELPER_SHA)
        self.assertEqual(hashlib.sha256(SYNC_SOURCE.read_bytes()).hexdigest(), SYNC_SOURCE_SHA)
        self.assertNotEqual(LOCK_RUNTIME_SHA, RUNTIME_SHA)
        candidate_lock = json.loads(subprocess.check_output(
            ["git", "-C", str(AGENT), "show", f"{AGENT_SHA}:runtime.lock.json"],
            text=True,
        ))
        candidate_test = subprocess.check_output(
            ["git", "-C", str(AGENT), "show", f"{AGENT_SHA}:tests/editing_conformance/test_native_batch_ingress.py"],
            text=True,
        )
        self.assertEqual(candidate_lock["source_commit"], LOCK_RUNTIME_SHA)
        self.assertIn("use_runtime(vendored_runtime_commit())", candidate_test)

    def test_named_row_uses_existing_parser_and_exact_argv(self):
        command = suite_command()
        self.assertIn("p4-d73-pinned-launch.sh", command)
        self.assertIn("-m integration", command)
        self.assertIn("-p no:cacheprovider", command)
        self.assertIn("--timeout=180", command)
        self.assertIn("--junitxml=", command)
        self.assertTrue(all(command.count(selector) == 1 for selector in SELECTORS))
        self.assertNotIn(RETIRED_SENTINEL, command)
        self.assertEqual(command.count("test_native_batch_ingress.py::"), 22)

    def test_central_test_run_parser_appends_all_files(self):
        runner = (ORCH / "bin/test-run").read_text(encoding="utf-8").splitlines()
        start = next(index for index, line in enumerate(runner) if line.startswith("CMD=$(awk"))
        end = next(index for index, line in enumerate(runner[start:], start) if line.startswith("HV="))
        parser = "\n".join(runner[start:end])
        with tempfile.TemporaryDirectory(prefix="d138-parser-", dir=os.environ["TMPDIR"]) as raw:
            root = Path(raw)
            (root / "tests").mkdir()
            (root / "tests/suites.conf").write_text(
                f"agent {SUITE} {suite_command()}\n", encoding="utf-8"
            )
            result = subprocess.run(
                ["bash", "-c", "bad() { echo \"$*\" >&2; exit 1; }; " + parser + '; printf "%s" "$CMD"'],
                env={
                    "O": str(root),
                    "repo": "agent",
                    "suite": SUITE,
                    "files": " ".join(SELECTORS),
                    "D66_OUTPUT_DIR": str(root / "central-id" / "d66"),
                },
                capture_output=True,
                text=True,
                check=True,
            )
        self.assertEqual(result.stdout.count("test_native_batch_ingress.py::"), 44)
        self.assertTrue(all(result.stdout.count(selector) == 2 for selector in SELECTORS))
        self.assertIn("-m integration", result.stdout)
        self.assertIn("-p no:cacheprovider", result.stdout)
        self.assertNotIn(RETIRED_SENTINEL, result.stdout)

    def test_manifest_is_first_equals_key_value_and_rejects_json(self):
        values = {key: "value" for key in ("format", *SELECTORS[:0])}
        text = "# launcher format\nservice_versions=a=b,c=d\nformat=p4-d73-v1\n"
        parsed, errors = parse_manifest(text)
        self.assertEqual(parsed["service_versions"], "a=b,c=d")
        self.assertTrue(any("missing agent_sha" in error for error in errors))
        self.assertTrue(parse_manifest(json.dumps(values))[1])
        _, duplicate_errors = parse_manifest("agent_sha=one\nagent_sha=two\nnot-a-key\n")
        self.assertTrue(any("duplicate agent_sha" in error for error in duplicate_errors))
        self.assertTrue(any("malformed key=value" in error for error in duplicate_errors))

    def test_manifest_rejects_current_source_mismatch(self):
        values = {key: "present" for key in __import__("check").REQUIRED}
        values.update(
            route="d138-cli22",
            agent_path=str(AGENT),
            agent_sha="0" * 40,
            agent_tree=AGENT_TREE,
            agent_parents=AGENT_PARENTS,
            runtime_path=str(RUNTIME),
            runtime_sha=RUNTIME_SHA,
            runtime_tree=RUNTIME_TREE,
            runtime_parents=RUNTIME_PARENTS,
            lock_runtime_sha=LOCK_RUNTIME_SHA,
            lock_runtime_tree=LOCK_RUNTIME_TREE,
            lock_path=str(LOCK),
            app_path=str(APP), app_sha=APP_SHA, app_tree=APP_TREE, app_parents=APP_PARENTS,
            composition_path=str(COMPOSITION), composition_sha=COMPOSITION_SHA,
            composition_tree=COMPOSITION_TREE, composition_parents=COMPOSITION_PARENTS,
            client_version="0.2.14", schema_digest=SCHEMA_DIGEST,
            launcher_sha256=LAUNCHER_SHA, test_source_sha256=TEST_SOURCE_SHA, lock_sha256=LOCK_SHA,
        )
        self.assertTrue(any("agent_sha" in error for error in manifest_errors(values)))

    def test_lock_is_preserved_and_normal_runtime_is_distinct(self):
        lock_bytes = subprocess.check_output(
            ["git", "-C", str(AGENT), "show", f"{AGENT_SHA}:runtime.lock.json"]
        )
        lock = json.loads(lock_bytes)
        self.assertEqual(lock["source_commit"], LOCK_RUNTIME_SHA)
        self.assertNotEqual(lock["source_commit"], RUNTIME_SHA)
        self.assertEqual(hashlib.sha256(lock_bytes).hexdigest(), LOCK_SHA)
        self.assertEqual(hashlib.sha256(LAUNCHER.read_bytes()).hexdigest(), LAUNCHER_SHA)
        self.assertEqual(hashlib.sha256(TEST_SOURCE.read_bytes()).hexdigest(), TEST_SOURCE_SHA)

    def test_per_id_artifacts_are_disjoint(self):
        with tempfile.TemporaryDirectory(prefix="d138-artifacts-", dir=os.environ["TMPDIR"]) as raw:
            root = Path(raw)
            first = artifact_paths(root / "first" / "d66")
            second = artifact_paths(root / "second" / "d66")
            self.assertTrue(set(first.values()).isdisjoint(second.values()))
            self.assertNotEqual(first["xml"], second["xml"])

    def test_launcher_run_mode_positive_and_poison_zero_call(self):
        with tempfile.TemporaryDirectory(prefix="d138-launcher-", dir=os.environ["TMPDIR"]) as raw:
            root = Path(raw)
            manifest, runtime, profile, marker, extra = fixture_manifest(root)
            environment = {
                **os.environ,
                **extra,
                "HOME": str(root / "home"),
                "P4_D73_EVIDENCE": str(root / "positive" / "d66"),
                "P4_D73_REQUEST_ID": "positive",
            }
            positive = subprocess.run(
                [str(LAUNCHER), str(manifest), "run", "--", "-m", "pytest",
                 "value with spaces", "semi;colon", "quote'and\"double"],
                cwd=AGENT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(positive.returncode, 17, positive.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8").splitlines(), [
                '["-P", "-m", "pytest", "value with spaces", "semi;colon", "quote\'and\\\"double"]'
            ])
            self.assertEqual((root / "positive" / "d66" / "positive.preflight.exit").read_text().strip(), "0")
            self.assertEqual((root / "positive" / "d66" / "positive.body.exit").read_text().strip(), "17")
            duplicate = root / "duplicate-manifest"
            duplicate.write_text(manifest.read_text() + f"agent_sha={AGENT_SHA}\n", encoding="utf-8")
            duplicate_result = subprocess.run(
                [str(LAUNCHER), str(duplicate), "run", "--", "-m", "pytest"],
                cwd=AGENT,
                env={**environment, "P4_D73_EVIDENCE": str(root / "duplicate" / "d66"), "P4_D73_REQUEST_ID": "duplicate"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(duplicate_result.returncode, 17, duplicate_result.stderr)
            self.assertEqual(len(marker.read_text(encoding="utf-8").splitlines()), 2)
            malformed = root / "malformed-manifest"
            malformed.write_text(manifest.read_text() + "not-a-manifest-line\n", encoding="utf-8")
            malformed_result = subprocess.run(
                [str(LAUNCHER), str(malformed), "run", "--", "-m", "pytest"],
                cwd=AGENT,
                env={**environment, "P4_D73_EVIDENCE": str(root / "malformed" / "d66"), "P4_D73_REQUEST_ID": "malformed"},
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(malformed_result.returncode, 0)
            self.assertIn("malformed manifest line", malformed_result.stderr)
            self.assertEqual(len(marker.read_text(encoding="utf-8").splitlines()), 2)
            poisoned = root / "poisoned-manifest"
            poisoned.write_text(manifest.read_text().replace(f"runtime_sha={RUNTIME_SHA}", "runtime_sha=" + "0" * 40), encoding="utf-8")
            poison = subprocess.run(
                [str(LAUNCHER), str(poisoned), "run", "--", "-m", "pytest"],
                cwd=AGENT,
                env={**environment, "P4_D73_EVIDENCE": str(root / "poison" / "d66"), "P4_D73_REQUEST_ID": "poison"},
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(poison.returncode, 0)
            self.assertIn("SHA mismatch", poison.stderr)
            self.assertEqual(len(marker.read_text(encoding="utf-8").splitlines()), 2)
            self.assertFalse((root / "poison" / "d66" / "poison.body.exit").exists())

    def test_launcher_seam_is_explicit_not_bypassed(self):
        source = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("lock['source_commit'] == runtime_sha.name", source)
        self.assertIn("runtime_sha", source)
        self.assertNotEqual(LOCK_RUNTIME_SHA, RUNTIME_SHA)


if __name__ == "__main__":
    unittest.main(verbosity=2)

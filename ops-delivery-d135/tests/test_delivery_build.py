"""D135 source/unit controls; no Git fixture or production package run is performed here."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).parents[1] / "delivery-build"
LOADER = SourceFileLoader("delivery_build_d135", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC and SPEC.loader
delivery_build = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = delivery_build
SPEC.loader.exec_module(delivery_build)


REPOS = tuple(delivery_build.ALL_REPOS)


def tuple_value(root="/tmp/source"):
    return {
        name: {"root": f"{root}/{name}", "sha": f"{index:040x}", "tree": f"{index + 10:040x}"}
        for index, name in enumerate(REPOS, 1)
    }


class TupleControls(unittest.TestCase):
    def write_tuple(self, value):
        source_root = tempfile.TemporaryDirectory(prefix="d135-source-")
        self.addCleanup(source_root.cleanup)
        for name in REPOS:
            (Path(source_root.name) / name).mkdir()
        value = {
            name: {**item, "root": str(Path(source_root.name) / name)}
            for name, item in value.items()
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
            path = Path(handle.name)
            self.addCleanup(lambda: path.unlink(missing_ok=True))
            json.dump(value, handle)
        return str(path)

    def test_tuple_requires_exact_four_entries_and_exact_identity_fields(self):
        path = self.write_tuple(tuple_value())
        raw, digest, parsed = delivery_build.source_tuple(path)
        self.assertEqual(set(json.loads(raw)), set(REPOS))
        self.assertEqual(len(digest), 64)
        self.assertEqual(parsed["agent"]["sha"], "1".zfill(40))

        malformed = tuple_value()
        malformed["agent"]["proof_pin"] = "not accepted"
        with self.assertRaisesRegex(delivery_build.Refused, "exactly root, sha, tree"):
            delivery_build.source_tuple(self.write_tuple(malformed))

    def test_tuple_digest_is_checked_when_caller_supplies_it(self):
        path = self.write_tuple(tuple_value())
        with self.assertRaisesRegex(delivery_build.Refused, "source tuple SHA mismatch"):
            delivery_build.source_tuple(path, "0" * 64)


class AncestryControls(unittest.TestCase):
    def test_failed_ancestry_reports_repo_base_and_tip(self):
        completed = subprocess.CompletedProcess(
            ["git"], 1, stdout="", stderr="not an ancestor\n"
        )
        with mock.patch.object(delivery_build.subprocess, "run", return_value=completed), self.assertRaisesRegex(
            delivery_build.Refused,
            r"ancestry refused for agent: repo=/private/agent "
            r"base=base-sha tip=tip-sha: not an ancestor",
        ):
            delivery_build.ancestry("/private/agent", "base-sha", "tip-sha", "agent")

    def test_all_preflight_checks_later_repo_before_returning_failure(self):
        calls = []

        def check(name, item):
            calls.append(name)
            if name == "app":
                raise delivery_build.Refused(
                    "ancestry refused for app: repo=/private/app base=base tip=tip"
                )
            return {"name": name, "repo": item["root"], "base": "base", "tip": item["sha"]}

        with mock.patch.object(delivery_build, "preflight_source", side_effect=check), self.assertRaisesRegex(
            delivery_build.Refused, "ancestry refused for app"
        ):
            delivery_build.preflight_all(tuple_value(), REPOS)
        self.assertEqual(calls, list(REPOS))


class MainBoundaryControls(unittest.TestCase):
    def test_missing_tuple_refuses_before_delivery_root_creation(self):
        with tempfile.TemporaryDirectory() as folder:
            delivery = Path(folder) / "delivery"
            argv = [str(SCRIPT), "--delivery-root", str(delivery)]
            with mock.patch.object(sys, "argv", argv), self.assertRaises(SystemExit) as raised:
                delivery_build.main()
            self.assertEqual(raised.exception.code, 2)
            self.assertFalse(delivery.exists())

    def test_ancestry_refusal_happens_before_any_staging_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            delivery = root / "delivery"
            work = root / "work"
            template = root / "README.template.md"
            template.write_text("{{REPO_SUMMARY}}\n{{REPO_SECTIONS}}\n{{GATE_RESULTS}}\n")
            source_tuple = root / "source.json"
            source_tuple.write_text(json.dumps(tuple_value()))
            argv = [
                str(SCRIPT), "--source-tuple", str(source_tuple),
                "--delivery-root", str(delivery), "--work-root", str(work),
                "--template", str(template), "--repos", "agent runtime",
            ]
            with mock.patch.object(
                delivery_build, "source_tuple", return_value=(b"{}", "a" * 64, tuple_value())
            ), mock.patch.object(
                delivery_build, "preflight_all",
                side_effect=delivery_build.Refused(
                    "all-repository preflight refused:\n"
                    "ancestry refused for runtime: repo=/private/runtime base=base tip=tip"
                ),
            ), mock.patch.object(sys, "argv", argv), self.assertRaises(SystemExit) as raised:
                delivery_build.main()
            self.assertEqual(raised.exception.code, 2)
            self.assertFalse(delivery.exists())
            self.assertFalse(work.exists())


class BuildRepoControls(unittest.TestCase):
    def test_build_repo_binds_the_resolved_tuple_tip(self):
        resolved = {
            "name": "agent",
            "repo": "/private/agent-home",
            "base": "b" * 40,
            "tip": "a" * 40,
        }
        calls = []

        def fake_git(repo, *args):
            calls.append((repo, args))
            if args[:2] == ("rev-list", "--count"):
                return "0"
            if args[:1] == ("diff",):
                return ""
            if args[:1] == ("rev-parse",):
                return resolved["base"]
            return ""

        with tempfile.TemporaryDirectory() as folder, \
                mock.patch.object(delivery_build, "private_source_view", return_value="/private/view") as view, \
                mock.patch.object(delivery_build, "git", side_effect=fake_git), \
                mock.patch.object(delivery_build, "squash"), \
                mock.patch.object(delivery_build, "verify", return_value={
                    "status": "PASS", "want_tree": "t", "applied_tree": "t",
                    "bundle_tree": "t", "bundle_tip": resolved["tip"], "applied": 1,
                }):
            result = delivery_build.build_repo(resolved, folder, folder)

        view.assert_called_once_with("agent", resolved["repo"], resolved["base"], resolved["tip"], folder)
        self.assertEqual(result["tip"], resolved["tip"])
        bundle_calls = [args for repo, args in calls if args[:2] == ("bundle", "create")]
        self.assertEqual(bundle_calls, [("bundle", "create", mock.ANY,
                                         delivery_build.BRANCH, "^" + resolved["base"])])


if __name__ == "__main__":
    unittest.main(verbosity=2)

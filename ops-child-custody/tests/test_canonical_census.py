"""Canonical packet controls; system probes are supporting evidence only."""

import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from support import ORCH


CHECKER = Path(__file__).resolve().parents[1] / "check-child-imports"
CANONICAL = ORCH / "design/agt-F-D139-import-input-census-2149-input-census.json"
LAUNCHER = Path("/home/user/work/agent/tools/p4-d73-pinned-launch.sh")


class CanonicalCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namespace = {"__name__": "canonical_checker"}
        exec(compile(CHECKER.read_text(), str(CHECKER), "exec"), cls.namespace)
        cls.raw = CANONICAL.read_bytes()
        cls.packet = json.loads(cls.raw)

    def test_exact_packet_membership_metadata_and_classifications(self):
        rows, provenance = self.namespace["_external_census"](CANONICAL)
        self.assertEqual(len(rows), 1146)
        self.assertEqual(provenance["sha256"],
                         "be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30")
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), provenance["sha256"])
        self.assertEqual(provenance["metadata"],
                         {k: v for k, v in self.packet.items() if k != "imports"})
        for original, adapted in zip(self.packet["imports"], rows, strict=True):
            self.assertEqual({key: adapted[key] for key in original}, original)
            self.assertEqual(adapted["name"], original["module"])
            self.assertEqual(adapted["classification"], original["category"])
            self.assertEqual(adapted["applicable"], original["category"] == "unconditional_required")
        self.assertEqual(collections.Counter(row["classification"] for row in rows), {
            "internal_source_carrier": 990, "stdlib": 108, "optional_manual": 17,
            "missing": 12, "unconditional_required": 10, "tested_conditional": 9,
        })
        self.assertEqual(sum(row["probe_policy"] == "required" for row in rows), 10)
        self.assertEqual(sum(row["probe_policy"] == "diagnostic_missing" for row in rows), 12)

    def test_malformed_rows_missing_fields_and_incomplete_membership_refuse(self):
        for key in self.packet["imports"][0]:
            packet = copy.deepcopy(self.packet)
            del packet["imports"][0][key]
            with self.subTest(missing=key), self.assertRaisesRegex(ValueError, "malformed"):
                self.namespace["_canonical_census"](packet, self.raw)
        for bad in (None, "module", {}, {"module": []}):
            packet = copy.deepcopy(self.packet)
            packet["imports"][0] = bad
            with self.subTest(row=bad), self.assertRaisesRegex(ValueError, "malformed"):
                self.namespace["_canonical_census"](packet, self.raw)
        packet = copy.deepcopy(self.packet)
        packet["imports"].pop()
        with self.assertRaisesRegex(ValueError, "1146"):
            self.namespace["_canonical_census"](packet, self.raw)

    def test_tampered_tuple_schema_rows_and_provenance_refuse_before_probe(self):
        with tempfile.TemporaryDirectory(prefix="d139-canonical-", dir=os.environ["TMPDIR"]) as temp:
            path = Path(temp) / "census.json"
            for key in ("agent_commit", "runtime_commit", "schema", "summary", "imports"):
                for missing in (False, True):
                    packet = copy.deepcopy(self.packet)
                    if missing:
                        del packet[key]
                    elif key == "imports":
                        packet[key][0]["source_owner"] = "foreign"
                    else:
                        packet[key] = "foreign"
                    path.write_text(json.dumps(packet))
                    probe = Mock(side_effect=AssertionError("must refuse before probe"))
                    with self.subTest(key=key, missing=missing), patch.dict(self.namespace, {"_probe": probe}):
                        with patch("sys.argv", [str(CHECKER), "--child", "/usr/bin/python3.13",
                                                "--launcher", str(LAUNCHER), "--census-file", str(path)]):
                            with self.assertRaises(SystemExit) as error:
                                self.namespace["main"]()
                            self.assertEqual(error.exception.code, 2)
                    probe.assert_not_called()
            path.write_text('{"imports":')
            with self.assertRaises(ValueError):
                self.namespace["_external_census"](path)
            path.write_bytes(self.raw + b"\n")
            with self.assertRaisesRegex(ValueError, "provenance hash"):
                self.namespace["_external_census"](path)

    def test_all_missing_probe_keeps_missing_separate_from_installed_requirements(self):
        def missing(child, names):
            return {"child_returncode": 0, "results": [
                {"name": name, "ok": False, "error": "supporting synthetic absence"}
                for name in names]}

        with tempfile.TemporaryDirectory(prefix="d139-all-missing-", dir=os.environ["TMPDIR"]) as temp:
            output = Path(temp) / "result.json"
            argv = [str(CHECKER), "--child", "/usr/bin/python3.13", "--launcher", str(LAUNCHER),
                    "--census-file", str(CANONICAL), "--output", str(output)]
            with patch.dict(self.namespace, {"_probe": missing}), patch("sys.argv", argv):
                with patch("builtins.print"):
                    self.assertEqual(self.namespace["main"](), 1)
            report = json.loads(output.read_bytes())
        expected = {row["module"] for row in self.packet["imports"]
                    if row["category"] in {"unconditional_required", "missing"}}
        self.assertEqual(set(report["attempted_modules"]), expected)
        self.assertEqual(len(expected), 22)
        self.assertEqual(len(report["missing_installed_distributions"]), 10)
        self.assertEqual(len(report["missing_census_modules"]), 12)
        self.assertEqual(len(report["failures"]), 22)
        for row in report["census"]:
            self.assertEqual("probe" in row, row["category"] in {"unconditional_required", "missing"})

    def test_exact_canonical_cli_with_system_interpreter_is_supporting_only(self):
        with tempfile.TemporaryDirectory(prefix="d139-canonical-cli-", dir=os.environ["TMPDIR"]) as temp:
            output = Path(temp) / "result.json"
            result = subprocess.run(
                ["python3", str(CHECKER), "--child", "/usr/bin/python3.13", "--launcher", str(LAUNCHER),
                 "--census-file", str(CANONICAL), "--output", str(output)],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(output.read_bytes())
        self.assertEqual(len(report["census"]), 1146)
        self.assertEqual(len(report["attempted_modules"]), 22)
        self.assertTrue(report["missing_census_modules"])
        self.assertEqual(report["census_provenance"]["sha256"], self.namespace["CANONICAL_SHA256"])

    def test_unverified_legacy_rows_cannot_select_canonical_probe_policy(self):
        with tempfile.TemporaryDirectory(prefix="d139-legacy-", dir=os.environ["TMPDIR"]) as temp:
            path = Path(temp) / "census.json"
            path.write_text(json.dumps({"census": [
                {"name": "d139_optional", "classification": "platform_optional",
                 "applicable": False, "probe_policy": "required"},
                {"name": "d139_source", "classification": "our_source",
                 "applicable": False, "probe_policy": "diagnostic_missing"},
            ]}))
            probe = Mock(return_value={"child_returncode": 0, "results": []})
            argv = [str(CHECKER), "--child", "/usr/bin/python3.13", "--launcher", str(LAUNCHER),
                    "--census-file", str(path)]
            with patch.dict(self.namespace, {"_probe": probe}), patch("sys.argv", argv):
                with patch("builtins.print"):
                    self.assertEqual(self.namespace["main"](), 0)
            probe.assert_called_once_with(Path("/usr/bin/python3.13"), [])


if __name__ == "__main__":
    unittest.main()

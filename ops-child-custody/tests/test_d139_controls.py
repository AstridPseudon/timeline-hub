import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

from support import store_python


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "check-child-imports"
MAKER = ROOT / "make-child-venv"


class D139CheckerTests(unittest.TestCase):
    def test_relative_stdlib_external_and_dynamic_classes_are_distinct(self):
        with tempfile.TemporaryDirectory(prefix="d139-check-") as temporary:
            root = Path(temporary) / "pkg"
            root.mkdir()
            (root / "__init__.py").write_text("")
            (root / "module.py").write_text(
                "from .sdk import value\n"
                "import sys\n"
                "import typing_extensions\n"
                "import importlib\n"
                "importlib.import_module(name)\n"
            )
            launcher = root / "launcher.py"
            launcher.write_text("from .module import value\n")
            result = subprocess.run(
                [sys.executable, str(CHECKER), "--child", sys.executable,
                 "--launcher", str(launcher), "--root", str(root)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            census = json.loads(result.stdout)["census"]
            relative = [row for row in census if row["name"] == "pkg.sdk"]
            self.assertTrue(relative)
            self.assertTrue(all(row["classification"] == "relative_source" for row in relative))
            external = [row for row in census if row["name"] == "typing_extensions"]
            self.assertTrue(external)
            self.assertTrue(all(row["classification"] == "installed_distribution" for row in external))
            dynamic = [row for row in census if row["classification"] == "dynamic_unresolved"]
            self.assertTrue(dynamic)
            self.assertEqual(json.loads(result.stdout)["attempted_modules"], ["typing_extensions"])

    def test_missing_many_cli_reports_all_failures_nonzero(self):
        with tempfile.TemporaryDirectory(prefix="d139-missing-") as temporary:
            temporary = Path(temporary)
            imports = temporary / "imports.json"
            imports.write_text(json.dumps(["d139_missing_one", "d139_missing_two", "d139_missing_one"]))
            launcher = temporary / "launcher.py"
            launcher.write_text("")
            result = subprocess.run(
                [sys.executable, str(CHECKER), "--child", sys.executable,
                 "--launcher", str(launcher), "--imports-file", str(imports)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["missing_installed_distributions"],
                             ["d139_missing_one", "d139_missing_two"])
            self.assertEqual({item["name"] for item in report["failures"]},
                             {"d139_missing_one", "d139_missing_two"})

    def test_merged_census_file_is_consumed_without_mass_installing_nonexternal_rows(self):
        with tempfile.TemporaryDirectory(prefix="d139-census-") as temporary:
            temporary = Path(temporary)
            census = temporary / "census.json"
            census.write_text(json.dumps({"census": [
                {"name": "d139_missing", "classification": "installed_distribution", "applicable": True},
                {"name": "pkg.relative", "classification": "relative_source", "applicable": False},
            ]}))
            launcher = temporary / "launcher.py"
            launcher.write_text("")
            result = subprocess.run(
                [sys.executable, str(CHECKER), "--child", sys.executable,
                 "--launcher", str(launcher), "--census-file", str(census)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["attempted_modules"], ["d139_missing"])
            self.assertEqual(report["missing_installed_distributions"], ["d139_missing"])


class D139MakerControls(unittest.TestCase):
    def _tree_hash(self, root):
        entries = {}
        for path in [root, *sorted(root.rglob("*"))]:
            rel = "." if path == root else path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                entries[rel] = ("dir", None, None)
            else:
                data = path.read_bytes()
                mode = "100755" if info.st_mode & 0o111 else "100644"
                entries[rel] = (mode, data, hashlib.sha256(data).hexdigest())

        def tree(rel):
            prefix = "" if rel == "." else rel + "/"
            children = {}
            for name, item in entries.items():
                if name == rel or not name.startswith(prefix):
                    continue
                tail = name[len(prefix):]
                children.setdefault(tail.split("/", 1)[0],
                                    None if "/" in tail or item[0] == "dir" else item)
            payload = []
            for name in sorted(children):
                item = children[name]
                if item is None:
                    mode, digest = "040000", tree(prefix + name)
                else:
                    mode = item[0]
                    digest = hashlib.sha1((mode + " blob\\0").encode() + item[1]).digest()
                payload.append(mode.encode() + b" " + name.encode() + b"\\0" + digest)
            raw = b"".join(payload)
            return hashlib.sha1(("tree " + str(len(raw)) + "\\0").encode() + raw).digest()

        return tree(".").hex()

    def _run_schema_admission(self, source, manifest, expected_tree):
        code = store_python(MAKER.read_text())
        snippet = code[code.index("identity = {"):code.index("seed_helper =")]
        snippet = snippet.replace("75a5a697f630affee40632e500b3f5b704a9b834", expected_tree)
        namespace = {
            "agent": "a" * 40, "backend": "b" * 40,
            "client": "packages/python/client=0" + "0" * 63,
            "schema_required": "1", "schema_source": str(source),
            "schema_manifest": str(manifest), "context": "", "root": str(source.parent),
            "tempfile": tempfile, "shlex": __import__("shlex"),
        }
        prefix = "import hashlib, json, os, pathlib, re, shlex, stat, tempfile\n"
        exec(prefix + snippet, namespace)
        return namespace

    def _synthetic_schema(self):
        temporary = tempfile.TemporaryDirectory(prefix="d139-schema-")
        root = Path(temporary.name)
        (root / "banodoco_timeline_schema").mkdir()
        (root / "pyproject.toml").write_text("[project]\nname='x'\n")
        (root / "banodoco_timeline_schema/__init__.py").write_text("VALUE = 1\n")
        manifest = root.parent / (root.name + ".json")
        manifest.write_text(json.dumps({
            "url": "https://github.com/banodoco/ArtAgents.git",
            "commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85",
            "subdirectory": "packages/timeline-schema/python",
            "source_tree": self._tree_hash(root),
        }))
        manifest.chmod(0o400)
        return temporary, root, manifest

    def test_synthetic_schema_manifest_tamper_and_closed_tree_refuse(self):
        temporary, source, manifest = self._synthetic_schema()
        try:
            tree = self._tree_hash(source)
            self._run_schema_admission(source, manifest, tree)
            tampered = json.loads(manifest.read_text())
            tampered["commit"] = "0" * 40
            manifest.chmod(0o600)
            manifest.write_text(json.dumps(tampered))
            manifest.chmod(0o400)
            with self.assertRaisesRegex(RuntimeError, "sourceNOT_READY"):
                self._run_schema_admission(source, manifest, tree)
            manifest.chmod(0o600)
            manifest.write_text(json.dumps({
                "url": "https://github.com/banodoco/ArtAgents.git",
                "commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85",
                "subdirectory": "packages/timeline-schema/python",
                "source_tree": tree,
                "foreign": True,
            }))
            manifest.chmod(0o400)
            with self.assertRaisesRegex(RuntimeError, "sourceNOT_READY"):
                self._run_schema_admission(source, manifest, tree)
            (source / "foreign.txt").write_text("foreign\n")
            (source / "foreign.txt").chmod(0o644)
            manifest.chmod(0o600)
            manifest.write_text(json.dumps({
                "url": "https://github.com/ArtAgents.git",
                "commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85",
                "subdirectory": "packages/timeline-schema/python",
                "source_tree": tree,
            }))
            manifest.chmod(0o400)
            with self.assertRaisesRegex(RuntimeError, "sourceNOT_READY"):
                self._run_schema_admission(source, manifest, tree)
        finally:
            temporary.cleanup()

    def test_synthetic_schema_source_race_refuses_before_snapshot_publication(self):
        temporary, source, manifest = self._synthetic_schema()
        try:
            tree = self._tree_hash(source)
            target = source / "pyproject.toml"
            original = Path.read_bytes
            reads = {"target": 0}

            def raced(path):
                if path == target:
                    reads["target"] += 1
                    if reads["target"] == 2:
                        target.write_text("changed\n")
                return original(path)

            Path.read_bytes = raced
            try:
                with self.assertRaisesRegex(RuntimeError, "changed during authenticated snapshot"):
                    self._run_schema_admission(source, manifest, tree)
            finally:
                Path.read_bytes = original
        finally:
            temporary.cleanup()

    def test_schema_authority_and_inventory_identity_guards_are_embedded(self):
        text = MAKER.read_text()
        for required in (
            "sourceNOT_READY", "TRUSTED_SCHEMA", "source_tree",
            "D73 schema source contains a symlink or hardlink",
            "protected schema source changed during authenticated snapshot",
            "schema-source-cas", "schema_source_identity_sha256",
            "schema source identity inventory equality", "__timeline_schema_identity__",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_schema_manifest_is_closed_and_not_self_authorizing(self):
        text = MAKER.read_text()
        self.assertIn("if manifest != TRUSTED_SCHEMA", text)
        self.assertIn("physical schema bytes/modes do not match the fixed D73 source tree", text)
        self.assertNotIn("manifest.get('source_tree', manifest.get('tree'))", text)


if __name__ == "__main__":
    unittest.main()

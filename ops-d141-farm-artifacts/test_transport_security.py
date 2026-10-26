"""Isolated transport controls; no extraction, product code, or live services."""

from __future__ import annotations

import argparse
import copy
import gzip
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


SOURCE = Path(__file__).with_name("package_record_closure.py")
SPEC = importlib.util.spec_from_file_location("transport", SOURCE)
transport = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transport)
ROOT = transport.TRANSPORT_ROOT
MANIFEST = f"{ROOT}/manifest.json"
TRUSTED = f"{ROOT}/trusted-schema-manifest.json"
PAYLOAD = f"{ROOT}/site-packages/banodoco_timeline_schema/validate.py"


class SecurityControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = Path(tempfile.mkdtemp(prefix="d141-security-", dir=os.environ["TMPDIR"]))
        cls.original = ARGS.archive.read_bytes()
        assert transport.sha256(cls.original) == ARGS.expected_sha256
        with tarfile.open(fileobj=io.BytesIO(cls.original), mode="r:gz") as archive:
            cls.members = [
                (copy.copy(member), archive.extractfile(member).read() if member.isfile() else None)
                for member in archive
            ]
        cls.counter = 0

    def fixture(self, mutate=lambda rows: rows):
        type(self).counter += 1
        path = self.scratch / f"control-{self.counter}.tgz"
        rows = mutate(copy.deepcopy(self.members))
        with tarfile.open(path, "w:gz") as archive:
            for member, data in rows:
                member.pax_headers.pop("path", None)
                archive.addfile(member, io.BytesIO(data) if data is not None else None)
        self.refresh_sidecar(path)
        return path

    def refresh_sidecar(self, path):
        digest = transport.sha256(path.read_bytes())
        path.with_name(path.name + ".sha256").write_text(digest + "\n")
        return digest

    def reject_structure(self, mutate, reason):
        path = self.fixture(mutate)
        # Deliberately authorize the fixture bytes to exercise checks beyond SHA.
        with self.assertRaisesRegex(transport.Refusal, reason):
            transport.verify_received_archive(path, self.refresh_sidecar(path))

    def change_manifest(self, rows, mutate):
        for member, data in rows:
            if member.name == MANIFEST:
                value = json.loads(data)
                mutate(value)
                data = transport.json_bytes(value)
                member.size = len(data)
                return [(m, data if m.name == MANIFEST else b) for m, b in rows]
        raise AssertionError("missing fixture manifest")

    def replace(self, rows, name, data):
        for member, _ in rows:
            if member.name == name:
                member.size = len(data)
        return [(m, data if m.name == name else b) for m, b in rows]

    def test_original_and_exact_source_conservation(self):
        result = transport.verify_received_archive(ARGS.archive, ARGS.expected_sha256)
        self.assertEqual(result["status"], "PASS_TRANSPORT_CLOSURE")
        schema, maker_sha = transport.extract_trusted_schema(SOURCE.parent.parent / "ops-child-custody/make-child-venv")
        closure = transport.inspect_distribution(ARGS.dist, schema)
        manifest = json.loads(next(b for m, b in self.members if m.name == MANIFEST))
        self.assertEqual(manifest["source_identity"], schema)
        self.assertEqual(manifest["maker_sha256"], maker_sha)
        self.assertEqual(manifest["closure"], closure)
        for entry in closure["files"]:
            name = f"{ROOT}/site-packages/{entry['path']}"
            member, data = next((m, b) for m, b in self.members if m.name == name)
            self.assertEqual(data, (ARGS.dist.parent / entry["path"]).read_bytes())
            self.assertEqual((member.mode, member.uid, member.gid), (int(entry["mode"], 8), entry["uid"], entry["gid"]))
        self.assertEqual(ARGS.archive.read_bytes(), self.original)

    def test_caller_binding_fails_closed(self):
        for digest in [None, "", "0" * 64, ARGS.expected_sha256.upper(), " " + ARGS.expected_sha256]:
            with self.subTest(digest=digest), self.assertRaises(transport.Refusal):
                transport.verify_received_archive(ARGS.archive, digest)
        result = subprocess.run(
            [sys.executable, "-I", "-B", str(SOURCE), "--verify-archive", str(ARGS.archive)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("external manager-peer", result.stderr)

    def test_self_refreshed_sidecar_cannot_authorize_payload(self):
        unhashed = f"{ROOT}/site-packages/banodoco_timeline_schema/__pycache__/theme.cpython-313.pyc"
        direct = f"{ROOT}/site-packages/{transport.DIRECT_PATH}"
        for name in [PAYLOAD, unhashed, direct]:
            def mutate(rows):
                rows = self.replace(rows, name, b"changed")
                def refresh(m):
                    entry = next(e for e in m["closure"]["files"] if name.endswith(e["path"]))
                    m["closure"]["closure_bytes"] += 7 - entry["bytes"]
                    entry.update(bytes=7, sha256=transport.sha256(b"changed"))
                return self.change_manifest(rows, refresh)
            path = self.fixture(mutate)
            with self.subTest(name=name), self.assertRaisesRegex(transport.Refusal, "external manager-peer SHA"):
                transport.verify_received_archive(path, ARGS.expected_sha256)

    def test_physical_archive_and_sidecar_custody(self):
        path = self.fixture()
        digest = self.refresh_sidecar(path)
        symlink = self.scratch / "archive-symlink.tgz"
        symlink.symlink_to(path)
        with self.assertRaisesRegex(transport.Refusal, "physical path"):
            transport.verify_received_archive(symlink, digest)
        hardlink = self.scratch / "archive-hardlink.tgz"
        os.link(path, hardlink)
        with self.assertRaisesRegex(transport.Refusal, "single-link"):
            transport.verify_received_archive(path, digest)
        fifo = self.scratch / "archive-fifo.tgz"
        os.mkfifo(fifo)
        with self.assertRaisesRegex(transport.Refusal, "single-link"):
            transport.verify_received_archive(fifo, digest)
        path = self.scratch / "sidecar-symlink.tgz"
        path.write_bytes(self.original)
        path.with_name(path.name + ".sha256").symlink_to(ARGS.archive.with_name(ARGS.archive.name + ".sha256"))
        with self.assertRaisesRegex(transport.Refusal, "physical path"):
            transport.verify_received_archive(path, ARGS.expected_sha256)

    def test_sidecar_is_consistency_only(self):
        path = self.fixture()
        digest = self.refresh_sidecar(path)
        sidecar = path.with_name(path.name + ".sha256")
        for data in [b"0" * 64 + b"\n", digest.encode(), (digest + "\nextra").encode()]:
            sidecar.write_bytes(data)
            with self.subTest(data=data), self.assertRaisesRegex(transport.Refusal, "sidecar"):
                transport.verify_received_archive(path, digest)

    def test_duplicate_and_missing_members(self):
        for name in [MANIFEST, TRUSTED, ROOT, PAYLOAD]:
            with self.subTest(duplicate=name):
                self.reject_structure(lambda rows: rows + [copy.deepcopy(next(r for r in rows if r[0].name == name))], "duplicate")
            with self.subTest(missing=name):
                self.reject_structure(lambda rows: [r for r in rows if r[0].name != name], "missing|member set")

    def test_unknown_or_unsafe_member_names(self):
        for name in [f"{ROOT}/unknown", f"{ROOT}/unused/", "/absolute", "../escape", f"{ROOT}/../escape", f"{ROOT}//manifest.json", f"{ROOT}/./manifest.json", "x\\escape"]:
            with self.subTest(name=name):
                def mutate(rows):
                    rows[0][0].name = name
                    return rows
                self.reject_structure(mutate, "unsafe|member set|missing")

    def test_nonregular_and_extension_members(self):
        for kind in [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE, tarfile.BLKTYPE, tarfile.GNUTYPE_SPARSE, tarfile.CONTTYPE]:
            with self.subTest(kind=kind):
                def mutate(rows):
                    rows[0][0].type = kind
                    return rows
                self.reject_structure(mutate, "unsupported|structure")
        self.reject_structure(lambda rows: self.set_header(rows, ROOT, "pax_headers", {"SCHILY.xattr.user.test": "value"}), "extension")

    def set_header(self, rows, name, key, value):
        for member, _ in rows:
            if member.name == name:
                setattr(member, key, value)
        return rows

    def test_modes_ownership_and_entry_ownership(self):
        for name in [ROOT, f"{ROOT}/site-packages", MANIFEST, TRUSTED, PAYLOAD]:
            for key, value in [("mode", 0o777), ("mode", 0o4644), ("uid", 12345), ("gid", 12345)]:
                with self.subTest(name=name, key=key, value=value):
                    self.reject_structure(lambda rows: self.set_header(rows, name, key, value), "mode/ownership")
        for key, value in [("uid", 12345), ("gid", 12345), ("nlink", 2), ("nlink", True), ("uid", False), ("mode", "0755")]:
            with self.subTest(entry_key=key):
                self.reject_structure(lambda rows: self.change_manifest(rows, lambda m: m["closure"]["files"][0].update({key: value})), "entry manifest")

    def test_bounded_compressed_and_expanded_input(self):
        path = self.fixture()
        with path.open("ab") as output:
            output.truncate(transport.MAX_ARCHIVE_BYTES + 1)
        with self.assertRaisesRegex(transport.Refusal, "archive limit"):
            transport.verify_received_archive(path, self.refresh_sidecar(path))
        self.reject_structure(lambda rows: self.replace(rows, PAYLOAD, b"x" * (transport.MAX_ARCHIVE_BYTES + 1)), "expanded limit")

    def test_strict_json_in_all_metadata(self):
        for name in [MANIFEST, TRUSTED]:
            original = next(b for m, b in self.members if m.name == name)
            value = json.loads(original)
            key = next(iter(value))
            duplicate = b"{" + json.dumps(key).encode() + b":" + transport.json_bytes(value[key]) + b"," + original[1:]
            with self.subTest(name=name):
                self.reject_structure(lambda rows: self.replace(rows, name, duplicate), "duplicate JSON")
        for data in [b'{"outer":{"key":1,"key":1}}', b'{"value":NaN}', b'[]', b'\xff']:
            with self.subTest(data=data), self.assertRaises(transport.Refusal):
                transport.strict_json(data)

    def test_record_and_self_refreshed_closure_tamper(self):
        for suffix in ["validate.py", "__pycache__/theme.cpython-313.pyc", f"{transport.DIST_INFO}/RECORD", f"{transport.DIST_INFO}/direct_url.json"]:
            name = f"{ROOT}/site-packages/" + (suffix if suffix.startswith(transport.DIST_INFO) else "banodoco_timeline_schema/" + suffix)
            def mutate(rows):
                rows = self.replace(rows, name, b"altered")
                def refresh(m):
                    entry = next(e for e in m["closure"]["files"] if name.endswith(e["path"]))
                    entry.update(bytes=7, sha256=transport.sha256(b"altered"))
                return self.change_manifest(rows, refresh)
            with self.subTest(name=name):
                self.reject_structure(mutate, "RECORD|closure")
        for key, value in [("rows", 17), ("hashed_rows", 11), ("unhashed_rows", [])]:
            with self.subTest(record_key=key):
                self.reject_structure(lambda rows: self.change_manifest(rows, lambda m: m["closure"]["record"].update({key: value})), "entry manifest")

    def test_entry_manifest_identity_and_directory_closure(self):
        for key in ["source_identity", "trusted_manifest_sha256", "maker_sha256", "payload_root", "trusted_manifest_path", "schema", "transport_kind"]:
            with self.subTest(key=key):
                self.reject_structure(lambda rows: self.change_manifest(rows, lambda m: m.update({key: "wrong"})), "entry manifest identity")
        self.reject_structure(lambda rows: self.change_manifest(rows, lambda m: m["closure"]["directories"].pop()), "directory manifest")
        self.reject_structure(lambda rows: self.change_manifest(rows, lambda m: m["closure"]["files"].append(m["closure"]["files"][0])), "entry manifest")
        for key in ["url", "commit", "subdirectory", "source_tree"]:
            def mutate(rows):
                obj = json.loads(next(b for m, b in rows if m.name == TRUSTED))
                obj[key] = "wrong"
                return self.replace(rows, TRUSTED, transport.json_bytes(obj))
            with self.subTest(identity_key=key):
                self.reject_structure(mutate, "trusted manifest identity")

    def test_invalid_and_trailing_archive_data(self):
        path = self.fixture()
        path.write_bytes(b"invalid gzip")
        with self.assertRaises(transport.Refusal):
            transport.verify_received_archive(path, self.refresh_sidecar(path))
        path = self.fixture()
        data = gzip.decompress(path.read_bytes()) + b"hidden member"
        path.write_bytes(gzip.compress(data))
        with self.assertRaisesRegex(transport.Refusal, "terminator"):
            transport.verify_received_archive(path, self.refresh_sidecar(path))

    def test_mode_preserving_receiving_advice_supersedes_embedded_advice(self):
        result = transport.verify_received_archive(ARGS.archive, ARGS.expected_sha256)
        advice = result["safe_receiver"]
        self.assertIn("--expected-sha256 MANAGER_PEER_SHA256", advice["preflight"])
        self.assertIn("--same-permissions", advice["extract"])
        self.assertNotIn("--no-same-permissions", advice["extract"])
        self.assertIn("--no-same-owner", advice["extract"])
        self.assertIn("--keep-old-files", advice["extract"])
        self.assertIn("review PASS", advice["gate"])
        # Do not execute extraction: checked modes are 0644/0755 and no special bits.
        self.assertEqual({m.mode for m, _ in self.members}, {0o644, 0o755})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--dist", type=Path, required=True)
    ARGS = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SecurityControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())

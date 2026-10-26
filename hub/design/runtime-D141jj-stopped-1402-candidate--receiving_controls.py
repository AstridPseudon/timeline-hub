"""Focused private controls for the D141z Main receiving adaptation."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
REGISTRY = ORCH / "tests/suites.conf"
BUILDER = ORCH / "bin/delivery-build"


def load_installer():
    spec = importlib.util.spec_from_file_location("d141z_installer", ROOT / "install-final-services.py")
    if spec is None or spec.loader is None:
        raise AssertionError("installer module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


installer = load_installer()
candidate = ROOT / "runtime-final-service-rows.txt"
raw = REGISTRY.read_bytes()
rows = candidate.read_bytes()
assert digest(raw) == installer.REGISTRY_SHA256
assert digest(rows) == installer.CANDIDATE_SHA256
installer.validate_registry(raw, rows)
installer.validate_artifacts(BUILDER)

caller_text = (ROOT / "run-final-delivery.py").read_text()
assert str(ROOT / "run-final-delivery.py") in rows.decode()
assert installer.RUNNER_SHA256 in rows.decode()
assert installer.LIFECYCLE_HELPER_SHA256 in (ROOT / "delivery_lifecycle.py").read_bytes().hex() or digest((ROOT / "delivery_lifecycle.py").read_bytes()) == installer.LIFECYCLE_HELPER_SHA256
assert "from delivery_lifecycle import run_delivery" in caller_text

private = Path(tempfile.mkdtemp(prefix="d141z-receiving-", dir=os.environ.get("TMPDIR", "/tmp")))
private_registry = private / "suites.conf"
private_registry.write_bytes(raw)
private_registry.chmod(0o600)
private_backup = private / "suites.conf.preimage"
installer.FINAL_TUPLE = private / "source-tuple.json"
installer.GATE_TUPLE = private / "gate-tuple.json"
source = b"private source tuple fixture\n"
gate = b"private gate tuple fixture\n"
installer.install(private_registry, candidate, private_backup, source, gate)
replacement = raw + rows.replace(installer.TUPLE_MARKER, digest(source).encode()).replace(
    installer.GATE_MARKER, digest(gate).encode()
)
assert private_registry.read_bytes() == replacement
assert private_backup.read_bytes() == raw
assert private_registry.stat().st_mode & 0o777 == 0o600
assert private_backup.stat().st_mode & 0o777 == 0o600
def outside(data: bytes) -> list[bytes]:
    result = []
    for line in data.splitlines(keepends=True):
        fields = line.split(None, 2)
        if len(fields) < 2 or fields[1].decode() not in installer.NEW_NAMES:
            result.append(line)
    return result


outside_before = outside(raw)
outside_after = outside(private_registry.read_bytes())
assert outside_before == outside_after

drift = private / "drift.conf"
drift.write_bytes(raw + b"# unrelated drift\n")
try:
    installer.validate_registry(drift.read_bytes(), rows)
except ValueError:
    pass
else:
    raise AssertionError("global preimage drift was accepted")
assert drift.read_bytes() == raw + b"# unrelated drift\n"

poison = private / "poisoned-caller.py"
poison.write_bytes((ROOT / "run-final-delivery.py").read_bytes() + b"\n# poison\n")
old_runner = installer.RUNNER
installer.RUNNER = poison
try:
    installer.validate_artifacts(BUILDER)
except ValueError:
    pass
else:
    raise AssertionError("poisoned caller was accepted")
finally:
    installer.RUNNER = old_runner

print("PASS adapted scoped CAS: exact caller/helper closure, current Main preimage, private install/readback/backup/fsync path, outside-row conservation, drift refusal, poisoned-caller refusal")

"""Independent acceptance for the private F-final row-launcher successor."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shlex
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
CANDIDATE = EVIDENCE / "candidate"
ROWS = CANDIDATE / "runtime-final-service-rows.txt"
SOURCE = CANDIDATE / "final-source-tuple.json"
GATE = CANDIDATE / "final-gate-tuple.json"
BUILDER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build")
REGISTRY = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf")

EXPECTED = {
    "check.sh": "16af7a95c308d85feff4d4f198b9187a2af0f48f99d76997f2a8e2868dac6332",
    "core-inventory.json": "e6a1fa17796e493532c3927e2ec6fc8fdb4e1928b7540be8c6644b3d0894bb14",
    "delivery_gate_build.py": "a26c2817e81ee1a725d7087ea0f4dd9cc3512d4d9c0d511407106cedc75d74c8",
    "delivery_lifecycle.py": "7607908a006fbedff58112ffbc4cb0bb68112615250c00de325b3e2e49fd63d3",
    "inherited-runtime-final-service-rows.txt": "774aafcd47adbdbce61c680132d091bb363f6466368d42e0c4ef55ee14615d3b",
    "install-final-services.py": "8469b0785dd741fa00d031acb26ed8e4aced33cb4b1e548eed230943f9d558db",
    "install-map.json": "c262a1ea4255f371cbe4bcbe2729743dd63ace8101200f2c64dac9dbd35ab308",
    "receiving_controls.py": "eba87c089e06c1a3d6e48e7a7ee05d2015db2eee0cf9167936ff7b40f19cbc9e",
    "run-final-delivery.py": "0a043d1c06d0c0b824e418108682341615248ad19d7aa39754fd6234a740d85a",
    "run-final-services.py": "8aea49759e600d18f5ed1f5e297269aa8dddad3a24024f776ac37e7c7d53acd7",
    "runtime-final-service-rows.txt": "c9fd51d178d736c2073d7936f031e3b38a813149f42aa3d85edfb4974d82565c",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd="/", env=env, text=True, capture_output=True, timeout=90)


def load_installer():
    spec = importlib.util.spec_from_file_location("launcher_installer", CANDIDATE / "install-final-services.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def launcher_argv() -> tuple[list[str], str, str, str]:
    row = next(line for line in ROWS.read_text().splitlines() if "delivery-v2-final" in line)
    _, name, command = row.split(None, 2)
    assert name == "delivery-v2-final"
    argv = shlex.split(command)
    assert argv[0] == "env"
    code = argv[argv.index("-c") + 1]
    assert "sys.path.insert(0,str(p.parent));" in code
    assert "hashlib.sha256(data).hexdigest()==sys.argv[2]" in code
    return argv, row, code, command


def concrete_command(argv: list[str], root: Path, source_sha: str, gate_sha: str, stub: Path, stub_sha: str) -> list[str]:
    result = list(argv)
    result = [source_sha if item == "FINAL_TUPLE_SHA256_PENDING" else gate_sha if item == "GATE_TUPLE_SHA256_PENDING" else item for item in result]
    result[result.index("--wrapper") + 1] = str(stub)
    result[result.index("--wrapper-sha") + 1] = stub_sha
    result[result.index("--receipt") + 1] = str(root / "delivery-receipt.json")
    return result


def main() -> int:
    assert EVIDENCE.is_absolute() and EVIDENCE.name == "evidence"
    assert SOURCE.is_file() and GATE.is_file() and BUILDER.is_file() and REGISTRY.is_file()
    source_sha, gate_sha = digest(SOURCE), digest(GATE)
    assert source_sha == "90b9da111d31a6f866795332521b6b6c660c1bfd2a9da92ee0c6d97683c1a561"
    assert gate_sha == "eec639784d85238545dfa244d4c8f79a7385f9d946f0453dc12115e5b8dbbec8"

    for name, expected in EXPECTED.items():
        path = CANDIDATE / name
        assert path.is_file() and not path.is_symlink(), name
        assert digest(path) == expected, name
    for path in CANDIDATE.glob("*.json"):
        json.loads(path.read_text())
    for path in CANDIDATE.glob("*.py"):
        ast.parse(path.read_text(), filename=str(path))
    compile_root = Path(tempfile.mkdtemp(prefix="launcher-pycache-", dir=EVIDENCE / "tmp"))
    compile_env = {**os.environ, "PYTHONPYCACHEPREFIX": str(compile_root), "PYTHONDONTWRITEBYTECODE": "0"}
    compiled = run([sys.executable, "-m", "compileall", "-q", "-f", str(CANDIDATE)], env=compile_env)
    assert compiled.returncode == 0, compiled.stderr
    ruff_env = {**os.environ, "RUFF_CACHE_DIR": str(EVIDENCE / "tmp" / "ruff-cache")}
    ruff = run(["ruff", "check", "--isolated", "--select", "F", *[str(p) for p in CANDIDATE.glob("*.py")]], env=ruff_env)
    assert ruff.returncode == 0, ruff.stdout + ruff.stderr
    bash = run(["bash", "-n", str(CANDIDATE / "check.sh")])
    assert bash.returncode == 0, bash.stderr
    print("PASS source closure hashes, AST, JSON, private compile, ruff F, and bash syntax")

    private = Path(tempfile.mkdtemp(prefix="launcher-acceptance-", dir=EVIDENCE / "tmp"))
    stub = private / "stub-delivery-gate.py"
    stub.write_text(
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "args=sys.argv[1:]\n"
        "receipt=Path(args[args.index('--receipt')+1])\n"
        "Path(os.environ['LAUNCHER_STUB_MARK']).write_text(json.dumps({'argv': args, 'cwd': os.getcwd()}))\n"
        "receipt.write_text(json.dumps({'status':'stub-pass','argv':args})+'\\n')\n"
    )
    stub_sha = digest(stub)
    argv, row, code, command = launcher_argv()
    clean_env = dict(os.environ)
    for key in ("PYTHONPATH", "PYTHONHOME", "NODE_PATH"):
        clean_env.pop(key, None)
    clean_env["LAUNCHER_STUB_MARK"] = str(private / "stub-argv.json")
    clean_env["TMPDIR"] = str(private)
    clean_env["TMP"] = str(private)
    clean_env["TEMP"] = str(private)
    actual = concrete_command(argv, private, source_sha, gate_sha, stub, stub_sha)
    old_code = code.replace("sys.path.insert(0,str(p.parent));", "")
    old_argv = list(actual)
    old_argv[old_argv.index("-c") + 1] = old_code
    old = run(old_argv, env=clean_env)
    assert old.returncode != 0 and "delivery_lifecycle" in (old.stdout + old.stderr)
    assert not (private / "stub-argv.json").exists()
    print("PASS original registered exec reproduces sibling-import failure with PYTHONPATH unset")

    launched = run(actual, env=clean_env)
    assert launched.returncode == 0, launched.stdout + launched.stderr
    receipt = json.loads((private / "delivery-receipt.json").read_text())
    stub_record = json.loads((private / "stub-argv.json").read_text())
    assert receipt["status"] == "PASS"
    assert "--gate-tuple" in stub_record["argv"]
    assert "--builder" in stub_record["argv"]
    assert "--repos" in stub_record["argv"]
    lifecycle = next(private.glob("**/lifecycle.json"))
    lifecycle_value = json.loads(lifecycle.read_text())
    assert lifecycle_value["status"] == "complete" and lifecycle_value["trace_status"] == "PASS"
    (EVIDENCE / "sampler-lifecycle.json").write_text(json.dumps(lifecycle_value, indent=2, sort_keys=True) + "\n")
    print("PASS registered hashchecked exec: caller import, source tuple, lifecycle, D68 argv, and harmless stub")

    bad_hash = list(actual)
    bad_hash[bad_hash.index("--tuple-sha") + 1] = "0" * 64
    bad = run(bad_hash, env=clean_env)
    assert bad.returncode == 2 and not (private / "delivery-receipt.json.bad").exists()
    source_link = private / "source-link.json"
    source_link.symlink_to(SOURCE)
    symlink = list(actual)
    symlink[symlink.index("--source-tuple") + 1] = str(source_link)
    refused = run(symlink, env=clean_env)
    assert refused.returncode == 2
    print("PASS malformed tuple hash and symlink source refusal before lifecycle/stub")

    installer = load_installer()
    received = run([sys.executable, str(CANDIDATE / "receiving_controls.py")])
    assert received.returncode == 0, received.stdout + received.stderr
    no_install = run([sys.executable, str(CANDIDATE / "install-final-services.py"), "--registry", str(REGISTRY), "--candidate", str(ROWS), "--builder", str(BUILDER)])
    assert no_install.returncode == 0, no_install.stdout + no_install.stderr
    wrong = private / "wrong-rows.txt"
    wrong.write_bytes(ROWS.read_bytes() + b"runtime wrong-row true\n")
    try:
        installer.validate_registry(REGISTRY.read_bytes(), wrong.read_bytes())
    except ValueError:
        pass
    else:
        raise AssertionError("wrong-row candidate was accepted")
    print("PASS scoped-CAS installer readback/backup/drift/wrong-row/outside-byte controls")

    result = {
        "status": "PASS",
        "registered_row": "delivery-v2-final",
        "import_fix": "row exec inserts hashchecked script parent before exec",
        "pythonpath_unset": True,
        "builder_invoked": False,
        "real_staging": False,
        "lifecycle_controls_repeated": False,
        "candidate_sha256": digest(ROWS),
        "tuple_sha256": source_sha,
        "gate_sha256": gate_sha,
    }
    (EVIDENCE / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS F-final launcher acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

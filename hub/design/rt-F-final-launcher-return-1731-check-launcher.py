"""Independent acceptance for the concrete F-final launcher successor."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shlex
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
    "install-final-services.py": "ae18753b7d66aa750608c1e0c683af9150812fcae32b35d05418b2fd59ebd2e4",
    "install-map.json": "c262a1ea4255f371cbe4bcbe2729743dd63ace8101200f2c64dac9dbd35ab308",
    "receiving_controls.py": "9d3f50fd3eb46e6992ea330cfcbd4dee41df31880190a47276d3b187a3f8a015",
    "run-final-delivery.py": "0a043d1c06d0c0b824e418108682341615248ad19d7aa39754fd6234a740d85a",
    "run-final-services.py": "8aea49759e600d18f5ed1f5e297269aa8dddad3a24024f776ac37e7c7d53acd7",
    "runtime-final-service-rows.txt": "d86ef7ee366adff5bcf2297f40cb247e14b8d818f2dd147b97bb26cb8a974f18",
}
NAMES = ("core-v2-final-integration", "delivery-v2-final", "delivery-v2-dryrun")
REQUIRED_CALLER_ARGS = (
    "--source-tuple", "--tuple-sha", "--gate-tuple", "--gate-tuple-sha",
    "--wrapper", "--wrapper-sha", "--builder", "--builder-sha", "--receipt",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd="/", env=env, text=True, capture_output=True, timeout=90)


def load_installer():
    spec = importlib.util.spec_from_file_location("launcher_installer", CANDIDATE / "install-final-services.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def row_parts(line: bytes) -> tuple[str, str, str]:
    repo, name, command = line.decode().rstrip("\n").split(None, 2)
    return repo, name, command


def row_code(command: str) -> str:
    start = command.index("'") + 1
    end = command.index("'", start)
    return command[start:end]


def successor_line(old_line: bytes) -> bytes:
    repo, name, command = row_parts(old_line)
    if name == NAMES[0]:
        return old_line
    code = row_code(command)
    fixed = code.replace(
        "sys.argv=[str(p),*sys.argv[3:]];",
        "sys.argv=[str(p),*sys.argv[3:]]; sys.path.insert(0,str(p.parent));",
        1,
    )
    assert fixed != code
    start = command.index("'") + 1
    end = command.index("'", start)
    return f"{repo} {name} {command[:start]}{fixed}{command[end:]}\n".encode()


def selected(raw: bytes) -> dict[str, bytes]:
    result = {}
    for line in raw.splitlines(keepends=True):
        if line.startswith(b"runtime "):
            name = line.split(None, 2)[1].decode()
            if name in NAMES:
                result[name] = line
    assert tuple(result) == NAMES
    return result


def concrete_command(argv: list[str], root: Path, stub: Path, stub_sha: str, label: str) -> list[str]:
    result = list(argv)
    result[result.index("--wrapper") + 1] = str(stub)
    result[result.index("--wrapper-sha") + 1] = stub_sha
    result[result.index("--receipt") + 1] = str(root / f"{label}-receipt.json")
    return result


def main() -> int:
    assert EVIDENCE.is_absolute() and EVIDENCE.name == "evidence"
    assert SOURCE.is_file() and GATE.is_file() and BUILDER.is_file() and REGISTRY.is_file()
    for name, expected in EXPECTED.items():
        path = CANDIDATE / name
        assert path.is_file() and not path.is_symlink(), name
        assert path.stat().st_size < 100 * 1024 * 1024, name
        assert digest(path.read_bytes()) == expected, name
    live = selected(REGISTRY.read_bytes())
    candidate = selected(ROWS.read_bytes())
    assert ROWS.read_bytes() == b"".join(successor_line(live[name]) for name in NAMES)
    assert candidate[NAMES[0]] == live[NAMES[0]]
    assert row_code(candidate[NAMES[1]].decode().split(None, 2)[2]).count("sys.path.insert(0,str(p.parent));") == 1
    assert row_code(candidate[NAMES[2]].decode().split(None, 2)[2]).count("sys.path.insert(0,str(p.parent));") == 1

    source_sha, gate_sha = digest(SOURCE.read_bytes()), digest(GATE.read_bytes())
    assert source_sha == "90b9da111d31a6f866795332521b6b6c660c1bfd2a9da92ee0c6d97683c1a561"
    assert gate_sha == "eec639784d85238545dfa244d4c8f79a7385f9d946f0453dc12115e5b8dbbec8"
    commands = {name: shlex.split(row_parts(candidate[name])[2]) for name in NAMES}
    core = commands[NAMES[0]]
    assert core[core.index("--tuple-sha") + 1] == source_sha
    assert core[-1] == "core"
    for name in NAMES[1:]:
        argv = commands[name]
        assert all(flag in argv for flag in REQUIRED_CALLER_ARGS), name
        assert argv[argv.index("--tuple-sha") + 1] == source_sha
        assert argv[argv.index("--gate-tuple-sha") + 1] == gate_sha
        assert argv[argv.index("--wrapper") + 1] != argv[argv.index("--receipt") + 1]
        assert argv[argv.index("--builder") + 1] == str(BUILDER)
    assert "--dry-run" in commands[NAMES[2]]
    print("PASS live-registry derivation, exact core row, mechanical three-row diff, and complete argv")

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
    print("PASS AST, JSON, private compile, Ruff F, and shell syntax")

    private = Path(tempfile.mkdtemp(prefix="launcher-acceptance-", dir=EVIDENCE / "tmp"))
    private.chmod(0o700)
    stub = private / "stub-delivery-gate.py"
    stub.write_text(
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "args=sys.argv[1:]\n"
        "required=['--gate-tuple','--gate-tuple-sha','--builder','--builder-sha','--stage-parent','--receipt']\n"
        "assert all(flag in args for flag in required) and '--' in args\n"
        "receipt=Path(args[args.index('--receipt')+1])\n"
        "Path(os.environ['LAUNCHER_STUB_MARK']).write_text(json.dumps({'argv':args,'cwd':os.getcwd()}))\n"
        "receipt.write_text(json.dumps({'status':'stub-pass','argv':args})+'\\n')\n"
    )
    stub_sha = digest(stub.read_bytes())
    clean_env = dict(os.environ)
    for key in ("PYTHONPATH", "PYTHONHOME", "NODE_PATH"):
        clean_env.pop(key, None)
    clean_env.update({"TMPDIR": str(private), "TMP": str(private), "TEMP": str(private)})

    old_argv = shlex.split(row_parts(live[NAMES[1]])[2])
    old_actual = concrete_command(old_argv, private, stub, stub_sha, "old")
    clean_env["LAUNCHER_STUB_MARK"] = str(private / "old-stub.json")
    old = run(old_actual, env=clean_env)
    assert old.returncode != 0 and "delivery_lifecycle" in (old.stdout + old.stderr)
    assert not (private / "old-stub.json").exists()
    print("PASS original actual registered exec fails at sibling import with PYTHONPATH unset")

    lifecycle_values = []
    for name in NAMES[1:]:
        row_tmp = private / name
        row_tmp.mkdir(mode=0o700)
        actual = concrete_command(shlex.split(row_parts(candidate[name])[2]), private, stub, stub_sha, name)
        clean_env["LAUNCHER_STUB_MARK"] = str(private / f"{name}-stub.json")
        clean_env["TMPDIR"] = str(row_tmp)
        clean_env["TMP"] = str(row_tmp)
        clean_env["TEMP"] = str(row_tmp)
        launched = run(actual, env=clean_env)
        assert launched.returncode == 0, launched.stdout + launched.stderr
        receipt = json.loads((private / f"{name}-receipt.json").read_text())
        stub_record = json.loads((private / f"{name}-stub.json").read_text())
        assert receipt["status"] == "PASS"
        wrapper_args = stub_record["argv"]
        assert all(flag in wrapper_args for flag in ("--gate-tuple", "--builder", "--builder-sha", "--receipt", "--stage-parent"))
        builder_args = wrapper_args[wrapper_args.index("--") + 1:]
        assert "--repos" in builder_args
        if name == NAMES[2]:
            assert "--dry-run" in builder_args
        lifecycle = next(row_tmp.glob("**/timeline-delivery-KEEP/lifecycle.json"))
        lifecycle_value = json.loads(lifecycle.read_text())
        assert lifecycle_value["status"] == "complete" and lifecycle_value["trace_status"] == "PASS"
        lifecycle_values.append(lifecycle_value)
    (EVIDENCE / "sampler-lifecycle.json").write_text(json.dumps(lifecycle_values, indent=2, sort_keys=True) + "\n")
    print("PASS corrected final and dryrun complete argv parsing, lifecycle, D68 boundary, and harmless full-path stub")

    bad_hash = list(concrete_command(shlex.split(row_parts(candidate[NAMES[1]])[2]), private, stub, stub_sha, "bad-hash"))
    bad_hash[bad_hash.index("--tuple-sha") + 1] = "0" * 64
    bad = run(bad_hash, env=clean_env)
    assert bad.returncode == 2
    source_link = private / "source-link.json"
    source_link.symlink_to(SOURCE)
    symlink = list(concrete_command(shlex.split(row_parts(candidate[NAMES[1]])[2]), private, stub, stub_sha, "symlink"))
    symlink[symlink.index("--source-tuple") + 1] = str(source_link)
    refused = run(symlink, env=clean_env)
    assert refused.returncode == 2
    print("PASS tuple hash drift and symlink refusal before lifecycle/stub")

    installer = load_installer()
    received = run([sys.executable, str(CANDIDATE / "receiving_controls.py")])
    assert received.returncode == 0, received.stdout + received.stderr
    no_install = run([
        sys.executable, str(CANDIDATE / "install-final-services.py"),
        "--registry", str(REGISTRY), "--candidate", str(ROWS), "--builder", str(BUILDER),
    ])
    assert no_install.returncode == 0, no_install.stdout + no_install.stderr
    wrong = private / "wrong-rows.txt"
    wrong.write_bytes(ROWS.read_bytes() + b"runtime wrong-row true\n")
    try:
        installer.validate_registry(REGISTRY.read_bytes(), wrong.read_bytes())
    except ValueError:
        pass
    else:
        raise AssertionError("wrong-row candidate was accepted")
    print("PASS actual unchanged installer CLI, concrete tuple custody, outside-byte/CAS/drift/wrong-row controls")

    result = {
        "status": "PASS",
        "registered_rows": list(NAMES),
        "import_fix": "final and dryrun rows add only hashchecked script-parent setup",
        "pythonpath_unset": True,
        "builder_invoked": False,
        "real_registry_install": False,
        "canonical_tuples_written": False,
        "candidate_sha256": digest(ROWS.read_bytes()),
        "tuple_sha256": source_sha,
        "gate_sha256": gate_sha,
    }
    (EVIDENCE / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS F-final launcher acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Bounded D29 carrier proof: requester -> unchanged dispatcher -> maker preflight."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")

def run(argv, *, env=None, cwd=None, timeout=8):
    return subprocess.run(argv, env=env, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout)

def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()

def make_repo(path: Path, files: dict[str, str], message: str) -> str:
    path.mkdir(parents=True)
    run(["git", "init", "-q", str(path)])
    run(["git", "-C", str(path), "config", "user.name", "D29 fixture"])
    run(["git", "-C", str(path), "config", "user.email", "d29@example.invalid"])
    for name, value in files.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)
    run(["git", "-C", str(path), "add", "."])
    result = run(["git", "-C", str(path), "commit", "-q", "-m", message])
    assert result.returncode == 0, result.stdout
    return git(path, "rev-parse", "HEAD")

def node_bin(path: Path, node: str = "v20.19.4", npm: str = "10.8.2"):
    path.mkdir(parents=True, exist_ok=True)
    (path / "node").write_text(f"#!/bin/sh\nprintf '%s\\n' '{node}'\n")
    (path / "npm").write_text(f"#!/bin/sh\nprintf '%s\\n' '{npm}'\n")
    (path / "node").chmod(0o755)
    (path / "npm").chmod(0o755)

def main() -> None:
    base = Path(os.environ.get("D29_BASE_ORCH", DEFAULT_ORCH))
    assert hashlib.sha256((base / "bin/make-runtime").read_bytes()).hexdigest() == "99cca067330fd87e1f8c475045ab8282e944b2455e25d44d4c6072e77e9e4e28"
    assert hashlib.sha256((base / "bin/request-runtime").read_bytes()).hexdigest() == "f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1"
    with tempfile.TemporaryDirectory(prefix="d29-carrier-", dir=os.environ.get("TMPDIR")) as raw:
        root = Path(raw); private = root / "private"; orch = private / "orch"; work = private / "work"
        (orch / "bin").mkdir(parents=True); (orch / "queue/pending").mkdir(parents=True)
        (orch / "queue/done").mkdir(); (orch / "queue/refused").mkdir(); (orch / "tests").mkdir()
        (work / "runtimes").mkdir(parents=True)
        for name in ("suites.conf", "agent-remotion-0013.env"):
            shutil.copy2(base / "tests" / name, orch / "tests" / name)
        for name in ("request-runtime", "make-runtime", "dispatcher-daemon"):
            shutil.copy2(base / "bin" / name, orch / "bin" / name)
        dispatcher = orch / "bin/dispatcher-daemon"
        dispatcher.write_text(dispatcher.read_text().replace(
            f"O={base}", f"O={orch}"))
        assert 'elif head -c8 "$f" | grep -q \'^RUNTIME \'' in dispatcher.read_text()
        # Feed the canonical patch through patch(1), without inventing a queue payload.
        result = subprocess.run(["patch", "--batch", "--fuzz=0", "-d", str(orch), "-p1"],
                                input=(HERE / "remotion-toolchain.patch").read_text(),
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert result.returncode == 0, result.stdout
        assert run(["bash", "-n", str(orch / "bin/request-runtime")]).returncode == 0
        assert run(["bash", "-n", str(orch / "bin/make-runtime")]).returncode == 0
        agent = root / "agent"
        package = json.dumps({"name":"fixture-remotion","engines":{"node":"=20.19.4","npm":"=10.8.2"}}, separators=(",", ":"))
        lock = json.dumps({"name":"fixture-remotion","lockfileVersion":3,"packages":{"":{"name":"fixture-remotion"},"node_modules/remotion":{"version":"3.0.0"},"node_modules/@banodoco/timeline-composition":{"version":"0.0.13"}}}, separators=(",", ":"))
        agent_sha = make_repo(agent, {"remotion/package.json": package, "remotion/package-lock.json": lock}, "fixture agent")
        runtime = root / "runtime"
        runtime_sha = make_repo(runtime, {"README": "fixture runtime\n"}, "fixture runtime")
        lock_sha = hashlib.sha256(lock.encode()).hexdigest()
        valid = ["agent-remotion-d29-2110", agent_sha, lock_sha, str(agent), str(runtime), runtime_sha, "agent-remotion-0013-nodes"]
        def request(args, *, env_extra=None, clean=False):
            env = {"PATH": os.environ.get("PATH", "")}
            if not clean: env.update({k:v for k,v in os.environ.items() if not k.startswith("RUNTIME_")})
            env.update({"RUNTIME_ORCH_ROOT": str(orch), **(env_extra or {})})
            return run([str(orch / "bin/request-runtime"), *args], env=env)
        def dispatch(name, *, clean=False):
            env = {"PATH": os.environ.get("PATH", ""), "RUNTIME_ORCH_ROOT": str(orch)}
            if not clean: env.update({k:v for k,v in os.environ.items() if not k.startswith("RUNTIME_")})
            return run(["timeout", "1s", str(orch / "bin/dispatcher-daemon")], env=env, timeout=4)
        def chain(name, node, *, clean=False, expect_preflight=True):
            binpath = root / "toolchains" / name
            node_bin(binpath, *node)
            args = valid + [str(binpath)]
            queued = request(args, clean=clean)
            assert queued.returncode == 0, queued.stdout
            assert dispatch(name, clean=clean).returncode in (0, 124)
            refused = orch / "queue/refused" / f"runtime-{valid[0]}"
            assert refused.is_file(), f"{name}: done={list((orch / 'queue/done').iterdir())} refused={list((orch / 'queue/refused').iterdir())} pending={list((orch / 'queue/pending').iterdir())}"
            output = refused.read_text()
            if expect_preflight:
                assert "bench store helper unavailable" in output, output
                assert "build required" not in output and "status=created" not in output, output
            return output
        normal = chain("normal", ("v20.19.4", "10.8.2"))
        env_i = chain("envi", ("v20.19.4", "10.8.2"), clean=True)
        assert "PREFLIGHT FAILED" not in normal and "PREFLIGHT FAILED" not in env_i
        # Legacy requester shapes remain queue-compatible; maker shapes remain source-visible.
        for i, args in enumerate(([valid[0], valid[1]], [valid[0], valid[1], lock_sha], valid)):
            queued = request(args)
            assert queued.returncode == 0, queued.stdout
            assert (orch / "queue/pending" / f"runtime-{valid[0]}").is_file()
            (orch / "queue/pending" / f"runtime-{valid[0]}").unlink()
        maker_text = (orch / "bin/make-runtime").read_text()
        assert "2|3)" in maker_text and "6|7)" in maker_text and "  8)" in maker_text
        invalid = 0
        for label, value in (("wrong-version", ("v22.0.0", "10.8.2")), ("wrong-npm", ("v20.19.4", "9.0.0"))):
            out = chain(label, value, expect_preflight=False); assert "selected-toolchain" in out; invalid += 1
        missing = root / "toolchains/missing"
        queued = request(valid + [str(missing)]); assert queued.returncode == 0
        assert dispatch("missing").returncode in (0, 124)
        assert "selected-toolchain" in (orch / "queue/refused/runtime-agent-remotion-d29-2110").read_text(); invalid += 1
        physical = root / "toolchains/physical"; node_bin(physical)
        symlink = root / "toolchains/symlink"; symlink.symlink_to(physical, target_is_directory=True)
        queued = request(valid + [str(symlink)]); assert queued.returncode == 0
        assert dispatch("symlink").returncode in (0, 124)
        assert "physical-directory-required" in (orch / "queue/refused/runtime-agent-remotion-d29-2110").read_text(); invalid += 1
        for label, path in (("relative", "relative/bin"), ("traversal", "/tmp/../toolchain/bin"), ("whitespace", "/tmp/tool chain/bin")):
            result = request(valid + [path]); assert result.returncode == 2; invalid += 1
        result = request(valid + [str(root / "toolchains/physical"), "extra"]); assert result.returncode == 2; invalid += 1
        result = request(valid + [str(root / "toolchains/physical")], env_extra={"RUNTIME_NODE_BIN": "/tmp/inherited"})
        assert result.returncode == 2; invalid += 1
        assert invalid == 9
        print("PASS cases=14 explicit=2 legacy=3 wrong-version/npm/path/missing/symlink/unsafe/extra/ambiguous=9 store=0 build=0")
        print("PASS actual requester -> unchanged dispatcher RUNTIME word-shape -> actual maker preflight")

if __name__ == "__main__":
    main()

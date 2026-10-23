#!/usr/bin/env python3
"""Finite private carrier fixture; it never touches the live ORCH or benches."""
import os
import pathlib
import subprocess
import tempfile


ROOT = pathlib.Path(tempfile.mkdtemp(prefix="child-carrier-"))
ORCH = ROOT / "orch"
WORK = ROOT / "work"
AGENT = ROOT / "agent"
RUNTIME = ROOT / "runtime"
REQUESTER = pathlib.Path(os.environ["CARRIER_REQUESTER"])
MAKER = pathlib.Path(os.environ["CARRIER_MAKER"])
(ORCH / "queue" / "pending").mkdir(parents=True)
(ORCH / "queue" / "done").mkdir()
(ORCH / "queue" / "refused").mkdir()
(ORCH / "tests").mkdir()
WORK.mkdir()


def run(command, *, env=None, check=True):
    return subprocess.run(command, env=env, text=True, capture_output=True, check=check)


def git(repo, *args):
    return run(["git", "-C", str(repo), *args]).stdout.strip()


def source_repo(path, files):
    path.mkdir()
    run(["git", "init", "-q", str(path)])
    run(["git", "-C", str(path), "config", "user.email", "fixture@example.invalid"])
    run(["git", "-C", str(path), "config", "user.name", "carrier fixture"])
    run(["git", "-C", str(path), "config", "commit.gpgsign", "false"])
    for name, content in files.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    run(["git", "-C", str(path), "add", "."])
    run(["git", "-C", str(path), "commit", "-qm", "fixture"])
    return git(path, "rev-parse", "HEAD")


agent_sha = source_repo(AGENT, {"pyproject.toml": "[project]\nname='astrid'\nversion='0'\n"})
runtime_sha = source_repo(
    RUNTIME,
    {
        "pyproject.toml": "[project]\nname='astrid-runtime'\nversion='0'\n",
        "packages/python/astrid_runtime_client/__init__.py": "CLIENT = True\n",
    },
)

base_env = {
    "PATH": os.environ["PATH"],
    "HOME": str(ROOT),
    "CHILD_VENV_ORCH_ROOT": str(ORCH),
    "CHILD_VENV_WORK_ROOT": str(WORK),
}
explicit = [
    "venv-agent-child-carrier",
    agent_sha,
    "agent-remotion-0013-nodes",
    "agent-remotion-0013",
    "--source-carrier",
    str(AGENT),
    str(RUNTIME),
    runtime_sha,
]


def request(args, *, ambient=True):
    env = dict(base_env)
    if ambient:
        env.update(
            CHILD_VENV_AGENT_CHECKOUT=str(ROOT / "wrong-agent"),
            CHILD_VENV_RUNTIME_CHECKOUT=str(ROOT / "wrong-runtime"),
        )
    return run([str(REQUESTER), *args], env=env, check=False)


result = request(explicit)
assert result.returncode == 0, result.stderr
pending = ORCH / "queue/pending/childvenv-venv-agent-child-carrier"
assert pending.read_text() == "CHILDVENV " + " ".join(explicit) + "\n"

# Exercise the installed dispatcher branch's exact word-split invocation.
dispatch_env = dict(base_env)
dispatch_env.update(PATH=os.environ["PATH"])
dispatch = run(
    ["bash", "-c", f"{MAKER} $(sed 's/^CHILDVENV //' {pending})"],
    env=dispatch_env,
    check=False,
)
assert dispatch.returncode == 2, dispatch.stderr
assert "PREFLIGHT FAILED" in dispatch.stderr
assert "requirements/proof.lock" in dispatch.stderr
assert not (WORK / explicit[0]).exists()

# The maker itself must honor the carrier in an empty environment and stop
# after source preflight, before any target/build setup.
maker = run([str(MAKER), *explicit], env=dispatch_env, check=False)
assert maker.returncode == 2, maker.stderr
assert "PREFLIGHT FAILED" in maker.stderr

normal_maker_env = dict(
    dispatch_env,
    CHILD_VENV_AGENT_CHECKOUT=str(ROOT / "wrong-agent"),
    CHILD_VENV_RUNTIME_CHECKOUT=str(ROOT / "wrong-runtime"),
)
normal_maker = run([str(MAKER), *explicit], env=normal_maker_env, check=False)
assert normal_maker.returncode == 2, normal_maker.stderr
assert "PREFLIGHT FAILED" in normal_maker.stderr

# Old 2/3/4-argument calls retain their exact meaning and queue shape.
for args in (
    ["venv-agent-child-old2", agent_sha],
    ["venv-agent-child-old3", agent_sha, "base"],
    ["venv-agent-child-old4", agent_sha, "base", "graph"],
):
    env = dict(base_env, CHILD_VENV_AGENT_CHECKOUT=str(AGENT), CHILD_VENV_RUNTIME_CHECKOUT=str(RUNTIME))
    old = run([str(REQUESTER), *args], env=env, check=False)
    assert old.returncode == 0, old.stderr
    payload = ORCH / ("queue/pending/childvenv-" + args[0])
    assert payload.read_text() == "CHILDVENV " + " ".join(args) + "\n"
    old_maker = run([str(MAKER), *args], env=env, check=False)
    assert old_maker.returncode == 2 and "PREFLIGHT FAILED" in old_maker.stderr

# Incomplete, unknown, wrong-SHA, symlinked, dirty, and missing-client inputs
# refuse before queueing or creation.
for args in (
    explicit[:-1],
    explicit + ["extra"],
    explicit[:-1] + ["0" * 40],
):
    refused = request(args)
    assert refused.returncode == 2

symlink = ROOT / "agent-link"
symlink.symlink_to(AGENT, target_is_directory=True)
refused = request(explicit[:5] + [str(symlink), str(RUNTIME), runtime_sha])
assert refused.returncode == 2 and "symlinked" in refused.stderr

no_client = ROOT / "runtime-no-client"
no_client_sha = source_repo(no_client, {"pyproject.toml": "[project]\nname='astrid-runtime'\nversion='0'\n"})
refused = request(explicit[:5] + [str(AGENT), str(no_client), no_client_sha])
assert refused.returncode == 2 and "client" in refused.stderr.lower()

(AGENT / "dirty.txt").write_text("dirty\n")
refused = request(explicit)
assert refused.returncode == 2 and "dirty" in refused.stderr

print("PASS cases=16 queued=4 dispatcher=1 maker_preflight=6 refusals=6")

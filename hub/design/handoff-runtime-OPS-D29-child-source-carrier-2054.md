# OPS-D29 report — PASS

Implemented worker-authored private copies of `request-child-venv` and `make-child-venv`.

Carrier shape:

```text
NAME AGENT_SHA BASE_SUITE REMOTION_GRAPH --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
```

Legacy 2/3/4-argument calls remain unchanged. Explicit paths/SHA are parsed first, validated canonically, and the requested Runtime SHA must equal the serialized checkout HEAD.

Production command:

```sh
/tmp/.../orch/bin/request-child-venv \
  venv-agent-child-ap2-current-079-2a9-1743 \
  079580ca46af77e0292d49dc34386b25c8391f99 \
  agent-remotion-0013-nodes \
  agent-remotion-ap2-current-079-2a9-1743 \
  --source-carrier \
  /home/user/work/wt/agt-pin-079580ca \
  /home/user/work/wt/rt-pin-2a9e347f \
  2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d
```

Validation:

```text
bash -n both scripts                         PASS
embedded Python compile                      PASS
private patch apply + cmp + diff --check     PASS
private fixture                             PASS
  cases=16 queued=4 dispatcher=1
  maker_preflight=6 refusals=6
```

No daemon restart, live queue, child request, install, network, pin/source checkout, or Runtime worktree change was performed.

Hashes:

```text
base request: 72cafb3a5ec343f648a0e41d59a51e7c803ee51b4d04a394dc2010df828bd731
base maker:   89d82618c6c67819e40cc73d32b6d1c372f95889761d5170bb1af3a83dc5fcff
dispatcher:   f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15

final request: 3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33
final maker:   c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2
request patch: e8a696ea6f787f5d92afad190bde0cca4977e4025beb991ee005fa64d5532b20
maker patch:   526caee0a7991023620fe10448dcb61f00189ee30c8c66e358c6a484d1e2e990
fixture:       0a19112d55d5023b93d6be9dee71bdb16f2a4b0ddcaaa3045ed9ab741079803b
```

The assigned worker `tmpdir` was a regular file, producing: `mkdir: cannot create directory .../tmpdir: Not a directory`. Scratch was kept in the permitted harness `$TMPDIR`; total size was 152K.

Commit message and `DONE` marker are ready. No production qualification claim is made.

```diff
--- bin/request-child-venv
+++ bin/request-child-venv
@@ -1,5 +1,6 @@
 #!/bin/bash
 # request-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH]
+# Explicit source carrier: ... --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
 # D21c retains exact Agent, Runtime backend and generated client custody.
 set -u -o pipefail
 O=${CHILD_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
@@ -7,11 +8,24 @@
 A=${CHILD_VENV_AGENT_CHECKOUT:-/home/user/work/agent}
 R=${CHILD_VENV_RUNTIME_CHECKOUT:-/home/user/work/runtime}
 N=${1:-}; S=${2:-}; BS=${3:-}; REMOTION=${4:-}
+RUNTIME_SHA=
 refuse() { echo "REFUSED: $*" >&2; exit 2; }
-case "$O:$W:$A:$R" in /*:/*:/*:/*) ;; *) refuse 'roots must be absolute';; esac
+case "$O:$W" in /*:/*) ;; *) refuse 'roots must be absolute';; esac
 [[ "$N" =~ ^venv-agent-child-[a-z0-9-]+$ ]] || refuse 'invalid child name'
 [[ "$S" =~ ^[0-9a-f]{40}$ ]] || refuse 'exact 40-character Agent commit required'
-[ "$#" -le 4 ] || refuse 'call shape is NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH]'
+if [ "$#" -eq 8 ] && [ "$5" = --source-carrier ]; then
+  A=$6; R=$7; RUNTIME_SHA=$8
+elif [ "$#" -gt 4 ]; then
+  refuse 'call shape is NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH] [--source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA]'
+fi
+case "$A:$R" in /*:/*) ;; *) refuse 'source checkouts must be absolute';; esac
+[[ "$A" =~ ^/[A-Za-z0-9._/-]+$ && "$R" =~ ^/[A-Za-z0-9._/-]+$ ]] || refuse 'source checkout path contains unsafe characters'
+[ "$A" = "$(readlink -e -- "$A" 2>/dev/null)" ] || refuse 'Agent checkout path is missing or symlinked'
+[ "$R" = "$(readlink -e -- "$R" 2>/dev/null)" ] || refuse 'Runtime checkout path is missing or symlinked'
+if [ -z "$RUNTIME_SHA" ]; then
+  RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || refuse 'Runtime source unavailable'
+fi
+[[ "$RUNTIME_SHA" =~ ^[0-9a-f]{40}$ ]] || refuse 'exact 40-character Runtime commit required'
 source_state() {
   local checkout=$1 wanted=$2 actual status
   actual=$(git -C "$checkout" rev-parse --verify HEAD^{commit} 2>/dev/null) || return 1
@@ -20,7 +34,6 @@
   [ -z "$status" ]
 }
 source_state "$A" "$S" || refuse 'requested Agent checkout/commit is unavailable, mismatched or dirty'
-RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || refuse 'Runtime source unavailable'
 source_state "$R" "$RUNTIME_SHA" || refuse 'Runtime checkout is dirty'
 CLIENT_IDENTITY=$(git -C "$R" ls-tree -r --name-only "$RUNTIME_SHA" packages/python/astrid_runtime_client/ | while IFS= read -r path; do
   [ -n "$path" ] || continue; printf '%s=' "$path"; git -C "$R" show "$RUNTIME_SHA:$path" | sha256sum | cut -d' ' -f1
@@ -202,7 +215,15 @@
 fi
 [ "${CHILD_VENV_REUSE_ONLY:-0}" != 1 ] || refuse 'existing target failed identity/preflight'
 [ ! -e "$W/$N" ] && [ ! -L "$W/$N" ] || refuse 'existing same-name target failed identity/preflight'
-# The installed dispatcher uses word splitting, not eval. Keep this exact legacy payload unquoted.
-for arg in "$@"; do [[ "$arg" =~ ^[a-zA-Z0-9_-]+$ ]] || refuse 'dispatcher arguments must be simple names'; done
-printf 'CHILDVENV %s %s%s%s\n' "$N" "$S" "${BS:+ $BS}" "${REMOTION:+ $REMOTION}" > "$O/queue/pending/childvenv-$N"
+# The installed dispatcher uses word splitting, not eval. Keep legacy fields
+# simple, while allowing only the canonical absolute carrier paths.
+for arg in "$N" "$S" "$BS" "$REMOTION"; do
+  [ -z "$arg" ] || [[ "$arg" =~ ^[a-zA-Z0-9_-]+$ ]] || refuse 'dispatcher arguments must be simple names'
+done
+if [ "$#" -eq 8 ]; then
+  [[ "$A" =~ ^/[A-Za-z0-9._/-]+$ && "$R" =~ ^/[A-Za-z0-9._/-]+$ && "$RUNTIME_SHA" =~ ^[0-9a-f]{40}$ ]] || refuse 'dispatcher carrier contains unsafe fields'
+  printf 'CHILDVENV %s %s%s%s --source-carrier %s %s %s\n' "$N" "$S" "${BS:+ $BS}" "${REMOTION:+ $REMOTION}" "$A" "$R" "$RUNTIME_SHA" > "$O/queue/pending/childvenv-$N"
+else
+  printf 'CHILDVENV %s %s%s%s\n' "$N" "$S" "${BS:+ $BS}" "${REMOTION:+ $REMOTION}" > "$O/queue/pending/childvenv-$N"
+fi
 echo "child venv $N queued; result in $O/queue/done/childvenv-$N"
--- bin/make-child-venv
+++ bin/make-child-venv
@@ -1,6 +1,7 @@
 #!/bin/bash
 # make-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH] — dispatcher child venv.
 # The fourth argument remains the optional Remotion graph used for suite substitution.
+# Explicit source carrier: ... --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
 set -u -o pipefail
 
 O=${CHILD_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
@@ -19,9 +20,9 @@
 PIP_RETRIES=${CHILD_VENV_PIP_RETRIES:-2}
 REQUIREMENTS_PATH=${CHILD_VENV_REQUIREMENTS_PATH:-requirements/proof.lock}
 
-case "$O:$A:$R:$W" in
-  /*:/*:/*:/*) ;;
-  *) echo 'REFUSED: child venv roots and source checkouts must be absolute' >&2; exit 2;;
+case "$O:$W" in
+  /*:/*) ;;
+  *) echo 'REFUSED: child venv roots and work root must be absolute' >&2; exit 2;;
 esac
 
 progress() { printf '%s child-venv %s\n' "$(date -u +%FT%TZ)" "$*"; }
@@ -30,13 +31,27 @@
 S=${2:-}
 BS=${3:-}
 RT=${4:-}
+RUNTIME_SHA=
 case "$N" in
   venv-agent-child-[a-z0-9-]*) ;;
   *) echo "REFUSED: name must be venv-agent-child-<suffix>"; exit 2 ;;
 esac
 [[ "$N" =~ ^venv-agent-child-[a-z0-9-]+$ ]] || { echo 'REFUSED: invalid child name'; exit 2; }
 [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: exact Agent commit required'; exit 2; }
-[ "$#" -le 4 ] || { echo 'REFUSED: invalid call shape'; exit 2; }
+if [ "$#" -eq 8 ] && [ "$5" = --source-carrier ]; then
+  A=$6; R=$7; RUNTIME_SHA=$8
+elif [ "$#" -gt 4 ]; then
+  echo 'REFUSED: call shape is NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH] [--source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA]' >&2
+  exit 2
+fi
+case "$A:$R" in /*:/*) ;; *) echo 'REFUSED: source checkouts must be absolute' >&2; exit 2;; esac
+[[ "$A" =~ ^/[A-Za-z0-9._/-]+$ && "$R" =~ ^/[A-Za-z0-9._/-]+$ ]] || { echo 'REFUSED: source checkout path contains unsafe characters' >&2; exit 2; }
+[ "$A" = "$(readlink -e -- "$A" 2>/dev/null)" ] || { echo 'REFUSED: Agent checkout path is missing or symlinked' >&2; exit 2; }
+[ "$R" = "$(readlink -e -- "$R" 2>/dev/null)" ] || { echo 'REFUSED: Runtime checkout path is missing or symlinked' >&2; exit 2; }
+if [ -z "$RUNTIME_SHA" ]; then
+  RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || { echo 'REFUSED: Runtime source unavailable' >&2; exit 2; }
+fi
+[[ "$RUNTIME_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: exact Runtime commit required' >&2; exit 2; }
 
 # Authenticate source state before either existing-target lookup or build setup.
 source_state() {
@@ -47,7 +62,6 @@
   [ -z "$status" ]
 }
 source_state "$A" "$S" || { echo 'REFUSED: Agent checkout/commit is unavailable, mismatched or dirty'; exit 2; }
-RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || { echo 'REFUSED: Runtime checkout unavailable'; exit 2; }
 source_state "$R" "$RUNTIME_SHA" || { echo 'REFUSED: Runtime checkout is dirty'; exit 2; }
```

Fixture source:

```python
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
```
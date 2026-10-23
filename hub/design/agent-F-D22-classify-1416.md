# Agent F D22 requalification classification

Status: **RUNNING** at the bounded handoff (`2026-10-23T14:26:57Z`). The
single authorized full service was not stopped and no replacement full or
targeted run was requested. This is a progress handoff, not a qualification.

## Sole service and retained files

The production caller was invoked exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-full-1342 full-current-v3-1229
```

Service ID:

```text
agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679
```

Result directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679
```

The exact retained files were read:

| File | Observed evidence |
|---|---|
| `request` | `target=agt-F-D22-full-1342`, `repo=agent`, `suite=full-current-v3-1229`, empty `files`, `nocache=0`, requested `2026-10-23T13:44:53Z` |
| `snap` | `tree=c4d72b065d6e68c92e4335120cc016cadf53b06a`, key `d21d099f1e62fb9145dd40b3e26c414d`, worktree `/home/user/work/wt/agt-F-D22-full-1342` |
| `ext` | external metadata: Runtime `8592822fd11275540f596562f43c715676f2bc0f`, App `4282d776497f651bce3870d1d9e6a37a5eaa2030`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` |
| `runner.log` | empty at handoff |
| `log.txt` | 18,758 bytes at handoff; progress reached 90% and was still growing |
| `status` | exactly `running` |
| `heavy` | empty |

There was no terminal `summary`, exit code, full traceback section, or exact
pytest node list. Therefore no node is called PASS, and no failure is assigned
to a source owner, upstream/preexisting cause, D14, D23, or environment cause.

## Locked identity and recipe

Agent identity is the requested base
`8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, with the preflight real-runner
snapshot commit `c711594fecd6cecf4fc87b93c647145f3a8dcf21`, parent equal to the
requested base, and tree
`c4d72b065d6e68c92e4335120cc016cadf53b06a`. The source/test/pyproject hash
lock was clean in preflight.

The exact full-suite row remains the sole `agent full-current-v3-1229` row,
with row SHA-256
`9035bd9672c7186c440e4e3aaee15ae3dfbeaeb0192864f0a68b9f68cc212879` and
this command/environment:

```text
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-3b926efa" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages /bin/sh -c 'test -x /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node && test -x /home/user/work/venv-agent/bin/python && test -d /home/user/work/wt/rt-pin-3b926efa/runtime_protocol && test -d /home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules && test -d /home/user/work/venv-agent/lib/python3.13/site-packages && exec /home/user/work/venv-agent/bin/python -P -c '''import hashlib,json,os,subprocess,sys; from pathlib import Path; import astrid,runtime_protocol,astrid_runtime_client; import astrid.core.timeline.banodoco_schema as schema; import banodoco_timeline_schema as shared_schema; import pytest,xdist; root=Path.cwd().resolve(); runtime=Path(os.environ["ASTRID_RUNTIME_CHECKOUT"]).resolve(); profile=Path(os.environ["ASTRID_REMOTION_PROJECT_DIR"]).resolve(); node=Path(os.environ["ASTRID_NODE_EXECUTABLE"]).resolve(); assert Path(astrid.__file__).resolve()==root/"astrid/__init__.py"; assert Path(runtime_protocol.__file__).resolve()==runtime/"runtime_protocol/__init__.py"; assert Path(astrid_runtime_client.__file__).resolve()==root/"astrid_runtime_client/__init__.py"; assert Path(schema.__file__).resolve()==root/"astrid/core/timeline/banodoco_schema.py"; assert Path(shared_schema.__file__).resolve()==Path("/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py"); assert os.environ.get("PYTHONNOUSERSITE") is None; assert subprocess.run([str(node),"--version"],capture_output=True,text=True,check=True).stdout.strip()=="v20.19.4"; lock=profile/"package-lock.json"; assert hashlib.sha256(lock.read_bytes()).hexdigest()=="f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"; package=json.loads((profile/"package.json").read_text()); dep=package["dependencies"]["@banodoco/timeline-composition"]; archive=profile/dep.removeprefix("file:"); assert hashlib.sha256(archive.read_bytes()).hexdigest()=="819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"; assert json.loads((profile/"node_modules/@banodoco/timeline-composition/package.json").read_text())["version"]=="0.0.14"; raise SystemExit(pytest.main(["-q","-n","3"]))'''
```

The actual locked Runtime module origin is `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol`:

- commit `3b926efab2eed122d374540baee297d4cdcec62a`;
- tree `b794170504544b259781e50d7ca4d61b6729e67c`;
- imported protocol file SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.

The actual Composition recipe is the installed profile
`/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, package version
`0.0.14`, lock SHA-256
`f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`, and
selected archive SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
The newer 859 environment is not claimed. The `ext` hashes above are retained
service metadata and do not replace the full row's locked Runtime3b/profile
recipe.

## Current progress markers; not a census

At the handoff, counting raw progress characters in `log.txt` gave:

```text
F=193  E=33  s=33  u=390
```

These are only live progress markers. They are not exact node identities or
terminal totals: `F` and `E` have no traceback/node mapping yet, `s` is not
expanded into a skip inventory, and `u` is deliberately left uninterpreted
until pytest's final summary establishes whether it represents deselection,
xfail, or another runner marker. No PASS is inferred from dots, exit state,
cache, or a neighboring node. The zero-test policy is therefore not met: a
zero collected count or an otherwise empty result cannot qualify this run.

D14's exact-two case and D23's child-word-anchor case remain required visible
checks. Their exact terminal nodes and outcomes are not present in the live
log, so both are **unconfirmed**, not passed or suppressed. Original tests
remain unchanged and no xfail/skip was added.

## Classification and next action

Classification is intentionally deferred because the service is still
running. Once it reaches a terminal state, the same service must be polled and
its complete node/traceback/skip/deselection/xfail inventory preserved before
classifying: actual regression owner; proven upstream/preexisting; visible
D14/D23 deferred; or unconfirmed when evidence is insufficient. Existing
owners R1 private1403, R2redo1404, and G5restructure1416 should be referenced
only when the terminal traceback proves that ownership. Runtimecfa0 and
unmerged G5 drafts are outside this full current8c + Runtime3b qualification.

No product, test, generated, dependency, environment, pin, or shared-dependency
file was changed. No full retry, targeted rerun, daemon operation, or service
stop was performed.

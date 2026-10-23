# Agent F full environment recipe — independent finalpass

Date: 2026-10-23 UTC  
Reviewer: `agt-F-full-env-review-1235`  
Reviewed handoff: `agt-F-full-env-handoff-1229`  
Verdict: **PASS for the recipe and row; not a full-suite/body PASS**

## Scope

This is a read-only operations review of the one `agent full-current-v3-1229`
row in `ORCH/tests/suites.conf`, at Agent base `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`.
No Agent product/test file, Runtime/App/Composition worktree, installation,
dependency, pin, schema, contract, Git ref, daemon, or live operation was
changed. The full v2 request/reply surface remains outside this row-only
review: base, commands, label, per-step patches, reads/ordinals, merge,
idempotency, dry-run, source/rationale/group_id, accepted/merged/fullcanonical
records, deps/effects/steps/history/undo_steps/preview, required
`would_status`, structured conflict, and invalid code/path/hint/command.

## Row and caller proof

The row occurs exactly once at line 22. The exact row bytes, including the
trailing LF, hash to:

```text
9035bd9672c7186c440e4e3aaee15ae3dfbeaeb0192864f0a68b9f68cc212879
```

The bytes outside the row at review time are recorded as:

```text
prefix lines 1-21: 87a8da0a0096d1ba678ea9b93c35265fe36f9945acaa3a922930d6b6d3759afb
suffix lines 23-end: 9c98d5e4c7b80950c9b428f505540cedcb7bec5093a7c0df62eeee59086a34cc
whole suites.conf: fad72f6a41b3018a2a955df2805eea538c7056b6dfaf326e52fb3453b00dcc2d
```

The service extraction is byte-for-byte equivalent to the reviewed row:

```sh
CMD=$(awk '$1=="agent" && $2=="full-current-v3-1229" {$1=$2=""; sub(/^ +/,""); print; exit}' "$ORCH/tests/suites.conf")
```

The extracted command passed `bash -n`. Its nested `/bin/sh -c '...'` keeps
the five literal pre-body checks before `&& exec`; the Python `-c` payload is
single-quoted through the outer shell and is therefore one argument. The
production caller is exactly:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-full-env-handoff-1229 full-current-v3-1229
```

`request-test` queues the named row. The dispatcher extracts the same row,
snapshots the worker tree, changes to that snapshot, and runs the command via
`bash -c`; its outer service timeout is 90 minutes. No request was submitted
by this reviewer because this task forbids a full/body run. Farm must use the
caller above, not the stale `full` row or the old D09 row, and must run one
full body only after this review.

## Environment identity

The row's current tuple was verified locally at these exact paths. These are
Farm prerequisites, not claims that an arbitrary remote machine has them.

| prerequisite | observed identity |
| --- | --- |
| Agent input | commit `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`, tree `ff6c46d0b5ba420e3fb9e912e5a30c7a9a41e27` |
| Runtime checkout | `/home/user/work/wt/rt-pin-3b926efa`, commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean detached checkout |
| Runtime import | `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/__init__.py`, SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2` |
| Python | `/home/user/work/venv-agent/bin/python`, Python `3.13.16` |
| pytest / xdist | `pytest 9.0.2`, `xdist 3.8.0` |
| Node | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `v20.19.4` |
| Composition profile | `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, installed `@banodoco/timeline-composition` `0.0.14` |
| profile lock | SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d` |
| selected archive | `artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` |
| shared schema | `/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py` |

The row deliberately does not assign `PYTHONNOUSERSITE`; the same-process
assertion requires `os.environ.get("PYTHONNOUSERSITE") is None`. The stale
Runtime/profile paths `rt-pin-95bd3c5f` and
`agent-remotion-composition14-255b6856` are not used by this row.

## Bounded checks

Exact commands and results:

```text
awk row count + service extraction comparison: PASS; exactly one row
bash -n on the extracted row command: PASS
same env import probe: PASS; Agent, Runtime3b, client, pytest and xdist origins verified
missing Runtime3b directory substituted in the pre-body gate: rc=1, 0 output
xdist child-origin probe: /home/user/work/venv-agent/bin/python -P -m pytest -q -n 3 -s tmp_child_origin_probe.py
  6 passed in 1.94s; temporary probe was removed after the check
```

The positive collection result is reused from the exact handoff row evidence
(no duplicate full collection was needed):

```text
16913/17598 tests collected (685 deselected) in 44.96s, exit 0
```

This is collection evidence only. It does not claim any test body, HTTP,
browser, live-socket, render, D09, or full-suite result.

## Discovery and skip preservation

The row invokes `pytest.main(["-q", "-n", "3"])` without `-m`, `-k`,
`--deselect`, `--ignore`, or `-p no:` overrides. Default `pyproject.toml`
addopts remain in effect. `tests/conftest.py` still imports the lane hooks
`pytest_collection_modifyitems`, `pytest_configure`, and `pytest_ignore_collect`
from `tests.lanes`; the single `LANES` registry and `_SkipGuard` remain the
source of declared deselection/skips. The 685 deselections are therefore the
configured default-off lanes shown by collection, not an invisible row-level
deselection. The handoff row's Python process prints actual module origins and
hashes before invoking pytest, and the separate xdist probe confirms child
environment/origins are preserved.

## Farm instructions and holds

Farm prerequisites are the literal paths in the table above: the d1fa Agent
snapshot, Runtime3b checkout and protocol package, Python venv with pytest and
xdist, Node20.19.4, the 819acf profile/node_modules, the installed schema
site-packages directory, and ordinary `/usr/bin:/bin` shell utilities. Verify
them on Farm before invoking the exact `request-test` command. Do not infer
availability from this local review, provision or install into shared paths,
reconstruct the environment from an old row, or duplicate the manager's full
request.

If Farm reports an actual-tool/autoclassifier denial, stop and report it; do
not substitute a tool or alter this row. A D18 productguard error is a harness
diagnosis, not evidence to edit the production recipe. The full body remains
Farm-owned and is the only next qualification; its result must be reported
separately from this PASS.

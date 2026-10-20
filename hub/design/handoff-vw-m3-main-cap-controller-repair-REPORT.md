**Three controller blockers repaired and frozen; no capture authorized or run.**

New artifacts use only the absolute prefix `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-`. The old rejected
controller/render/COMMAND/REPORT retain all four SHA256 values from the rejecting
gate and must never be granted. Repository product/tests and shared dependencies,
runtimes, venvs and caches were untouched; the worker worktree remains clean.

Frozen SHA256:

| Artifact | SHA256 |
|---|---|
| controller.py | `41455095972277d6e2b8da04f7796bfb6579cb960c948f64b7fed1e5adc2fde3` |
| render.mjs | `c5be04066bfef43c76b97464f9ce1cc981ca9fc36a224bd2ffe0a078338437e4` |
| COMMAND.txt | `234e79bec954b7378a761f2ad3a9c7aed3fb0c618fe5aefc6cc9fbf4e01581cf` |

[Exact command and manager-only grant instructions](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-COMMAND.txt).
No placeholders: the proposed existing small grant has exactly three lines,
the suite command followed by the two literal approved script hashes. No actual
grant or suite registration was created. Synthetic calibration grants existed
only inside disposable private fake directories and were removed.

Changes and implementation choices:

- Original MAIN reads now use the durable read-only `/home/user/work/agent`
  object store, always pinned to `a411628f8fd6129f9c58c332019b56769d997384`.
  Only `git archive`/`git show` read that store; no creator worktree dependency.
- Main owns allocation: `stage_allocated` becomes true only after `mkdir`
  succeeds. A nested finally cleans only this allocation, including partial
  source staging and postflight evidence failures. Refused pre-existing
  directories, files and symlinks retain their sentinel data.
- Both scripts independently compare controller AND render SHA256 against the
  manager-owned grant. The controller checks before preflight/allocation,
  rechecks before stage allocation and every child execution; the renderer
  checks before stage inspection or peer imports. Path-only or changed-byte
  grants refuse. This extends the existing test grant without a new protocol.

Preserved guards: immutable source/freeze and 2,414 original MAIN files; all 29
lock-exact Composition6 members and generated package bytes; physical f816 SSR
full graph, six peers, versions and Node/browser bytes; pre/post source and graph
checks; raw-closure consumer replay with all seven byte-equal outputs; original
Root/aliases/normal TimelineComposition; actual 1920x1080, numeric30, duration120
metadata before exactly frames90/105/119; original PNG hashes/bytes and RGB240
frame90/background#050814 measurement with separate RGBA reporting; 10GiB floor,
2GiB headroom and 500ms watchdogs; real private scopes/cache parents and peer leaf
links; central-only request checks, lock and exclusive no-auto-rerun marker.
These execution guards are retained in code, not claims of completed capture.

Executed commands and results (all paths absolute):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-guard-tests.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-guard-tests.log 2>&1
```

Exit0: **9 tests passed** (1.356s). Includes actual pinned-MAIN source reads;
exact disk boundaries/QUIET; absent grant; path-only/controller-tamper/render-
tamper refusal before preflight/log/spawn; real refusal-preserves-sentinel
calibrations for directory/file/symlink; real cleanup of tiny partial staging
and postflight-failure fixtures; success cleanup and retry refusal. Renderer
hash checks execute only its built-in-import admission header in a fake ORCH,
ending before stage inspection or any peer import. No renderer was executed.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-controller.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-guard-tests.py
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-render.mjs
git -C /home/user/work/wt/vw-m3-main-cap-controller-repair diff --check
git -C /home/user/work/wt/vw-m3-main-cap-controller-repair status --porcelain=v1 --untracked-files=all
```

All exit0: Ruff passed; Node syntax passed; git checks produced no output.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-controller.py preflight
```

Exit1 **STAGE_BLOCKED solely by disk**: `12,499,419,136` free bytes versus
unchanged `13,021,077,036` required (10GiB reserve +
2,283,658,796 staging/headroom). Short by
`521,657,900` bytes at measurement.
No budget/floor override, source extraction or actual stage allocation occurred.
Source/fixture/29-member package and preflight full-graph checks passed.

Physical graph: checkout `f8164bef73215272562c4d6974acadbd82c2898a`, 21,488 entries,
SHA256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`.
The complete manifest and six peer/tool byte hashes remained identical before/
after preflight and after the guard tests; see `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-graph-pre.json`,
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-preflight.json` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-controller-repair-offline-postflight.json`.
Actual grant, capture-stage, CAPTURE-STARTED and PNGs are absent; disposable test
fixtures were removed. No browser, render, socket, network, install, git mutation,
product/full suite or service request ran.

**Unverified / next:** consumer generator/seven-output execution, bundling/cache
behavior, actual metadata and actual PNG pixels/RGB opacity remain unverified.
Source prediction at90/105/119 is 1/0.5/1⁄30; **0.5 is not an approved golden**.
No App/unified parity, audio, Runtime admission or Gate6 claim. Manager must
obtain a fresh independent verdict for these exact hashes and enough disk for
the unchanged reserve plus headroom before considering the new exact grant and
one named central attempt. Never grant the old rejected controller. The repair
task is complete; capture remains held separately.

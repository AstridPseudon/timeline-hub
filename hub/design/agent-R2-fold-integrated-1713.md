# R2 integrated occurrence-fold proof

## Verdict

PASS for the bounded integrated proof requested. No product source edits were
made by this worker. The exact integrated Agent tree is
`280e8669f56b41a1023e14219d5fad6eda006260`, tree
`12e290fd07b5f9892eb8ac21b3279a65a1d5d595`; it is the reviewed `64e7c59e1`
tree. HEAD is a two-parent merge with first parent `63baa707b` and second
parent `64e7c59e1`. Runtime was the clean pinned checkout
`/home/user/work/wt/rt-pin-d9e2a71e`, HEAD
`d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, tree
`9b07545cac9a8bbafb16246aaa6f72050ef7cffe`.

## Focused proof

Exact requested command body, run once:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py
```

Result: **113 passed in 11.87s**; no skip, deselect, or xfail was reported.
The shell wrapper also attempted to tee into the worker `tmpdir`, but that
path is an existing pointer file (`/tmp/w-62ade97b2`), not a directory. Thus
the wrapper exit was 1 from `tee`, while pytest itself reached 100% and passed.
The test was not rerun.

The four test files retain the strict alias/source/order/membership/ABA and
contradictory-storage negative controls. No original-nine duplicate, public
redo, c271, P1/P4, full, browser, daemon, or native14 run was made.

## Source identity and preservation

The fold commit has exactly two changed paths and two reviewed blobs:

```text
209b6036b1158b1f4ba7ef40a23f1cbcc5831889  astrid/sdk/timeline/inverse.py
914575c88c64edf6d164c2523f3b7a6a4bcd3f4f  tests/editing_conformance/test_captured_registry_redo.py
```

`git diff --name-status 63baa707b HEAD` reports only those two paths. The
current R1/private and 103-predecessor paths are unchanged from `63baa707b`:
`_commit_patch.py`, `_recording.py`, `_root_inverse.py`, `_step_undo.py`,
`commit.py`, and `test_captured_nested_redo.py`. This preserves the prior
103-case source-history qualification and the current R1 private carrier.

Current relevant SHA-256 values:

```text
b971050c92b14304bbc037ed775ddb7ddfa6cf5a233cd2075f92ba68725c3163  astrid/sdk/timeline/_commit_patch.py
85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43  astrid/sdk/timeline/_recording.py
0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a  astrid/sdk/timeline/_root_inverse.py
206f13ac5991ed6abecbc0b1fbde24f2526cb3bf2f47f57f9b91c66aa43fa1dc  astrid/sdk/timeline/_step_undo.py
a4d612aeadfd66011258b9003d3b7d9a4f33c4fa387c50b65bf4fa79bafb4e91  astrid/sdk/timeline/commit.py
0638e98f11a96230246f8c9685b48096abea6524a5308f9cce787bb69989380a  astrid/sdk/timeline/inverse.py
9779118aaf953b1bee428fddf27690bb1a2bfcbbf63defcd4945cf661d64e1c2  tests/editing_conformance/test_captured_registry_redo.py
d7567b519698bd9ae36b44f1747ad26dd0e394dd7f1cdaaf3b83866ed2b7f8d4  tests/editing_conformance/test_captured_nested_redo.py
2365ad33012766f7531077f0608308d458452b57d210c85654b725b2584da338  tests/editing_conformance/test_inverse_stage_images.py
30788f581da21db7099f3c7adb746a4d4312cbcc6f9b302967ed095696fb61a8  tests/editing_conformance/test_step_undo_v2.py
```

## Import provenance

The specified `PYTHONPATH` was used. Post-run direct probes resolved Agent
modules to this worktree, including
`astrid/sdk/timeline/inverse.py` and `astrid/sdk/timeline/commit.py`, and
resolved Runtime modules to the pinned checkout, including
`runtime_protocol/service.py`. `astrid_runtime_client` resolved to the Agent
worktree's vendored client. The pre-run probe output was not separately
captured before pytest; because the command used the same unchanged source
tree and both worktrees were clean before/after, the post-run resolution is
the applicable source identity. This is an evidence limitation, not a
source-integrity failure.

## Quality and reused evidence

Fresh scoped checks, all exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-62ade97b2/ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py --cache-dir /tmp/w-62ade97b2/mypy --hide-error-context --no-pretty
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

The reviewed prior evidence is explicitly reused, not claimed as a new run:
Ruff baseline **2149/2149**, private mypy baseline **1912/1912**, vendor and
artifact checks, plus the independent bounded fold 113-pass and causal
two-test old-source RED. The prior reports are
`design/agent-R2-occurrence-fold-sol-1651-report.md` and the source-history
worker report. The requested `scratchpad/luna/reports/` directory itself is
absent in this environment.

No C0 request/reply contract, generated client, pin, guard, dependency,
Runtime source, or production caller was changed. The full C0 field/reply
surface therefore remains inherited and unmodified, but this proof does not
newly qualify full wire behavior.

## Limits and next step

This is bounded fold qualification only. The prior fold evidence still stops
at the later historical physical-storage scratch guard; it does not claim a
complete accepted/public redo. Recommended next step is the already-assigned
historical storage continuation by the sole R2 inverse owner, followed by an
independent review before any original public redo or full-body execution.


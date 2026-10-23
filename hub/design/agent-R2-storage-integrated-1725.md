# R2 storage integrated proof — `6531622c8f198c3efb509217e303fcad0126c47b`

## Verdict

**PASS for the bounded offline integrated proof.** No Agent source, test,
generated file, pin, dependency, or Git state was changed.

The exact integrated head is `6531622c8f198c3efb509217e303fcad0126c47b`,
tree `7c624ddd8ac897923ad85cf4520c905d64eb68a1`, with parents
`4ff762fda765bfa6c111fe571bed11ced03eae8b` and
`ccbb528dc19ddf67367bbfec08d9110a02adafc3`. The Runtime was explicitly
pinned to `/home/user/work/wt/rt-pin-d9e2a71e`, head
`d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, tree
`9b07545cac9a8bbafb16246aaa6f72050ef7cffe`.

Agent and Runtime worktrees were clean before and after. The post-run merge
delta from the first parent was exactly:

```text
M astrid/sdk/timeline/inverse.py
M tests/editing_conformance/test_captured_registry_redo.py
```

## Exact integrated test

Command, run once on this integrated head:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py
```

Result: **130 passed in 12.87s, exit 0**. No skip, deselection, or xfail was
reported.

Before and after imports resolved as follows (unchanged):

```text
Agent:   /home/user/work/wt/agt-R2-storage-integrated-1725/astrid/sdk/timeline/{inverse.py,_commit_patch.py,_root_inverse.py,_step_undo.py,commit.py,_commit_preview.py}
Runtime: /home/user/work/wt/rt-pin-d9e2a71e/runtime_protocol/{__init__.py,errors.py,timeline_commit_port.py,timeline_commit.py,timeline_commit_store.py,timeline_commit_provider.py,timeline_commit_execution.py}
```

## Storage and ancestry preservation

The two reviewed `ccbb` blobs are exact at the integrated head:

```text
astrid/sdk/timeline/inverse.py                            5567e57d3b60e8002faa4e261b5a23407206a5f0
tests/editing_conformance/test_captured_registry_redo.py  72637c7b80763aefb163e73e45df8ad3378ed68b
```

The seven-file 103-case predecessor from `63baa707b…` remains present. Five
files are byte-identical to that predecessor; the only two expected changes
are the reviewed storage correction in `inverse.py` and its retained registry
regression test. The six R1-private files remain present; the three private
capture tests and `_commit_preview.py` are byte-identical to `bac094180…`,
while the expected later R1/R2 integration deltas remain in `_commit_patch.py`
and `commit.py`. No predecessor file was deleted.

The integrated proof therefore preserves the strict alias/source identity,
order, membership, ABA, and contradictory-storage negative controls covered by
the retained tests. The separate storage review also established the exact
canonical digest `9c0d1b08599c0c0f8fb895c65a18bca29ca3dab4fff8c21307032fadb882b312`
and 47 tamper/current-audit controls.

Relevant source SHA-256 values were identical before and after the proof:

```text
astrid/sdk/timeline/inverse.py                              626f26805c406081ad034af73459c85e350cbaeeba3bddc2021f1eb5f97a72ab
astrid/sdk/timeline/_commit_patch.py                        b971050c92b14304bbc037ed775ddb7ddfa6cf5a233cd2075f92ba68725c3163
astrid/sdk/timeline/_root_inverse.py                        0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a
astrid/sdk/timeline/_step_undo.py                           206f13ac5991ed6abecbc0b1fbde24f2526cb3bf2f47f57f9b91c66aa43fa1dc
astrid/sdk/timeline/commit.py                               a4d612aeadfd66011258b9003d3b7d9a4f33c4fa387c50b65bf4fa79bafb4e91
astrid/sdk/timeline/_commit_preview.py                     70ad40a78248805bee83fe0261145b7e0c3b470ebb770f5f78526900a42dfce5
tests/editing_conformance/test_captured_registry_redo.py    5881d8d48fa3c5dffb605d7a3f67fb9924b474ca4003577265c6c7688d731dbd
tests/editing_conformance/test_captured_nested_redo.py      d7567b519698bd9ae36b44f1747ad26dd0e394dd7f1cdaaf3b83866ed2b7f8d4
tests/editing_conformance/test_inverse_stage_images.py      2365ad33012766f7531077f0608308d458452b57d210c85654b725b2584da338
tests/editing_conformance/test_step_undo_v2.py              30788f581da21db7099f3c7adb746a4d4312cbcc6f9b302967ed095696fb61a8
```

## C0 boundary

No request/reply or production-caller files changed. The preserved C0 request
continues to carry `api_version`, project/timeline, exact base pair, commands,
label, per-step `id`/`label`/`intent`/`tags`/`command_ordinals`/`patch`/`reads`,
`merge` (`fields` or `atomic`), declared reads, idempotency key, dry-run,
source, rationale, and group ID. The accepted/merged replies retain canonical
documents, receipts, records, bindings, effects, dependencies, history, and
undo steps; preview retains required `would_status`; structured failures retain
code/path/head/hint/suggested command.

## Scoped checks

All checks below passed on the current integrated source:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=<private-temp> /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py --cache-dir <private-temp> --hide-error-context --no-pretty
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

The first Ruff attempt used the harness `tmpdir`, which is a regular file;
that cache initialization failed without touching source. Ruff was rerun with
a private `mktemp` cache and passed. Mypy reported no issues in two files;
vendor lock reported `ok runtime.lock.json`; artifact manifest reported
`artifacts.json is current`.

Previously completed evidence on the exact reviewed storage tree is reused,
not represented as a new run: Ruff baseline **2149/2149**, Mypy baseline
**1912/1912**, vendor lock, artifact manifest, and diff check all passed. The
causal `64e7c59e1…` old-source regression remains the expected historical-
aggregate RED result. See the independent review:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-storage-review-1717.md`.

## Limits

This is an offline Agent-provider proof only. No public/live Runtime redo,
original public redo, full suite, browser, socket, daemon, native-14, C271,
P1/P4, or manual environment provisioning was run. The separate
legacy-validation author task remains live and is not claimed here. The C0
request/reply shape and production caller were not edited; this proof does not
add a claim beyond the focused tests and retained review evidence.

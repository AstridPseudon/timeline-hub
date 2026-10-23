# G5 restructure hydration review — bounded PASS, whole G5 still blocked

## Decision

The bounded caller-hydration change from Agent `052e148539828cdf44d36029074bab225e21de31`
against `77ab3908fbf827fd591f077a3ef00664c073409d` passes independent review.
It is limited to the permitted `publish.py` callsite plus six fixture controls. The
exact-current-closure guard is unchanged. This is **G5 DRAFT ONLY / P1 NO-GO**;
the overall normal restructure path remains blocked by the already-known native
helper pin-shape incompatibility before submission. That issue is outside this
review and already has its separate Sol/C0 ownership; it is not a new scope gate.

## Source review

The only source change is the hydration immediately before the existing guard in
`astrid/sdk/timeline/publish.py`:

```python
original = _store.fetch_bundle(
    project, timeline,
    revision_id=local["base_parent"]["revision_id"],
    publication_id=local["base_parent"].get("publication_id", state["base"]["publication_id"]),
    client=client,
)
local["base_parent"] = {**original["base_parent"], **local["base_parent"]}
local["source_mapping"] = {**original["source_mapping"], **local["source_mapping"]}
```

This binds the caller's original revision, paired with its existing local
publication when present, otherwise the current matching outbox receipt. The
existing public `open_bundle` route validates the exact scope and revision,
retains the pinned parent/shot/internal closure, checks the publication's
receipt against the requested revision, and verifies the receipt canonical
document against the reconstructed closure. There is no historical-to-current
revision substitution, digest waiver, provenance stripping, unknown-provenance
overwrite, or private-cache injection.

The merge order preserves every existing local value, including an intentionally
wrong digest, wrong pair, or local source metadata. Therefore those values still
reach the unchanged guard and refuse rather than being repaired silently. The
existing comparison remains:

```python
if (local["base_parent"] != base["base_parent"]
        or set(local["shots"]) != set(base["shots"])):
    raise TimelineEditError("restructure requires its exact current closure; reopen the timeline")
```

The production request construction remains unchanged, including the v2 base
pair, commands/select/args, label, per-step id/intent/tags/patch/read ordinals,
merge, reads, idempotency key, dry-run/source/rationale/group ID, and structured
accepted/merged/preview/conflict/invalid reply handling. No schema, generated
file, pin, contract, dependency, guard, executor, or shared install changed.

## Fixture controls

The six fixture controls are the new exact-current preflight, four caller refusal
cases (`digest`, `pair`, `historical`, `scope`), and the public reader authority
control. They assert no Runtime calls, unchanged history/head, unchanged
canonical document, and unchanged SQL store dump on refusal. The successful
preflight stops at the real guard with a test-only sentinel, after asserting
`local == base`, canonical-document equality with the accepted receipt, and the
matching publication receipt ID. The original inverse behavior body remains
byte-identical.

The immutable inverse-body SHA-256 is unchanged in both parent and reviewed
source:

```text
c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d
```

## Evidence

Agent source identity:

```text
commit 052e148539828cdf44d36029074bab225e21de31
tree   5fecdabcb0eff53a9329779073caf77772116f74
parent 77ab3908fbf827fd591f077a3ef00664c073409d
```

Pinned Runtime identity used by the controls:

```text
commit 3b926efab2eed122d374540baee297d4cdcec62a
tree   b794170504544b259781e50d7ca4d61b6729e67c
```

Exact commands and results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
-o tmp_path_retention_policy=all -p no:cacheprovider --timeout=30 \
--basetemp=/tmp/agt-G5-restructure-hydration-review-1335-fixture \
-k 'fixture_' tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 6 passed, 1 deselected in 37.76s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
--collect-only tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 7 tests collected

/home/user/work/venv-agent/bin/ruff check --no-cache \
tests/sdk/test_timeline_restructure_guarded_runtime.py
=> All checks passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m mypy \
--cache-dir=/tmp/agt-G5-restructure-hydration-review-1335-mypy \
tests/sdk/test_timeline_restructure_guarded_runtime.py
=> Success: no issues found in 1 source file

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/publish.py
=> Same two pre-existing diagnostics as parent: I001 and E741;
   normalized code/message identity confirmed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m mypy \
--cache-dir=/tmp/agt-G5-restructure-hydration-review-1335-mypy \
astrid/sdk/timeline/publish.py
=> 19 pre-existing attr-defined diagnostics; same normalized diagnostic set as
   the 1319 private baseline/current comparison

git diff --check 77ab3908fbf827fd591f077a3ef00664c073409d \
052e148539828cdf44d36029074bab225e21de31
=> pass
```

The first attempt to run the six controls used the harness `tmpdir` path, which
is a regular file in this worker, so pytest setup failed before collection. It
was rerun with the private `/tmp` basetemp above and produced the result claimed
here. No product code was edited during this review; the worktree is clean.

## Not run / not claimed

No full suite, HTTP/P1/P4, browser, native14/58, D17, original inverse/503
body, daemon, dependency installation, Git mutation, or normal full restructure
helper run was performed. The normal helper's known failure is the native
two-field pin comparison against the authenticated three-field
`revision_id`/`publication_id`/`content_digest` base pin, before restructure
submission; this review does not relax or repair it.


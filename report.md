# P4 genesis prerequisite diagnosis — BLOCKED

Base: `0afe4e082fd01fc7ffbff469b842538dc21fa50b`, tree
`41b002d59bcbcca0840a774b2bb8b7620e4c92f4`.
Runtime: `34eac0041b0891e9011966b39bcbd26053fde5bc` at
`/home/user/work/wt/rt-pin-34eac004` (the unchanged Agent lock).

No test or product source changed. Only this report changed in the worktree.
The exact ten-note positive, ten commands/one commit, per-step undo/redo,
mirrors, authored closure, show/history, restart, publisher assertions and
Runtime call-observation boundary remain unchanged. No pin, helper, schema,
launcher, suite, generated file, dependency or authentication change was made.

## First missing dependency, checked against retained service29153 data

The existing service result is **1 failed before any edit**, at
`TimelineCommitStore._validate_closure:660`. Its log is
`$ORCH/tests/ap2-P4-ten-seed-return-0507-p4-v2-http-nodes-1023051513-29153/log.txt`.
This worker did not rerun it.

The concrete missing physical object is
`sha256:1111111111111111111111111111111111111111111111111111111111111111`.
It is the literal `MEDIA` in
`tests/sdk/test_timeline_commit_provider_document.py:19`, referenced by the
parent/internal `registry.assets.picture.media_id` and shot items' `media_id`.
The trusted seed helper includes this exact pin in its media manifest.

Opened the retained database read-only (`mode=ro&immutable=1`):
`/tmp/pytest-of-root/pytest-4/test_http_ten_note_commit_per_0/realm/realm.sqlite3`.
Project: `dbd7ab9f6b4b4ca6a4b426fbbf714ac0`. The exact line657 managed-object
join returns no row; `objects` has zero rows and this project's
`project_objects` has zero rows. The exact CAS path under
`realm/cas/sha256/11/` is absent too. No retained files were modified.

The brief's missing-child-image hypothesis does not explain this first
failure. The reconstructed seed contains two shot images and two internal
images, with matching occurrence edges, internal links, manifests and payload
digests. Runtime's existing `_persist_closure` inserts internal images before
shots and parent after validation; it does not require every new revision
image already to be persisted. Adding revision seed calls cannot satisfy the
missing managed media object.

## Supported insertion API and owner need

The existing supported prerequisite API is `RuntimeService.ingest`, used by
`seed_shared_occurrence_parent`. An insertion preserving this pin would need:

```python
runtime.service().ingest(
    runtime.project, original_media_bytes,
    expected_digest="sha256:" + "1" * 64,
    idempotency_key="p4-ten-note-source",
)
```

This call was **not executed or added**: there are no original media bytes in
`document_fixture`, only the literal synthetic digest. `ingest` delegates to
`stage_object`; CAS computes SHA-256 over supplied bytes and rejects a digest
mismatch (`service.py:4843–4867`, `cas.py:79–82`). Closure validation then
independently hashes the installed bytes (`timeline_commit_store.py:662–664`).
No supported trusted fixture API was found that installs this arbitrary fixed
identity without matching bytes. A fabricated object row, staged digest,
authentication or validation bypass would violate the brief. The neighbouring
shared seed helper ingests different bytes and replaces all media pins, also
explicitly forbidden here.

Owner need: provide the original bytes matching the required pin, or issue a
separately authorized fixture prerequisite correction. No exact successful
trusted insertion call can honestly be reported with the supplied data.

## Independent fidelity finding

The inherited compiler seed also fails the required same-child invariant
offline. The original `occ-a` and `occ-b` reference one `chapter-shot/shot-1`.
After the unchanged `_seed_original` compilation, there are two distinct
`shot-placement-*` shot identities and two distinct internal revision IDs.
The original positive still requires equal placement `shot_id` values at
line137. This contradicts treating the prior compiler/registry seed as a
faithful shared-child genesis. It was not repaired by changing closure edges,
substituting fixtures, or relaxing the assertion. The owner must resolve this
in the authorized shared-closure preparation after the physical source issue.

## Commands and results

Successful collection command (no fixtures/body executed):

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-faf69ab833 PYTHONPATH=/home/user/work/wt/ap2-P4-ten-closure-sol-0517:/home/user/work/wt/rt-pin-34eac004 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
```

**PASS**, exactly 1 test collected in 0.49s; existing unknown `timeout` option
warning. An initial collection attempt omitted Runtime from `PYTHONPATH` and
exited4 during conftest import; adding the exact pinned Runtime path fixed it.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-faf69ab833 ruff check --no-cache --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-faf69ab833 mypy --config-file pyproject.toml --no-incremental --cache-dir /tmp/w-faf69ab833/mypy-cache astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py
git diff --check
git diff 0afe4e082fd01fc7ffbff469b842538dc21fa50b -- tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/helpers/trusted_seed.py
```

**PASS**: Ruff; mypy (4 files, two annotation-unchecked notes); diff whitespace;
empty test/helper diff. Initial `python -m ruff` and `python -m mypy` attempts
found neither module in the shared test venv; existing `/root/.local/bin`
tools supplied the successful checks, without installing anything.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-faf69ab833 PYTHONPATH=/home/user/work/wt/ap2-P4-ten-closure-sol-0517 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python /tmp/w-faf69ab833/closure_witness.py
```

**PASS as a diagnostic, not an acceptance witness**. Uses the actual compiler,
existing trusted helper `_closure`, Runtime digest function and read-only
retained SQL. Confirms image digests/closure edges and empty mirrored note
genesis; explicitly records `original_child_count=1`, `compiled_child_count=2`,
`same_child=false`, managed media absent. The initial stronger same-child
assertion failed and exposed the inherited fidelity issue. Scratch output:
`/tmp/w-faf69ab833/closure-witness.json` and `compiled-closure.json`.
The worker `tmpdir` file resolves to `/tmp/w-faf69ab833`.

No service, HTTP, sockets, body, full suite, browser, build, or central-test
request was launched. Authentication and accepted Runtime persistence remain
unverified. Full C0 request/reply/steps/dependencies/history/conflict/invalid
coverage and production callers were not changed or newly qualified.

## Next step

Independently review this diagnosis; resolve the exact source bytes and shared
identity preparation through the owner. Do not spend the manager's one
original-node retry on the unchanged failing seed. No P4/H3 completion claim.

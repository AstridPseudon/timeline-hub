# Independent P4 scoped source/fidelity review — source PASS; acceptance BLOCKED

## Review verdict

Reviewed candidate commit `3696239c48f9705568af30f2704855cc6a9175e5`
(`94f7f4ff4d60a798d9cd664638a2b182234ad82c`) against its same-branch base
`0afe4e082fd01fc7ffbff469b842538dc21fa50b`
(`41b002d59bcbcca0840a774b2bb8b7620e4c92f4`), PLAN §3 P4, and C0c §§2/4/5.

**Source review: PASS. Acceptance: BLOCKED. No P4 GO.** The correction is
bounded to genesis setup and does not alter the original P4 assertions. The
remaining blockers are genuine reader/projection seams, so this review does
not request an HTTP/body rerun and does not change source assertions.

## Scope and fidelity

- `git diff --name-status HEAD^ HEAD` reports only this report and
  `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.
- The original fixture, `cases.json`, and all ten-note assertions are unchanged;
  `_note_values` through the end of the test are byte-for-byte identical to the
  base. The changed setup removes `compile_authoring_candidate`, performs no
  compiler materialization, and routes bytes through the existing
  `RuntimeService.ingest` API.
- `tiny.png` is exactly 69 bytes with SHA-256
  `b1ff9c8ea3a780bad09b346c423d2d0e46815926879b18e841d928376a946640`.
  The setup asserts the returned `object_id == digest == sha256:<hash>`,
  `relation == managed`, and the observed size, then uses that digest in all
  three original `media_id` locations. The reverse map and full encoded source
  equality assertion preserve types, null/absence, ordering, opaque fields,
  timing, and identity.
- The original two occurrences remain exactly
  `chapter-shot/shot-1`; the sole internal image remains
  `chapter-1/internal-1`. The unchanged trusted setup helper receives that
  canonical closure. The only new owner operation is the normal
  `RuntimeService.create_timeline(project, "chapter-1", ...)` call required for
  Runtime admission. No new compiler fork, direct store mutation, auth bypass,
  product/client/schema/pin change, or assertion weakening is present.

The unchanged body was reviewed for the full C0 v2 surface: base revision and
publication pair; commands; label; ten per-step patches; declared reads;
`fields` merge and reads; dry-run/key assertions; accepted and merged reply
shapes; canonical head/document digest; receipt; step dependencies; history,
conflict, rerun, invalid/refusal, inverse and redo assertions. It remains
unexecuted in this review. The production caller is real: `timeline.open` →
`fetch_bundle` → `RemoteTimelines.open_bundle`.

## Independent seam classification

1. **Working aliases versus physical closure: genuine projection seam, not a
   C0c failure.** C0c §2 requires each root alias to resolve to exactly one
   physical closure image; two occurrences pointing at one image count as one,
   and entity IDs are aliases rather than physical identity. It does not require
   authoring working aliases to be equal. The current adapter intentionally
   derives occurrence-specific `shot-placement-*` IDs in
   `astrid/core/timeline/authoring_bundle.py:218–228,413–456`, while its
   `source_mapping` retains one `chapter-shot/shot-1` image. The offline witness
   reproduced two distinct working placement IDs and one physical source image.
   The unchanged positive at test line 196 compares the working IDs, so it
   cannot pass on this faithful closure. Preserve the shared physical boundary;
   the eventual positive should use a physical-boundary/source-mapping oracle
   if that is the accepted contract. Do not retarget product identity or weaken
   the positive solely from the earlier report.

2. **Internal read scope: genuine owned production-path bug, not unused code.**
   `timeline.open` calls `fetch_bundle` (`astrid/sdk/timeline/store.py:641–651`),
   which calls `open_bundle`; after reading the parent and shot, the reader
   requests `get_project_timeline_revision(project_id, timeline_id,
   internal_revision)` at `astrid/sdk/_remote_timeline.py:73–89`. For this
   faithful case that sends `film`, but the immutable row is owned by
   `chapter-1`. Pinned Runtime enforces the owner in
   `runtime_protocol/service.py:2312–2317` with SQL predicates on
   `(project_id, timeline_id, revision)`, yielding `internal timeline revision
   not found` for `(film, internal-1)`. The same incorrect parent scope exists
   in `astrid/sdk/authoring_revision_diff.py:56–64`. Creating `chapter-1`
   correctly fixes seed admission, not this read. The candidate report’s
   `_validate_closure` lines 607–614 citation is stale; the pinned source
   enforcing this owner is `_record_internal_revision:1410–1416`.

## Evidence and limits

Commands run offline in this worktree:

```text
stat -c '%s bytes %n' tests/packs/builtin/generate_image/fixtures/tiny.png
sha256sum tests/packs/builtin/generate_image/fixtures/tiny.png
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python - <<'PY'  # pure _original_publication → _closure → bundle_from_document witness
PY
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... ruff check --no-cache --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... mypy --config-file pyproject.toml --no-incremental --cache-dir .../mypy-cache tests/editing_conformance/test_p4_ten_note_v2_runtime.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py
git diff --check
```

Results: 69 bytes/hash matched; offline witness PASS; exactly one test
collected (existing unknown `timeout` warning); Ruff PASS; private mypy PASS
(the two existing unchecked-body notes); diff check PASS. An initial witness
attempt lacked the Runtime PYTHONPATH and failed at import only; the corrected
offline witness passed. No HTTP, socket, service instantiation/call, test
body, central test request, browser, build, full suite, or unchanged rerun was
run. Therefore ingest persistence, authenticated readback, accepted/merged
live replies, history, and inverse/redo remain unverified.

The prepared source is review-ready, but acceptance remains **BLOCKED** on the
working-identity oracle/adapter decision and the Agent reader owner-scope fix.

---

# Candidate handoff — correction prepared; acceptance BLOCKED

Base: `tl/ap2-P4-ten-seed-return-0507` resolves exactly to
`0afe4e082fd01fc7ffbff469b842538dc21fa50b`, tree
`41b002d59bcbcca0840a774b2bb8b7620e4c92f4`.
Unchanged Runtime lock: `34eac0041b0891e9011966b39bcbd26053fde5bc`, inspected at
`/home/user/work/wt/rt-pin-34eac004`.

## Change and decisions

Changed only the genesis setup/imports in
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py` (new blob
`56a8f80e16834c6d5da02ddf8a8a3e1dc5a15026`).

- Ingest the existing 69-byte PNG at
  `tests/packs/builtin/generate_image/fixtures/tiny.png` using the existing
  `RuntimeService.ingest(project, data, media_type=, original_name=,
  expected_digest=, idempotency_key=)` API. The bytes hash to
  `sha256:b1ff9c8ea3a780bad09b346c423d2d0e46815926879b18e841d928376a946640`.
  Setup asserts returned object ID and digest equal that computed hash,
  relation is `managed`, and size equals the supplied bytes; it uses the
  returned object ID for the cloned payloads.
- Exhaustively assert and map the original three payload `media_id` paths.
  Reverse that mapping and compare the entire encoded document to the original;
  this retains value types, null/absence, ordered lists, opaque fields, source
  references, timing and identities. The original fixture function/data are
  untouched. The existing two empty mirrored note containers remain the only
  authored genesis overlay.
- Pass the original canonical parent/shot/internal images to the unchanged
  `seed_trusted_parent`, whose existing `_closure` computes normal digests and
  the complete dependency manifest. The original registry envelope is already
  present; it is retained. No authoring compiler materialization is used.
- Keep both original occurrences pointing to exactly `chapter-shot/shot-1`
  and the single `chapter-1/internal-1` image, including `item-1` and all source
  links. Create the unchanged `chapter-1` owner through normal
  `RuntimeService.create_timeline` during fixture setup, because Runtime's
  `_validate_closure` requires that owner to exist (lines607–614). This avoids
  changing the internal source scope to `film` or inventing shot-scoped IDs.

Everything from `_note_values` through the end of the test is **byte-for-byte
unchanged** against the base. The exact ten notes, ten commands/one commit,
every per-step undo/redo, equal-shot positive, mirrors, full authored closure,
show/history, restart, publisher, request base pair/key/label/steps/patch/reads,
merge mode, accepted reply/head/digest/receipt/dependencies assertions remain.
Original fixtures/cases and trusted seed helper were also checked byte-for-byte.
No product/client/schema/pin, transport, auth, store, provider, suite, or
production caller changed. Existing C0 v2 accepted/merged/conflict/invalid and
production-caller coverage was preserved, not newly qualified by this task.

## Remaining exact product seams

**The prior seed-fidelity PASS is withdrawn. This is not a P4 acceptance PASS.**

1. Agent `astrid/core/timeline/authoring_bundle.py:218–228,413–418,446–456`
   deliberately assigns distinct `shot-placement-*` identities to repeated
   physical shots, using each occurrence ID. The real pure
   `bundle_from_document` on the corrected canonical closure still returns
   **two different working placement shot IDs and two working shot entries**.
   Both source mappings retain the one physical `chapter-shot/shot-1` and
   `internal-1`; the loss is in the working identity projection. Thus the
   unchanged positive at test line196 cannot pass even with perfect ingestion
   and canonical seeding. No edge rewrite, binding, alternative fixture,
   assertion change or new executor was added.
2. An earlier read obstruction is visible in the actual source: Agent
   `astrid/sdk/_remote_timeline.py:86` requests `internal-1` using the parent
   timeline ID `film`. Runtime
   `runtime_protocol/service.py:2312–2317` requires the stored internal's
   `timeline_id` to equal that request's timeline ID. The faithful image's
   owner is `chapter-1`. Creating its proper owner satisfies seed admission,
   but does not change this read mismatch. This is a source-level diagnosis;
   no HTTP read or service call was executed to qualify its live error.

These are outside the authorized test-genesis-only scope. The supported
canonical boundary preserves shared physical identity; the current production
reader cannot satisfy the original working-identity assertion. Do not spend
an original-node retry merely to rediscover these known seams.

## Exact checks and results

All commands ran in `/home/user/work/wt/ap2-P4-authentic-genesis-sol-0522`.
The worker's assigned `tmpdir` file names `/tmp/w-16c448f11f`.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-16c448f11f PYTHONPATH=/home/user/work/wt/ap2-P4-authentic-genesis-sol-0522:/home/user/work/wt/rt-pin-34eac004 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
```

**PASS**: exactly 1 test collected in 0.50s. Existing unknown `timeout`
configuration warning. No test fixture or body executed.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-16c448f11f ruff check --no-cache --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-16c448f11f mypy --config-file pyproject.toml --no-incremental --cache-dir /tmp/w-16c448f11f/mypy-cache tests/editing_conformance/test_p4_ten_note_v2_runtime.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py
git diff --check
```

**PASS**: Ruff; mypy, no issues in 5 files (two existing annotation-unchecked
notes); whitespace check. Shared dependencies were not changed.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-16c448f11f PYTHONPATH=/home/user/work/wt/ap2-P4-authentic-genesis-sol-0522:/home/user/work/wt/rt-pin-34eac004 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python /tmp/w-16c448f11f/genesis_witness.py
```

**PASS for offline canonical fidelity and diagnosis only**. Uses the changed
pure genesis constructor, actual trusted `_closure`, Runtime digest and
`validate_commit_value(..., 'CanonicalDocument')`, and actual Agent canonical
converters. Checks exhaustive three-payload/one-manifest media mapping,
every payload digest and manifest edge, exact two-to-one shared closure,
full encoded authored restoration, lossless canonical roundtrip, unchanged
original assertions/fixture/cases/helper, and actual service method signatures
via AST. Confirms **working_shared_identity=false**, without treating it as
acceptance success. Outputs:

- `/tmp/w-16c448f11f/genesis_witness.py`
- `/tmp/w-16c448f11f/genesis-witness.json`
- `/tmp/w-16c448f11f/canonical-closure.json`

No HTTP, socket, service instantiation/call, test body, central-test request,
full suite, browser or build ran. Actual ingest, accepted persistence, authenticated
readback, C0 reply/history coverage and live inverses remain unverified.

## Handoff

Independent review should confirm this bounded fixture correction and the two
reader seams. Manager must route the Agent/Runtime boundary work before its
one original-node retry can prove the unchanged positive. No unchanged rerun
was requested. The end-to-end objective is BLOCKED; the prepared correction
and exact evidence are ready for review. Commit message is supplied separately;
no git mutation, push, branch operation, dependency write or cleanup performed.

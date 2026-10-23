# P4 authentic canonical genesis — correction prepared; acceptance BLOCKED

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

# A4 parent raw witness independent review

## Verdict

**PASS — test-only witness is faithful and scoped.** The reviewed commit is
`258031478` on base `9a095a95178e0bb89ef3b2024d6502d47b35ac25`; its only path
is the 334-line addition
`tests/editing_conformance/test_a4_parent_media_raw_witness.py`.

The old App donor at `7f7e2daffad39a6d9aa3917a9fc526ba91caf2e6` and prepared
coverage at `76ed048ac` were read read-only. The current App checkout at
`2107e1870e51c650d59315f4cc1ab6af338f198c` retains byte-identical
`parentAfterAnchorCapture.test.ts` and implementation blobs (`346ae62e...` and
`2703ff50...`). Existing App implementation/tests remain KEEP.

## Exact new coverage

- Current registered `clip.add-media` accepts a complete literal parent row
  through the detached real-provider preview/accept boundary. The test checks
  JSON round-trip, exact row/mirror preservation, opaque/unknown values,
  explicit null effect fields, absent `at_ms`/`transition`, source-document
  immutability, created clip/asset IDs, media owner/track bindings,
  authoritative reads, and previous-value `ABSENT` writes.
- Missing/null `hold` is covered for raw video, raw image, and ordinary birth;
  all are current structured refusals with no write. Explicit null `track` and
  `asset` refuse without write; explicit null `effectId`/`effect_id` survives
  the accepted literal row.
- Duplicate source identity is created in both parent clip mirrors and refuses
  before write with `identity_conflict`.
- Submitted source `at_ms` and incoming `transition` are refused without
  normalization/drop, with the submitted values retained. Zero and positive
  `.01` duration are refused without flooring (the latter at current final
  timing quantization).
- Refusals assert structured status/reason/path/hint/suggested command and
  unchanged head, history entries, documents, and accepted state.

The old accepted → current refused cases are recorded honestly: the new tests
do not claim after-anchor clone/ripple parity or retirement credit. In
particular, old positive missing/null video-hold, positive subminimum floor,
and incoming-transition behavior remain uncovered as current accepted parity.

## Scope and retained limits

The provider evidence is intentionally detached `MediaRealm`/`DetachedPort`
evidence for the registered normal provider. It does not prove mounted App A2
`localSaveSession`, HTTP/Runtime transport, or whole old capture-envelope
parity. The old after-anchor source clone, rate-aware ripple, and its derived
writes remain uncovered here. No inverse/reload duplication, source/catalog
pin re-test, track/transcript operation, invented operation/API, schema/pin,
Runtime, or product change was made.

The witness asserts the relevant C0 subset: request controls (label, steps,
step patch/reads, merge, declared reads, source, rationale, group ID), preview
`would_status` with null receipt, accepted receipt/result, records, reads,
bindings, created claims, and `ABSENT` writes. Full C0 contract coverage
(canonical/merged replies, effects/dependencies/history/undo steps and all
request envelope fields) remains owned by the existing provider/contract
suites and was not duplicated or weakened.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_a4_parent_media_raw_witness.py tests/editing_conformance/test_recipe_m2_parent_media.py::test_exact_capture_replay_scoped_birth_and_inverse[video] tests/editing_conformance/test_recipe_m2_parent_media.py::test_provider_exact_reload_inverse_redo_and_retired_ids[False]
15 passed in 2.35s

RUFF_CACHE_DIR=$TMPDIR/agt-A4-parent-raw-review-1919-ruff-cache /home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_a4_parent_media_raw_witness.py
All checks passed!

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy tests/editing_conformance/test_a4_parent_media_raw_witness.py --hide-error-context --no-pretty --cache-dir=$TMPDIR/agt-A4-parent-raw-review-1919-mypy-cache
Success: no issues found in 1 source file
```

`git diff --check` passed. Diff against the requested base is exactly the new
test file. Agent product/R1/store/registry protected paths are unchanged from
base; the `d106dfe8...` schema blob is unchanged. Frozen App donor/current
parent-capture blobs are equal. Credential scan of the new file found zero
matches. No full, HTTP, browser, gate, or original-14 suite was run/requested.

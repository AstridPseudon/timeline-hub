# G5 native restructure pin compatibility — forward proof ready for inverse observer

**G5 DRAFT ONLY / P1 NO-GO.** The native two-key/three-key pin incompatibility
is repaired, with authentic public forward acceptance, preview, exact lost-ACK
retry, canonical readback and history proof against approved Runtime859.
The original whole undo body was **not run**. Its cause remains for the existing
Runtime observer's one instrumented diagnosis; no Runtime inverse defect or
undo/redo readiness is claimed here.

## Exact source and scope

- Agent worktree: `/home/user/work/wt/agt-G5-restructure-pin-sol-1335`.
- Parent commit: `052e148539828cdf44d36029074bab225e21de31`.
- Parent tree: `5fecdabcb0eff53a9329779073caf77772116f74`.
- Candidate tree: `ac1251cdc911b99d690d303cdd777fe14643bdb1` (computed from Git
  object encodings and the two changed files, without writing Git objects/index).
- Native source SHA-256 before:
  `1eaeac4793850098eccd1e0e9a38d5945fbe17681e926798fc16ea41d95d2712`;
  after: `800247535bbe034777fe84beb0612d96ea11992f8d77ad52ba7503dff56afb43`.
- Final focused test file SHA-256:
  `d7dc8942c49b4c464535280b8849520adfba4b67d4dc0560a5b68203abf7983b`.
- Runtime worktree: `/home/user/work/wt/rt-pin-8592822f`, commit
  `8592822fd11275540f596562f43c715676f2bc0f`, tree
  `ed9856f43a4e44a058bf2230badea2c4c7080050`.
- Vendored client pin remains `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Original whole inverse function source SHA-256 remains
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
  Complete function bytes, including terminal newline, equal the parent.

Only `astrid/sdk/timeline/native_restructure.py` and focused new tests in
`tests/sdk/test_timeline_restructure_guarded_runtime.py` changed. `publish.py`,
the original inverse body, all predecessor tests, Runtime, rebase/inverse/journal,
other writers, CLI, schema, generated files, pins, contracts and dependencies
are unchanged. No Git mutation was performed. Commit SHA is assigned by the
harness after exit; the exact candidate source tree above is available now.

## Decision and authority boundary

Read PLAN, report1319 and the Runtime1305 observer handoff first. A new test on
the unmodified parent reproduces the refusal at native_restructure.py's pin
comparison. The public exact-pair loader returns revision/digest plus authenticated
publication provenance, while the canonical immutable parent image has
revision/digest. Comparing those entire differently shaped dictionaries refused
the ordinary production caller before submission.

The repair accepts exactly the existing two-field pin or that same pin plus one
nonempty string `publication_id`. It compares **both exact revision and exact
digest** with the source image, retains project/timeline checks, and rejects
unknown fields. It never removes publication/provenance from the bundle and
does not fetch or substitute any head. Both supported pin forms produce equal
native command records; the input bundle and prepared pin/source mapping retain
the full metadata.

The pure preparer does not independently authenticate an opaque publication ID.
That remains the existing public exact-pair loader and actual provider/Runtime
request boundary's responsibility. The final call-event observer records the
complete bundle before the native handler, and the caller's real request and
evaluated head, without replacing methods or changing values:

| Native invocation | Content input | Publication authority |
| --- | --- | --- |
| Normal `Checkout.publish` preparer | Public exact-pair bundle with all three pin fields | Existing verified loader and unchanged exact-current-closure guard |
| Real preview provider | Runtime-loaded canonical bundle with two pin fields | Actual request base pair and identical evaluated head |
| Real accepted provider | Runtime-loaded canonical bundle with two pin fields | Same actual request base pair and evaluated head |

Source-backed enforcement remains Agent `commit.py`'s `port.history_entry` pair
check and `execute(..., commit_request=request, evaluated_head=base/current)`,
plus Runtime `timeline_commit_store.py`'s scoped `_check_context` publication /
revision check and `_check_head` exact-pair CAS. The recorder still captures the
whole timeline dependency. The request negative controls below exercise this
actual service path, rather than treating pure preparation as authorization.

## Final public proof and no-write controls

The new forward fixture runs the same accepted `inverse-name` naming edit and
ordinary detached `Checkout.open(...).publish(..., restructure=True)` path as
the original journey. A generated-boundary proxy first forwards an exact copy
as a real dry-run request, then forwards the original request and loses its ACK
after acceptance. A fresh checkout retries through the existing durable session.
The accepted requests, idempotency keys and complete replies are equal. History
grows from 10 to 11 entries, with exactly one cut publication. Narration media
is refused by the same bounded test seam used in the original journey so this
proof isolates one restructure publication; it does not qualify narration.

Final actual before pair:
`authoring-parent-revision-3e61b61d70dfe5c94d857cd1fa6e6b1348dc744696f833961c8e3c766b81ae6c`
/ `txn-4c7df61153444fd59dd8e003c048b068`.
Accepted pair:
`authoring-parent-revision-a9ee17ada347061b9b658032a1c95adb0b7c5025da2f2136a4d277120f6220dd`
/ `txn-9ddabb6764e74fb3bf6c36695cb3c831`.
Canonical document digest:
`sha256:056c7b7a7d3415d802fa3d10c2e64e627ef7a978b4e93522aa5ed19067015f97`.

Preview has no receipt, reports `preview/would_status=accepted`, and leaves
complete history, canonical readback and SQL dump unchanged. Its full canonical
document and digest equal the actual accepted result. The forward result retains
three distinct shot/internal revisions, equivalent film content, and opaque
authored null/list data. Full request shape, semantic select/args, commands,
label, step IDs/intents/tags/patches/ordinals, atomic merge, declared reads,
source, key and dry-run are asserted. Preview also carries rationale/group ID.
History's receipt, previous exact pair, source, reads, accepted steps, computed
step patches/dependencies, records, bindings, writes and `undo_of/undo_steps`
are checked and retained in the full capture. Actual production absence of
optional rationale/group ID is preserved. No reply or request field is filtered.

The final ten focused cases include all six unchanged predecessor cases and:

- Native exact revision, digest, project, timeline, unknown-key, malformed
  publication and altered source-image negatives; no input/store/history writes.
- Actual Runtime request wrong revision, wrong publication, cross-scope,
  forged captured content digest and invented source-document argument controls;
  each raises a typed Runtime error with unchanged full canonical/history/store.
- A real A→B→A sequence of ordinary commits restores the **entire exact canonical
  document**. Its newer publication differs. The original restructure request
  still refuses, with unchanged canonical/history/store during that refusal.
- Forged **current** immutable parent payload under its original revision/digest
  fails the public pair loader with `protocol_error`; normal publish refuses at
  session opening's digest verification, with zero new calls/history/store writes.

The predecessor legitimate closure preflight still crosses the unchanged guard
with `local == base`, then stops read-only at the existing test sentinel. Its
full capture is retained separately from the unrestricted forward evidence.
Wrong detached digest, wrong publication pair, historical checkout after a real
advance, wrong timeline scope and exact historical reader integrity controls all
still pass. No closure, source cache, SQL state, read claim or executor is forged
to make a positive case pass. Negative tampering only tests actual refusals.

Merged/conflict/invalid reply contracts are untouched, not newly qualified here.
Typed request refusals are tested; no broad merged or conflict journey is claimed.

## Exact commands and results

All pytest commands used this literal prefix from the Agent worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o tmp_path_retention_policy=all -p no:cacheprovider --timeout=40
```

Suffixes and report-all results (each node is in
`tests/sdk/test_timeline_restructure_guarded_runtime.py`):

```text
--basetemp=/tmp/w-0bdae42539/red tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_native_restructure_accepts_only_known_exact_pin_fields
  1 failed in 8.08s: expected source-causal RED at original native guard.
--basetemp=/tmp/w-0bdae42539/green tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_native_restructure_accepts_only_known_exact_pin_fields
  1 passed in 8.68s: same test after bounded pin fix.
--basetemp=/tmp/w-0bdae42539/forward tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_public_restructure_preview_forward_and_exact_retry
  1 failed in 33.12s: new test used obsolete WorkspaceClientError constructor; corrected only this new test.
--basetemp=/tmp/w-0bdae42539/forward2 tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_public_restructure_preview_forward_and_exact_retry
  1 passed in 34.72s: unrestricted public forward/preview/exact retry.
--basetemp=/tmp/w-0bdae42539/authority tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_restructure_request_authority_and_same_byte_stale_refuse_without_writes
  1 passed in 9.91s.
--basetemp=/tmp/w-0bdae42539/final -k fixture_ tests/sdk/test_timeline_restructure_guarded_runtime.py
  2 failed, 8 passed, 1 deselected in 104.71s: global line tracing hit 40s; forged-current negative expected a later refusal seam.
  Corrected observation to call events only; corrected assertion to the actual earlier digest-verification refusal.
--basetemp=/tmp/w-0bdae42539/final2 -k fixture_ tests/sdk/test_timeline_restructure_guarded_runtime.py
  10 passed, 1 deselected in 75.85s on final source.

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/native_restructure.py tests/sdk/test_timeline_restructure_guarded_runtime.py
  All checks passed!
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-0bdae42539/mypy-final astrid/sdk/timeline/native_restructure.py tests/sdk/test_timeline_restructure_guarded_runtime.py
  Success: no issues found in 2 source files.
git diff --check
  PASS.
```

There were no suppressions, skips, weakened existing tests or baseline changes.
The one explicitly deselected test is the original inverse journey reserved for
the observer, not a replaced or expected-to-fail behavior test. No full suite,
P1/P4, HTTP/native14/58, D17, browser/54, daemon, live sockets, dependency install,
Runtime patch, original undo-body execution or body retry was run.

## Durable evidence and return to Runtime

Evidence directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-pin-sol-1335/evidence/`.

It contains all run logs above, `source-evidence.json`, `forward-summary.json`,
the full `public-forward.json` (actual public reads, generated reader arguments,
native input bundles/request/evaluated heads, requests/replies, canonical before
and after, complete history, naming receipt and actual module origins), and
`closure-preflight.json`. Large captures remain outside design/ and the repo.
The harness-designated scratch location is `/tmp/w-0bdae42539`, as recorded in
this worker's `tmpdir` file; durable copies above preserve the evidence.

Return this exact candidate source to the existing Runtime observer described in
`design/handoff-runtime-G5-inverse-boundary-diagnosis-1305.md`. The two proven
pre-submission blockers are now repaired and forward proof is genuine. The next
step is **one** instrumented normal-service invocation of the byte-identical
`test_restructure_whole_inverse_redo_and_intervening_overlap_refusal`, with the
observer preserving all request/provider/port arguments and exceptions. This
worker did not spend that invocation, diagnose the old 503, or alter the body.
No remaining blocker to this bounded pin-repair task; G5 remains draft-only and
P1 remains NO-GO pending the separate inverse diagnosis and broader acceptance.

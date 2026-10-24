# R2 whole-path read-only investigation

Date: 2026-10-24 UTC. No product or test source was changed and no body was
rerun. The required retained-original invocation was allowed to finish.

## Exact identities

- Agent tree: `3b2db4bdf9014de013338521dd038ebdecd25f02`.
- Runtime checkout/head: `e89eb8c7dfa8cb2c451653ab200dbf77df28b173`.
- Current Runtime source SHA-256: `timeline_commit_auth.py`
  `75f5141cadebafc9f887f5968f39f0ff030d1b2e6c724c24de0bd10b94cde2f0`;
  `timeline_commit_store.py`
  `a2db29e4dbb5ef781d818690647e888b4eb02550c93a3e3d962df161d610d4cd`;
  `timeline_commit_validation.py`
  `c4b2143f151db766738eebd330983a8037a9a9fc8627b93303f26a59bbc53115`;
  `timeline_commit_port.py`
  `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b085c`;
  `service.py`
  `94591ec2924b940eccb8deb87ec8c8d3913d803399b1a9737108eee78d0f542c`;
  `store.py`
  `4bb37ed4a77b36ffe66d367388c75ae00c2ce09cb223be6c7e398fab132da2c0`.
- The original worker's preflight recorded the exact reviewed PARAM donor:
  `_selected_param_authority.py` `86f4c4154ecb4e2dd26770a04c35c6285e67c067621e628e2cb0026bafdfcfdf`;
  `test_selected_param_neutral_stage.py`
  `fb9aa03b356bdfe5a51c93be06dd62ca2826be122ffd3a0874101d17885c9657`.
- Retained original files are byte- and AST-identical before/current:
  `tests/core/test_timeline_element_publication_runtime.py` bytes
  `c331dcfd930544ff699674c31d7867d8da5d852d22e72f3ebcb335aabe55c79a`, AST
  `d44612f8c7778a8cefc10b99e9fb0aabe91d9c0f91fbd0954660333a840519bb`;
  `tests/sdk/test_element_inverse_source_retention.py` bytes
  `616b2b9d3a90963d95c735747ddd48410d3a8d2bea6be5c678d3e66cf42e2694`, AST
  `9ae7fba786e0545b5b3cbf28807af9df0e520088802093e8f245da56ed158ddf`.
- Full preflight source/blob records remain in
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-finite-walk-originals-1929/evidence/preflight-identities.txt`.

## Retained-original terminal, lossless membership

Evidence files:

- XML SHA-256 `26f43b0a3e43e214c5b8f12ac5a229bde992a8b830d4634fd3042c1a1a810fc3`.
- Log SHA-256 `4badeb633f3a241acd7da37c9cc94bd359d9374c958910008ef89481e645c722`.
- Command SHA-256 `60c6a8687fe23d8d52da7b7dff5d66bd922da34ae129ecc5415944be62026e29`.
- Source evidence directory:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-finite-walk-originals-1929/evidence/`.

The exact command was pytest with `--timeout=45`, the four literal original
nodeids, the normal `venv-agent`, `PYTHONPATH=$PWD:/home/user/work/runtime`,
and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`. It exited 1.

| nodeid | outcome | duration | terminal frame / mapping |
| --- | --- | ---: | --- |
| `test_public_helper_restart_exact_retry_later_head_inverse_redo[False-None]` | FAIL, timeout | 45.007s | `history_entry:460 → _verify_accepted:254 → _inverse_stage_history:872 → history_entry:460 → _verify_accepted:254 → _historical_sequential:362 → validate_sequential_capture:2497 → _capture_records:2372 → validate_commit_value:141 → jsonschema` |
| `test_public_helper_restart_exact_retry_later_head_inverse_redo[False-public-element]` | FAIL, timeout | 45.007s | `history_entry:460 → _verify_accepted:254 → _inverse_stage_history:872 → history_entry:460 → _verify_accepted:261 → _historical_sequential:331 → validate_commit_value(prepared, PreparedCommit):141 → jsonschema` |
| `test_public_helper_restart_exact_retry_later_head_inverse_redo[True-None]` | PASS | 42.886s | no failure frame |
| `test_public_helper_restart_exact_retry_later_head_inverse_redo[True-public-element]` | PASS | 42.950s | no failure frame |

Suite result: `2 failed, 2 passed in 178.47s`; JUnit suite time `178.459s`.
The two failures are exactly the changed-revision (`same_revision=False`) pair;
the same-revision pair passes. The terminal frames do not prove that PARAM
authority resolution is the failing operation.

## Authentic PASS controls and counts

- Genuine Runtime whole-restore control `tests/test_timeline_inverse_sequential_authority.py::test_inverse_sequential_scope_round_trip[v2-whole-restore]`:
  `1 passed in 6.87s` (XML testcase `6.344s`, process `6.864s`). Profile
  SHA-256 `06e38f8810c7039528b385c8d203ee7b07d7f5d72ed41d1f4e77795e84d4e8d7`.
  The profile records Runtime head `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f`,
  not the current `e89eb8c7…`; its counts are therefore a historical authentic
  control for call-shape/multiplicity, not a current-source timing claim.
  Authentic profile counts: `store.history_entry` 258; max recursive depth 6;
  `_verify_accepted` 254; `store._inverse_stage_history` 259;
  `auth._inverse_stage_history` 106; `auth._capture_records` 106;
  `auth._capture_document_images` 212; `Recorder` validation 106;
  `PreparedCommit` validation 55; `CanonicalDocument` validation 212;
  `json.loads` 6,299; digest 3,136; canonical JSON 5,696.
  Per-publication history counts were 11 (`publication-001`), 67
  (`publication-002`), 170 (`publication-003`), and 49 (`publication-004`).
  The profile records 153 store inverse-stage requests for publication-003 and
  6 for publication-004. This is direct evidence of recursive accepted-history
  revalidation, not merely a finite-JSON walker cost claim.
- Genuine P4 service `agent-p4-current-becfe-http-3legs-1024174105-16328`:
  CLI/sheet PASS `3.013s`; conflict/rerun PASS `12.386s`; ten-note path FAIL
  `45.336s`; aggregate `1 failed, 2 passed in 63.58s`. Its authentic report
  records 54 `CanonicalDocument` validations, 2 `Recorder` validations, 56
  finite-JSON checks, and the stack ending at `_capture_document_images` on
  `validate_commit_value(..., "CanonicalDocument")`, with `fps` as the shown
  schema instance. This is a different P4 path; it is not asserted to be the
  same cause as the R2 original timeout.
- Strict PARAM/source-retention controls on the exact donor2 carrier: `99
  passed, 1 warning in 49.74s`; XML suite time `49.731s`. This qualifies the
  selected-PARAM custody path only and does not qualify the original gate.

## Source call graph and line citations

1. Agent `TimelineSession._flush` builds the complete frozen request body and
   sends `client.timelines.commit(...)` at `astrid/sdk/timeline/sync.py:525-558`.
   `TimelineSession.commit_many` freezes label/steps/merge/reads at
   `sync.py:313-369`; publication undo is an ordinary inverse request at
   `sync.py:422-462`.
2. The Agent provider loads the exact base and target closures at
   `astrid/sdk/timeline/commit.py:1227-1261`, obtains accepted records at
   `commit.py:1284-1299`, then calls the Runtime port at `commit.py:1421-1444`.
   The exact selected-PARAM authority resolver is called only while recovering
   inverse element sources at `commit.py:528-567` (and during schema
   resolution at `commit.py:573-658`).
3. Runtime's production door validates the request/path and enters the
   coordinator at `runtime_protocol/service.py:2435-2502`; its port accept
   invokes store acceptance at `timeline_commit_port.py:650-662`.
4. Runtime accepted-history verification is `timeline_commit_store.py:202-269`.
   When records carry v2 steps, `_verify_accepted` calls
   `_inverse_stage_history` and historical sequential validation. The latter
   calls `validate_sequential_capture` at `timeline_commit_store.py:254-269`.
5. `_inverse_stage_history` calls `self.history_entry` once per undo publication
   at `timeline_commit_store.py:864-873`; `history_entry` itself calls
   `_verify_accepted` at `timeline_commit_store.py:442-468`. This is the
   recursive loop observed in the retained original traceback and profile.
6. `validate_sequential_capture` validates both original and landing command
   boundaries at `timeline_commit_auth.py:2469-2535`; each boundary calls
   `_capture_records` and `_capture_document_images`. The latter performs full
   `CanonicalDocument` schema validation and payload digest checks at
   `timeline_commit_auth.py:2243-2267`, while `_capture_records` validates the
   `Recorder` at `timeline_commit_auth.py:2370-2387`. The generic validation
   entry performs finite traversal and then full JSON-schema validation at
   `timeline_commit_validation.py:130-146`.

## FACTS / CAUSE / UNPROVEN

### FACTS

- The current retained-original body reaches Runtime accepted-history
  verification and times out inside `jsonschema`; it is not a rejected request,
  a missing route, or a failure at the Agent selected-PARAM resolver.
- Runtime source directly re-enters `history_entry` from accepted-history
  inverse-stage verification. The authentic PASS profile measured hundreds of
  repeated history/verifier calls and depth up to 6, including 212 canonical
  image validations and 106 recorder validations.
- `same_revision=True` passes both retained originals; `same_revision=False`
  fails both. The changed-revision distinction is real, but it does not identify
  which historical edge or schema branch dominates.

### CAUSE

The smallest demonstrated causal seam is Runtime's recursive accepted-history
verification: `TimelineCommitStore._verify_accepted` →
`_inverse_stage_history` → `history_entry` → `_verify_accepted`, with each
historical sequential proof revalidating recorder/document boundaries. This
explains why a finite-walker improvement alone cannot be assumed to cure the
original 45-second failures. It does not show that one specific schema
definition, digest, or PARAM lookup is the sole cost center.

### UNPROVEN

- The exact per-original call counts and phase split (base/target history,
  original/landing capture, `Recorder` vs `PreparedCommit` vs
  `CanonicalDocument`) were not instrumented in this investigation; no new
  measurement body was authorized.
- The P4 `fps` frame and its 54/2/56 counts are authentic P4 evidence only; the
  R2 timeout must not be declared identical by timeout coincidence.
- No original PASS, merge qualification, or fix effectiveness is claimed.

## Smallest unapplied seam and constraints

Runtime owner: first measure/repair the request-local recursion at
`TimelineCommitStore._verify_accepted` / `_inverse_stage_history` (caller
`history_entry`, current lines above), with a secondary validation-dispatch
measurement at `validate_commit_value`. Any optimization must remain inside the
existing locked acceptance/history read and preserve the complete accepted
closure, recorder, event, digest, schema, and sequential-proof checks.

- Caller/pin: key any request-local reuse by exact `(project_id, timeline_id,
  publication_id, allow_archived)` and the current locked read/transaction
  context. Publication identity, not equal revision bytes, orders effects.
- ABI: no changes to `RequestCommitPort`, provider signatures, request/reply
  DTOs, idempotency behavior, receipts, or the 45-second guard.
- ABA/security: never cache by revision/content digest alone, across requests,
  or across mutable database snapshots. A same-byte different-publication edge
  must still be independently attributable; event/history/record custody and
  authorization must remain rechecked at the correct scope.
- No finite-walker shortcut, dropped schema validation, mutable history/authority
  cache, synthetic acceptance, test weakening, skip/xfail, or budget increase is
  justified by this evidence.

Recommended next bounded non-original measurement: Runtime-owned,
disabled-by-default local counters/timers around `_verify_accepted`,
`_inverse_stage_history`, `_historical_sequential`, `_capture_records`,
`_capture_document_images`, and `validate_commit_value`, tagged by
publication/edge, original-vs-landing, command ordinal, and validation
definition. It must emit no persisted data and make no acceptance decision.

# Runtime Main-infrastructure touched for M4 disclosure

Read-only disclosure of integrated Runtime changes on `tl/integration` at
`2ef92e46535e5dddf9db62342824986d9de5b9ec`. This is source provenance, not an
all-green, ZIP, or final-delivery claim. The [delivery README
template](../delivery/README.template.md) remains the applying/delivery
record. Scope follows the owner precedent: each false-refusal repair retains
the original positive, adds a strict negative, and has an independent review.

## WAV settlement enrichment (`8292b94`, integrated by `4ec5d59`)

- **Trigger:** a normal `generation.generate_speech` settlement published an
  `audio/wav` output whose `duration_seconds` key was absent, although the
  already-staged, content-addressed output could be inspected.
- **Invariant:** enrichment is missing-key-only. Runtime inspects one verified
  CAS descriptor (size/digest and open-file identity are checked) and stores a
  positive finite WAV duration. Explicit `null` remains explicit `null`; an
  invalid or zero-rate WAV remains unknown and selection refuses it. The
  settlement wire result, DTOs, and original idempotent replay order are
  unchanged; replay conflict/stale-fence refusal remains atomic.
- **Source/review:** `runtime_protocol/cas.py`, `service.py`, and `store.py`,
  plus `tests/test_generation_publish_v1_settlement.py`, from `8292b94`; the
  current-base carry is `b8930da`. Review provenance is the WAV829/speech
  intrinsics integrated lane (`tl/rt-m2-review-wav829-final`,
  `tl/rt-m2-review-speech615-intrinsics`, `tl/rt-m2-wav-integrated-scope-gates`).
  Named passing tests include
  `test_speech_settlement_derives_wav_duration_for_exact_media_selection`,
  `test_speech_settlement_preserves_explicit_null_duration_and_refuses_selection`,
  `test_speech_settlement_zero_rate_wav_keeps_duration_unknown_and_selection_refused`,
  `test_speech_settlement_verified_media_is_exact_over_authenticated_http`, and
  `test_publish_v1_replay_conflict_and_stale_fence_are_atomic`. The historical
  targeted cohort (`tests/test_generation_publish_v1_settlement.py` and its
  Runtime neighbours) recorded 120 passed.
- **Exclusions:** this does not activate the actual Speech SDK or prove a
  real Speech SDK producer; it adds no new public effect/DTO and no
  authoritative document pin.

## Publication-only Task input classification (`0113bc7`, integrated by `285a3b4`)

- **Trigger:** a normal producer task carrying an ordered script CAS input and
  the existing publication target was incorrectly classified as a two-edge
  continuation and refused before execution.
- **Invariant:** the exact publication-only shape is accepted as having no
  continuation edges. The ordered script descriptor, UTF-8 bytes, digest, and
  publication target remain unchanged across a source-document update,
  Runtime restart, and exact task replay. The existing two-edge continuation
  validation is unchanged.
- **Source/review:** `runtime_protocol/store.py` and
  `tests/test_timeline_producer_guards.py` from `0113bc7`, merged by `285a3b4`.
  Review provenance is `tl/rt-m2-review-script0113-authority` and the
  voiceover current-gates lane `tl/rt-m2-wav-script-batch-current-gates`.
  Named passing tests include
  `test_admitted_utf8_script_input_stays_pinned_after_source_update_and_restart`,
  `test_out_of_order_completion_admits_once_in_declared_order_and_paginates`,
  and `test_replay_conflict_and_restart_at_continuation_admission`; the same
  historical targeted cohort recorded 120 passed.
- **Exclusions:** this is not a new public effect, DTO, or authoritative
  document pin. It does not loosen continuation ordering or add a new producer
  API.

## Inherited door audit append race (`16acbb6`, source fix `d80b578`)

- **Trigger:** the door handler can append its audit JSONL record in
  `finally` after the HTTP response, so an immediate test read could race the
  append.
- **Invariant:** the test waits only for a bounded, complete-line/count
  condition, then retains strict audit fields and expected-count assertions;
  Runtime protocol behavior is unchanged.
- **Source/review:** `tests/test_door_transport.py` from `d80b578`, merged by
  `16acbb6`. The named passing test is
  `test_audit_lines_without_credentials`; its bounded neighboring audit-race
  lane recorded 6 passed.
- **Exclusions:** test synchronization only; no audit ledger, receipt, or
  product behavior was added.

No other changes are listed: Timeline-core changes, generated outputs, kits,
and unrelated infrastructure are outside this disclosure.

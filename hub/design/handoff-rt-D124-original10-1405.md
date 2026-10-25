# D124 original10 result review

Verdict: **RESULT REVIEW PASS WITH FAILED ACCEPTANCE OUTCOMES**.

This review is read-only. It credits the exact pinned run and preserves every
outcome; it does not claim a whole-product PASS.

## Custody and applicability

- Normal Agent receipt: `61fefc6983f4413f1d1964b149bbaf5eadb8d2f0`, tree
  `70fcd38844e7d93cdf97e4aebaf248d3736a312a`; its source commit is
  `16bbd56dbf016bcddeafa891291129efcfa87196`.
- Runtime: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree
  `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Composition: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- App was captured once as clean at `af5fe0a2748ce6df65fb36ce9cd435fc1df0502a`,
  tree `2afa38ba9e8ebfcefb23c81dbc1af3b1b9eabe0c`.
- Module origins resolve to the pinned Agent `astrid/sdk/timeline/commit.py`
  and pinned Runtime `runtime_protocol/service.py`; no borrowed 453b Runtime
  was used.
- All eight manifest target SHA-256 checks matched. All five test target byte
  hashes and all five recorded AST hashes matched independently. The normal
  Agent merge and independent security review 1339 are source credit only.
- The production seam is the original recipe → registered Agent provider →
  Runtime authority, with the C0 request/reply shape retained: base IDs,
  commands, label, steps, merge, reads, dry-run, idempotency key, and
  accepted/merged/conflict/invalid replies with canonical document, receipt,
  head, effects, bindings and dependencies where applicable.

## Admission and exact commands

Preflight passed the regular 5,000,000,000-byte floor at 5,001,871,360 bytes.
The exact Agent and Runtime checkouts were clean and pinned. The native smoke
ran once before original10:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-pin-16bbd56d:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$E/native-smoke.xml" tests/sdk/test_timeline_commit_native_boundary_runtime.py
```

Result: exit 0, all five smoke selectors passed in 3.73s.

Original10 ran once, with the same `-q -n3 -o addopts= -p no:cacheprovider
--timeout=45` flags, no marker or `-k` filter, and durable XML. The unique ten
selectors exactly match the published own-node recipe: two word-recipe nodes,
two occurrence nodes, three scalar modes, and three numeric cases. Result:
exit 1, 6 passed, 4 failed, 0 errors, 0 skipped, 15.46s.

## Smoke outcomes

All five are exact Runtime-pin result credit:

1. `test_native_child_batch_captures_materialized_input` — PASS.
2. `test_native_child_inverse_uses_authenticated_effect_images` — PASS.
3. `test_native_child_effect_tampering_cannot_write[revision]` — PASS.
4. `test_native_child_effect_tampering_cannot_write[digest]` — PASS.
5. `test_native_child_effect_tampering_cannot_write[physical-ref]` — PASS.

## Original10 per-ID outcomes

PASS IDs:

- `test_phrase_records_all_consecutive_main_word_ids` — PASS.
- `test_raw_canonical_bundle_compiles_in_fresh_process_without_history` — PASS.
- `test_bootstrap_birth_child_media_exact_history_inverse_redo_retry[False]` — PASS.
- `test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-occurrence:occurrence-1/clip:clip-1]` — PASS.
- `test_native_film_param_edit_preserves_exact_image_and_inverse[True-1-occurrence:occurrence-1/clip:clip-1]` — PASS.
- `test_native_film_param_edit_preserves_exact_image_and_inverse[1-True-occurrence:occurrence-1/clip:clip-1]` — PASS.

FAIL IDs and first unmet predicate:

- `test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[scalar]` —
  first unmet operation is `accepted = submit(body, 'app-scalars')` at the
  unchanged test source line 216. Runtime/provider acceptance rejects with
  `provider intermediate promotion differs from its sequential allocation`.
  Safe class/frame: authenticated Runtime commit validation, provider effect
  allocation/materialization frame; not an environment or harness failure.
- `test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[compound]` —
  same first unmet operation and same safe provider-validation frame/reason.
- `test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[separate]` —
  first unmet operation is the same submit at line 216. Runtime/provider
  acceptance rejects with `provider successor differs from its authenticated
  physical edges`. Safe class/frame: authenticated Runtime commit validation,
  provider successor/physical-edge custody frame.
- `test_bootstrap_birth_child_media_exact_history_inverse_redo_retry[True]` —
  setup, birth, and grouped acceptance complete; the first unmet operation is
  `undone = inverse(created, 'undo-birth')` at unchanged source line 222. The
  Runtime inverse validation rejects with `provider occurrence alias is outside
  its boundary`. Safe class/frame: authenticated inverse/physical-closure
  boundary validation. The outer line-70 assertion only reports the subprocess
  refusal.

The original assertions, requests, fixtures, parameters, and timing topology
were not edited. The five target test files are byte- and AST-identical to the
captured manifest; no original or smoke test was rerun during this review.

## Floor, integrity, and limits

Postflight recorded 4,974,526,464 bytes, below the 5,000,000,000-byte regular
START floor. No body, retry, or repeat was run after that drop. This is not a
continuous-floor claim; only the actual preflight admission is credited.

Independent checks performed after the run:

- `jq -e .` on all five JSON evidence records: PASS.
- Python `xml.etree.ElementTree.parse` on original10 and native-smoke XML:
  PASS; 10 and 5 testcase elements respectively.
- Python AST parse and `py_compile` for all five target test files, writing
  bytecode only to a private temporary directory: PASS.
- Scoped Ruff on all five target test files: PASS.
- `git diff --check` on pinned Agent and Runtime checkouts: PASS.
- Scoped mypy was attempted with the private cache path, but the requested
  `venv-agent-typecheck-v2/bin/mypy` executable was not installed; no mypy
  result is claimed. The earlier independent source review's baseline
  comparison remains separate evidence.

The original10 XML and raw logs remain private because failures contain raw
traceback/payload material. The safe exact XML/JSON/manifest copies and SHA-256
list are flat-published beside this handoff. The private original10 XML SHA-256
is included in that list for custody without publishing its contents.

No core-425 or REG14 count reduction is credited here. Those counts remain the
downstream Agent/Farm owner's accounting responsibility. This result is
applicable only to the exact smoke and original-ten selectors on the pinned
Agent/Runtime pair; it does not qualify full/core/P4, release adoption, or the
whole product.

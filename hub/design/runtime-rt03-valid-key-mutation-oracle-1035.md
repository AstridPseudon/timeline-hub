# RT03 valid-key mutation oracle correction

Date: 2026-10-21 UTC

## Result

Corrected only the RT03 negative block in
`tests/test_timeline_owned_reference_integration.py`.

The same-key changed-payload case now changes only the existing top-level
`rationale` request field. `validate_request(changed)` is called before the
commit, and the unchanged command list is asserted, proving the mutation is
schema-positive and one-to-one with the original request. The original
`args.role = "target"` mutation is retained as a separate same-key control
that explicitly expects status 422. Both controls snapshot and compare the
complete SQLite dump, timeline head, and commit history before and after the
refusal.

No product, schema, pin, generated client, fixture, ordered case, or other
test file changed. No qualification or adoption claim is made.

## Ordering trace

`RuntimeService.commit_timeline` first calls
`timeline_commit_port.validate_request(body)`, which validates the closed
`CommitRequest` and the `timeline.reference` union. Its
`TimelineReferenceArgs.role` is a `const: "source"`; therefore the retained
role mutation is invalid and must produce 422 before idempotency lookup.

After request validation, Runtime computes the request hash including the
whole body and enters `CommitExecutionCoordinator`. A changed `rationale`
under the original `exact-reference-key` keeps the command schema valid but
changes the request hash. The durable idempotency lookup then refuses the
changed request with 409 before provider execution or persistence.

The pure schema probe confirmed both premises:

```text
schema-positive changed rationale body: PASS
schema-negative invalid role: PASS (invalid CommitRequest: 'source' was expected)
```

## Oracle audit

The remaining RT03 assertions match the reviewed contracts and were left
unchanged: exact accepted status/receipt/result, exact reference ID/object
pin/source role in live and snapshot projections, empty occurrences/clips,
canonical sorted media manifest with both complete pins, restart exact retry
with provider tripwire and no duplicate/SQLite change, foreign raw ownership
refusal, occupied identity refusal with unchanged SQLite/head/history,
and inverse removal/restoration of the unrelated reference and complete
prior parent payload/closure.

No other concrete mismatch was found by source/schema inspection. The
ordered RT03 sibling remains untouched and unrun because it is blocked on the
separate Agent inverse diagnosis.

## Verification

- `git diff --check`: **PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python -B - <<'PY' ... ast.parse(...) ... PY`:
  **PASS**.
- Pure `validate_request` probe for the changed rationale body and invalid
  role body: **PASS**, as shown above.
- `PYTHONDONTWRITEBYTECODE=1 python -B -m pytest -q -p no:cacheprovider
  -m integration --collect-only
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract`:
  **PASS**, 1 test collected.
- Same selector with `--setup-plan`: **PASS**; complete closure included
  `tmp_path_factory`, `tmp_path`, `film`, `monkeypatch`,
  `astrid_importable`, and `agent`; no test body ran.

The collection/setup commands emitted one pre-existing Pytest warning about
the unknown `timeout` config option. No actual RT03 execution, full suite,
HTTP/socket/browser/render/install/generation run, or ordered-case run was
requested or performed.

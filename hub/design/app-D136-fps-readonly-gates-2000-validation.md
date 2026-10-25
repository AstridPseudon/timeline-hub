# D136 validation record

## Gate result

`STOP_REPORT_REGRESSION_D54A`.

The local published Agent ref `origin/main`/`origin/HEAD` resolves to
`886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`, but remote freshness cannot be
established without the prohibited fetch/acquisition step. Therefore G1 is
`NOTQUALIFIED`, despite the exact path being absent at that local ref and at the
frozen SDK candidate.

G2 is a captured-ref regression. Pristine upstream's `ThemeOverrides.visual`
schema is an open object (`additionalProperties: {}`), so `canvas.fps` is not
array-rejected. Its `_timeline_fps` helper (lines 171–187) only returns a
positive scalar and otherwise falls back to `30.0`; it does not reject the
array. The receiving Agent provider's `_fps` (lines 53–64) rejects the array as
not a finite number and explicitly supports only positive scalar or exact
integer numerator/denominator mapping.

Approved C0 does not define TimelineConfig or this field. It requires provider
validation of final known parameter schemas and preserves open document fields;
it cannot be cited as an upstream FPS rejection rule. The list-accepted versus
receiving-list-rejected condition requires D54a handback.

## Static checks performed

- Read-only receiving commit/tree/blob/hash census: PASS.
- Read-only current Agent FPS validator/schema source comparison: PASS.
- Read-only pristine upstream schema/validator source comparison at exact local ref: PASS.
- Read-only frozen R4 SDK/C0 source/ref census: PASS.
- Read-only AST conservation census: 43 original predicates, 11 test bodies,
  54 fixture statements; current module has one additional setup assertion,
  consistent with the protected source record.
- Python tests, service, socket, browser, profile, full suite and rerun: NOT RUN
  by task rule.

## Required lead readback

The Agent/App lead must return the current published upstream tip's full commit,
full ref/provenance, publication timestamp and exact presence/absence result for
`tests/sdk/test_timeline_capture_projection.py`. No stale local ref may be used
to qualify G1.

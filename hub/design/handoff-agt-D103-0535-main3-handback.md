# D103 MAIN3 source handback

This is a source-only handback. It does not claim behavioral qualification.

## Exact candidate and normal merge state

- Author candidate commit: `ef3d6c0b60c87601b6ba0adb415609e585d33e3e`.
- Candidate source blob: `793ab7efc71ead62c0b8e2ab827f31856a066aec`.
- Candidate source SHA-256: `bd29a7a63e2213c326321ddf38bae2fe3df751c60ffa8acef1eaed46e8743868`.
- Independent review: `PASS_SOURCE`, report `handoff-agt-D103-0535-review-report.md`.
- D103 normal merge target: `9c9ba51f65b94b6ea9363caf04329dad5b33f201`.
- Current home `tl/integration` target: `bde578505c035ae949ee8176b466bf8297772904` (the D103 merge target is an ancestor; current source blob remains `793ab7efc71ead62c0b8e2ab827f31856a066aec`).
- Queue receipt: `merge-agt-F-D103-CLItrim-video-0520` says merged into Agent `tl/integration` at `9c9ba51f65`; no refused merge record exists.

## Authentic media and exact containment

- Tracked fixture: `tests/fixtures/reshape/hype_regression/main.mp4`.
- Git blob: `c54c64cdc532ef4d08752ee01983966e58726531`.
- File SHA-256: `a13a68e512b6fae7fa4edd71b68266b33d1f7581be3fa199031809ec14d2f95e`.
- Reviewed file size/container: 102,248 bytes, ISO BMFF/H.264/AAC; reviewed `mvhd` duration 42 seconds and `mdat` ending at EOF.
- Exact authored source windows remain `[1, 6)`, `[1, 5000001/1000000)`, `[1, 4)`, and `[1, 3)`; exact source endpoint is `6`.
- Exact occurrence ends remain `5/2`, `4000001/2000000`, `3/2`, `1`, and moved `11/2`; retained title end is `6`.
- The 42-second genuine file duration therefore contains every authored source endpoint and occurrence end. No fixture-made-valid behavioral result is inferred.

## Canonical MAIN3 selectors

Run exactly these original selectors on the current integrated Agent/Runtime tuple:

```text
tests/editing_conformance/test_cli_trim_runtime.py::test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[disjoint-rebase-undo]
tests/editing_conformance/test_cli_trim_runtime.py::test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[relevant-conflict]
tests/editing_conformance/test_cli_trim_runtime.py::test_cli_move_exact_retry_restart_and_undo_over_real_http
```

The run must retain the existing lost-ACK, exact retry, restart, peer
rebase/conflict, dependent suffix, inverse/undo, history, publication,
canonical-document, physical-identity, and no-write assertions. MAIN is the
sole proof venue; no source-only result is a behavioral PASS.

## Distinct opaque6 source receipt

- Normal opaque6 merge receipt: `fd3cbf2b1a` (merge of `tl/rt-D86-6058-opaque6-0514` into Agent `tl/integration`).
- Opaque6 source commit: `3c742a9cfa1509234ca70048612e7302e4e2298c`.
- Opaque6 reviewed target blob: `339bf63752f509c1c0cb6b1fce30cda385dd2065`.
- Exact protected review is published separately as `handoff-agt-D103-0535-opaque6-review.md`; it is source-only PASS and defers behavior to MAIN.

# D116 protected return review

## Verdict

**PASS_SOURCE; genuine downstream FAIL remains.** The final candidate is source-qualified for D116, but the eight-node protected sample is not all green and the 95-test cluster must not be credited as full GREEN.

Candidate `tl/agt-F-D116-first-return-1040`:

- commit `7c717062128f61adacf613b6ee05a0992abb9024`
- parent `21146cd6decaa1c15bca1753ca719f6937040798`
- baseline `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`

## Review result

The candidate restores the complete C0 request envelope in both producer paths. It supplies the exact scope/base pair, commands, label, sequential steps, merge mode, reads, dry-run flag, source/rationale/group fields, and the real caller's idempotency key. `doc.patch` step patches are the ordered submitted changes; semantic step patches remain empty where C0 permits them. The field-omission workaround is removed.

The native and recipe callers now use the genuine current-form seed. The previous `Recording.compile_inputs` mirror monkeypatch and both canonical readback masks are removed. The approved first-use expectation is retained source pin `[case.pin]` before and after acceptance/refusal, with exact restart retry behavior. Original word text, FPS, timing, opaque payloads, topology, and short-negative interval/refusal purposes are preserved.

The prescribed protected sample, run with the exact candidate and 45-second timeout, recorded 6 PASS / 2 FAIL / 0 error / 0 skipped in 37.325 seconds. PASS covers first-use retention/restart retry, all three unavailable-pin refusals, `short-occurrence`, and `raw-source-window`.

The two FAILs are:

- `test_phrase_records_all_consecutive_main_word_ids`
- `test_raw_canonical_bundle_compiles_in_fresh_process_without_history`

Both reach `bundle_from_document` and the production lookup path, which rejects divergent `parent.clips` and `parent.config.clips`. This is the requested real-producer/current-caller seam, not a hidden source-fixture omission. No normalizer or product fix is authorized by D116 and none was added.

## Checks and custody

Ruff, AST parsing, and full-range `git diff --check` were independently rechecked against the candidate Git objects. The candidate hashes match the exact author-run evidence for mypy, `py_compile`, and diff checking. No product, validator, registry, pin, generated, or fourth timing file changed in the D116 return. No full/95 suite, P4, body, browser, observer, M5, or credential evidence was run or exported.

This is not a second substantive source failure, so no `HARD:` Sol escalation is requested. Keep the two recipe failures visible as downstream production work; do not add a test normalizer or weaken the approved negative controls. The unchanged 95-test cluster was correctly not rerun after the sample remained non-green.

Evidence summary: `scratchpad/orch/workers/agt-F-D116-protected-return-review-1104/evidence/`.

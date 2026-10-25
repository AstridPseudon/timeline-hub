# D124/D126 root finding

The first sanitized exception is `SystemExit: P2 Runtime phase helper is unavailable at the selected Runtime source`, at `scripts/testing/sitecustomize.py:51`, `_start_capture`. The actual guard-only invocation reproduced it. On automatic startup, lines 81–88 catch `BaseException` and call `os._exit(78)`, so no exception text reaches stderr. This explains the empty first exception and generic endpoint-readiness failure.

1402 and 1414 selected the correct reviewed bytes under the wrong basename (`app-D124-helper-final-review-1315-helper.py`). D66's absolute path/file/SHA checks accept that source; Python's next guard requires `p2_commit_phase_capture.py`. 1354 initially made the same mistake, then changed only its selected path to the retained canonical-basename helper and passed both controls. The two files have identical SHA256 `6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`. Bootstrap and harness source are byte-identical across af5fe0, parent 4b4e0558 and candidate 9d75477. The evidence supports a launch configuration error, not a reviewed-helper implementation failure or validator regression.

No source was changed. No basename/hash/source/privacy refusal was overridden. A byte-exact canonical-basename helper copy is retained in this worker's evidence directory. The 1354 real capture remains readable (102 rows, 30758 bytes, mode 0600); only safe structural metadata was copied. This is prior activation evidence, not a fresh activation PASS.

## Request correlation

- `request` is the helper's local ordinal, scoped by capture namespace/PID/birth. It is not either request_id.
- Public HTTP `request_id`: `RuntimeHandler._request_id` accepts a valid X-Request-ID or creates uuid hex; `_error` and the response header return it.
- Logged service `request_id`: `RuntimeService._execute_timeline_commit` separately calls `_new_request_id` (`secrets.token_hex(16)`), passes it as `diagnostic_request_id`, and emits it via `_emit_redacted_diagnostic`. There is no public/service id equality guarantee. The missing-commit-callable handler and door refusal branches use HTTP ids directly; those exceptions do not establish general equivalence.
- Existing `idempotency_key_sha256` is SHA256 over exact UTF-8 header bytes, lowercase hex without prefix/normalization. It is an exact browser/helper join only when both observed the same key bytes. Retries share it: also use the existing namespace and ordinal to identify the attempt. It is not `request_hash`, which covers the canonical invocation/publisher/body.
- Current `timeline_commit_error` diagnostics contain request_id but no key hash; current helper contains neither public nor logged request_id. Therefore the existing hash cannot by itself join to those log lines. UTC proximity is not exact identity.

## Proposed next helper scope (unapplied)

No helper bootstrap fix is required. For the owner's additional request_id join, keep the existing helper as the sole collector. Observe the actual `RuntimeHandler._request_id` return and actual `_emit_redacted_diagnostic(request_id, ...)` call through trace call/return events. Associate them with the already-tracked request ordinal and emit separately named bounded SHA256 values (`public_request_id_sha256`, `diagnostic_request_id_sha256`) in the final summary. Never invoke id generation, read bodies/auth/URLs, or equate the ids. A missing observation remains null; early/pending failures may have no public id or diagnostic. Keep all current caps, retention/byte accounting, truthful dispatch/unsupported arrival, sampling denominator/loss and capture-wide overhead unchanged.

The next sole helper worker must implement and test that delta separately against the exact reviewed source. Meaningful required controls: two independent request threads with deliberately different HTTP/service ids; missing/early/pending observations; emitted diagnostic id versus actual logger argument; repeat-key attempts remaining distinct; private-marker ids only as digests; non-string/malformed values yielding null without inspecting payload; unchanged replies/exceptions/tracing and restored trace hooks; all 19 existing offline helper tests. Those tests were not run here because no helper repair was made. The App's closed-schema validator will also need coordinated review for any new fields; its two files remain owned by the separate clean importer.

## Validation limit

Fresh normal/reviewed socket controls were not run. The central service's generic targeted suite runs Vitest, and no exact Node two-control suite is registered. The central-only socket rule precludes running those controls directly. A clarification is pending. No full tour, browser/native run or activation GO is claimed. Typecheck/lint are N/A because no App source changed; source hashes, clean status and diff check passed.

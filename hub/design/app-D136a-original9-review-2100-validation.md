# Validation and privacy controls

## Actual-result custody

- Parsed the private original9 XML in place: 9 cases, 9 errors, 0 failures, 0 skips, 0 passes.
- Independently matched all nine testcase names to the retained selector list.
- The exact selector list was: `test_real_saved_projection_config_registry_and_full_pins_golden`, `test_real_saved_entire_expansion_golden`, `test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows`, `test_real_candidate_matches_sdk_opener_exactly[parent]`, `test_real_candidate_matches_sdk_opener_exactly[child]`, `test_real_candidate_matches_sdk_opener_exactly[new_shot]`, `test_real_candidate_matches_sdk_opener_exactly[duplicate]`, `test_real_candidate_matches_sdk_opener_exactly[remove]`, and `test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]`.
- Private XML, log, and run metadata were checked in place and remain mode `0600`. No private XML, payload, URL, frame, auth value, key, raw path, or private identifier is included in this publication.
- The published receiver facts retain the exact one-run admission reading `5,039,394,816` free bytes and post-run reading `5,038,260,224`, source hashes, Runtime pin identity, and XML/log hashes without exposing raw output. The actual XML hash is `2ca6517bfa5027cab5fdb1bab2c96cf42980e19d132d6606e4cce13cfbeed1a2`; the actual log hash is `fa2695167b4b8c2f648f43351cdcfe47f30217876304bf6d60e58a2a37ede6cf`.

## Source and tree controls

- Agent HEAD/tree and all three received Git blobs/SHA-256 values match the receiver manifest.
- Immutable Runtime pin is `ab1e4f6141987706132916e2da16477f5a019464` / tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`; the three registered-provider route module hashes match the reviewed custody facts.
- AST inspection confirmed the relevant source ranges: `_typed_fps_paths` 95-108, `_validate_fps` 141-155, initializer 7-22, provider commit 1160-1469, and test setup `submit` 251-260.
- `git status --short` is empty and `git diff --check` passes; no product, test-body, generated, pin, or fixture files were modified by this review.
- Prior receiver controls are reused exactly: 45 scoped tests passed; Ruff, mypy, compile, and diff checks passed. No 27-pass or 45-check duplicate was requested.

## Scope limits

This is a source/result review, not a new behavior run. No full client/server/public-production suite, browser, native provider, core/service rerun, collector, or new original9 execution was performed. The nine-result failure remains visible even though source custody and route custody pass. No current 9-go or release claim is made.

# D100a release assessment

## Verdict

`PASS_RELEASE_ASSESSMENT` for the narrow D100 additive physical-item-birth candidate.

All three requested gates pass in one read-only assessment:

1. **Corrected independent behavior:** App’s independent final-result review records the exact candidate `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1` / tree `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`, the corrected product/test receipt, the registered Astrid provider route, a real 5 GB admission, and `27 passed, 0 failed, 0 errors, 0 skipped`, exit 0, 2.86 s. The private XML remains App-owned and in place.
2. **B022 nonintersection:** Exact Git comparison resolves `9486cbb06e` and `42040a9c05` as two commits in the same Agent repository. The product/test diff is limited to `_command_state.py` and the additive D100 test. It intersects none of the retained B022 Runtime paths (`native_site` 213–218; `command_output` 2189–2335, refusal 2209), Agent physical-closure functions, or Agent private-capture producer functions. No intersection hunk exists.
3. **Security review:** The exact `9486cbb06e2ab53402086772e6c2bc18bc4849fc` candidate has an independent `PASS_SOURCE_SECURITY` review against `d4ba991638f7d94e6b9f91f5a463cd3587af00eb`. That review is source/security-only and explicitly says behavior was not run; behavior is supplied by the later independent App receipt, not by the security claim.

## Exact source identity

- Author branch: `tl/rt-Agent-D100-test-return-1914`.
- Candidate source commit: `9486cbb06e2ab53402086772e6c2bc18bc4849fc`, tree `0919e511bd28b3d3af76bb18155efda12c3e94f6`.
- Corrected additive follow-up: `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1`, tree `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`.
- Protected product blob: `astrid/sdk/timeline/_command_state.py`, Git blob `09cbeeddefdc6375ba7d026406c95fb35bafda40`, SHA-256 `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- Additive test blob: `tests/sdk/test_d100_item_birth_boundary.py`, Git blob `39ed571d5f3e49d2545fc31e1f868ee7c58dbc8a`, SHA-256 `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`.
- Runtime input: immutable `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

## Scope and remaining holds

This passes D100a only. It does not turn the separate App projection result into a pass: the independent record retains nine setup errors at the authored FPS value `[30000, 1001]` and makes no projection-acceptance claim. D136c’s original9 remains open with nine setup errors and zero body outcomes; diagnostics2312 is diagnostic-only and not a causal repair. D130 remains held. No source cleanup, fixture conversion, retry, collector, new body, or merge was performed.

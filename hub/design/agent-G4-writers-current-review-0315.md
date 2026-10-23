# FAIL — G4 writers current merge review

`7abb79956bad41d94b18039ca18f8bfeeb1a20bd` has a **PASS** G4 writer delta:
the only three current-parent resolutions are `publish.py`,
`timeline_elements.py`, and the narration test, and the source-writer lane is
**42 passed**. Both production callers use the reviewed `TimelineSession`
submit/flight-retry path with the v2 request fields; exact source custody,
ownership, retry, idempotency, inverse/opaque and element guards are preserved.

The final join is **FAIL** for the separately owned inherited G3 schema issue:
current/ecea schema blob `b399bafa7e50d8512d39c1f59786c7e8b5f5eae9` omits
`InverseArgs.steps`, while approved d106 includes it. Do not attribute this to
the G4 writer delta or repair it in this review. All 15 official 780 mappings
and lock match; V4’s six approved paths remain absent. Normal Ruff/mypy ratchets
pass at 2150/2150 and 1915/1915; vendor-lock, artifact, compileall and diff
checks pass. Runtime malformed-reply/text-alias holds remain external and the
known 21/native14 suites were not rerun.

# D127c findings

## D127c-F001 — blocker — final App source guard rejects the final helper

The final App blob `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` has the final Runtime helper binding:

```text
REVIEWED_PROFILER_HELPER_SHA256 = 095c252b...
```

Its `readCapture()` allowlist recognizes that hash and arms `reviewed-profiler`. However, the normal D66 bootstrap/source-pin guard at lines 1070–1078 only has branches for normal and reviewed, then an `else` that asserts `REVIEWED_NEW_HELPER_SHA256 = 4ee0424b...`. It has no branch for `095c252b...`.

Therefore a final-tree `p2CommitPhaseCaptureConfig()` returns the actual final helper hash, enters the `else`, and fails the assertion before the normal source-pinned bootstrap recipe can qualify. This is a committed-source defect, not an environment-only failure. The App validator unit positives passed because they exercise `readCapture()`/`assertCProfile`, not the live bootstrap source guard.

Disposition: `FAIL` / `STOP_UNAPPLIED`. No source, product, or test fix was made.

## Coupling result

The final committed App source does contain the intended mounted path: ElementsLibraryPanel → element adapter → `useTimelineSave` local save/outbox → `RuntimeDataProvider.commitTimeline` → generated `POST /v1/projects/{project}/timelines/{timeline}/commit` with Idempotency-Key. The final staging assertions identify the first element request as `source: { via: 'app' }`, one `doc.patch`, one `list.insert` under `parent/clips`, and `timeline.apply_element`; parameter edit and undo shapes remain distinct.

The Runtime helper independently passes the corrected targeted result and enforces dispatch/prefetch provenance, first matching element-shaped request selection, mixed/dry-run/retry exclusion, bounded cProfile output, private raw pstats, and restoration paths. The coupled result nevertheless fails on F001.

## Evidence custody

The promised binder1950 `evidence/` directory is absent. The source manifest in this packet is independently generated from `git show`/blob hashes; it does not claim binder-authored metadata exists. No live body, browser, full suite, activation, or product behavior is qualified.

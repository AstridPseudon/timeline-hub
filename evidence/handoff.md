# D141 handoff

Runtime classifier `rt-P2-D141-history-binding-classify-0140` owns semantic
classification. This packet supplies its two immutable SAFE inputs:

1. `extra-fields.json`: the actual-only added key names and JSON paths from
   the retained 3118 `assertNativeHistoryEntry` diff, relative to
   `historyentry/records`.
2. `prior-pass.json` plus `source-manifest.json`: the exact PRE-CUT 15203
   automatic-placement PASS case, its source tuple/tree pins, source spec
   path/blob, case title/counts, durations/exits, and raw receipt hashes.

The 3118 full run is not a passing replacement: it failed at the strict
history-entry assertion, with one readiness case passed and one placement
case failed. The earlier 15203 full run is also overall FAIL, but its exact
automatic-placement case passed and reached its complete tail. No same-file
or selector-only substitution was used.

UNKNOWNs: none for the requested safe key paths or retained source tuple/blob.
No product or contract classification is made here. Composition `635f` is
documentary host metadata only. Raw 3118/15203 artifacts remain in place and
untouched; no raw testdiff or field value is transferred.

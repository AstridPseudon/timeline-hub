# D141 popup identity correction handoff

`PASS_IDENTITY_CORRECTION`.

The production caller should consume the corrected derivative at the absolute `source-manifest.json` path. It preserves the 0232 source-manifest shape while replacing only the invalid Agent historic commit fields with the exact Git object and carrying full current/last-pass/author tuples, source blobs, retained run hashes, and the unchanged request/reply contract-preservation notes. `correction.json` names each old field, correction, and basis; the 0232 originals and related 0226 source map remain private and unchanged.

Corrected Agent identity: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / tree `6056414359ae9fce08d999d54cbecf719fda33c3`. The App historic trees were checked against their commits and were already full exact objects, so no blind expansion was made.

Retained evidence remains bounded: selector PASS is run `app-pin-96d4754b-d73-p2-96d4754b-submit-1025100712-15203`, popup ADD `36.819s`, with overall suite `NO-GO`; actual run is `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`, readiness `PASS`, original popup case `FAIL` before activation. Popup spec blob is `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6`.

Causal classification remains finite `UNKNOWN`: unresolved are accepted-head continuity at the canonical read, occurrence presence at that read, `activeCanonicalOccurrences` before `useShotGroups`, and the `useShotGroups` input/result before `ShotGroupOverlay`. The activation/layout commits are not proved causes; intended-contract and REG classifications remain not established. No tests or expectations were edited.

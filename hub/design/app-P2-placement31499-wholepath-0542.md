# D33 wholepath report — actual 31499

Outcome: **NO-GO for the original test, with no product or test changes.**

The first proven unmet predicate is the reload-mounted row assertion at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1213`:

```text
.clip-action[data-clip-id="clip-0"]
```

The committed preview label passed first. The DOM showed `Saved to canonical timeline`, the committed accepted revision, the canonical occurrence marker, and the newly imported media row.

Evidence from the retained trace:

- Placement commit: accepted, HTTP 200, receipt issued.
- Post-reload canonical/history/inspect reads: HTTP 200.
- Inspect result: `canonical_head`, `is_current_head=true`, matching head/content digests, selected target present.
- Internal child revision: four clips, including raw `clip-0` at `at=9`, `hold=5`.
- DOM: occurrence marker and imported media-digest row present.
- No evidence of local dirty state, canonical-head adoption lag, or unresolved canonical read.

The failure is an identity mismatch at the UI oracle boundary. The command and canonical internal revision use raw `clip-0`, but current projection deliberately mounts child clips as `<occurrence-id>:<raw-clip-id>` (`shotCompositionProjection.ts:336-348`). Existing integration coverage expects this occurrence-prefixed identity (`ShotTimelinePreview.integration.test.tsx:188-205`). The accessibility snapshot does not preserve the row’s `data-clip-id` attribute, so the exact mounted attribute is source-derived rather than directly observable; the media row itself is present.

The reviewed provenance caller is correct at `ShotTimelinePreview.tsx:258-274`: committed state is reported only with a canonical revision identity, while adoption/local states remain non-committed. Canonical reload projection also remains authoritative (`canonicalCompositionState.ts:33-70`; `LocalTimelineShotBrowser.tsx:105-145`).

Historical comparison is non-causal: old 20517 failed earlier on the preview label before this caller fix; parent20481 and asset27438 passed under different App/input tuples. Their outcomes do not establish a different cause for 31499.

Validation performed:

- XML validation with `xmllint --noout`: PASS.
- Artifact JSON validation with `jq empty`: PASS.
- App source identity: `e96be32f`, tree `484ea188`; clean.
- Protected test hashes matched before/after:
  - placement test: `c75baf23…`
  - readiness test: `2b9723db…`
- No new browser/full suite was run, per the READONLY/no-service instruction.

Source owner: `app-P2-placement31499-source-return-0542`. No product fix is justified by this trace; the next decision is to reconcile the test’s raw-ID expectation with the established occurrence-prefixed mounted identity.
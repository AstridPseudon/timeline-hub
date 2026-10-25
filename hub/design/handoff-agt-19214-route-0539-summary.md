# F-D86 corrected source applicability and routing

This is the explicit successor to `fd86-source-route-0514`; the original is
preserved unchanged. It is evidence-only: no product, test, schema, generated,
pin, ledger, or shared-record change was made, and no body, collection,
helper, fixture, function, probe, service, or full-suite execution was run.

## Accounting

The exact 61 selectors and direct body outcomes are preserved: **13 PASS, 21
FAIL, 27 ERROR, 0 SKIPPED**. Family totals are in `family-route.tsv` and all
selectors are in `per-id-route.tsv`.

The corrected exact-tuple PASS rows are behavioral proof at the recorded
Agent/Runtime tuple and exact tested source. They are not source-only PASS and
do not transfer to a new tuple or the core/full suite:

- CLI-document8: ordinals 50, 52, 55–58, 60–61 (8)
- D95-NEW-two: ordinals 34, 36 (2), separate from original550
- ordinary-sheet3: ordinals 38, 53 (2)
- ownedmove8: ordinal 40 (1)

The parent-media 18 FAIL rows and graph row 59 are **not CHANGED**. Their
actual captured test blobs equal current-home blobs: parent-media
`369b9a4532423589acaab09bfe48adb99a54e705` and graph
`9215b5a6277d54a50ede11c44ab2a9a146a56768`. Their live outcomes remain,
respectively, the track-lane refusal and internal-timeline scope mismatch;
they route to their existing narrow source owners without a repeated body.
The ordinary-sheet family is corrected to two exact-tuple PASS rows and one
live closure/provenance FAIL row; no closure claim is made for the FAIL.

The captured helper used by retained-input2 and word-bootstrap46 is not the
current helper: captured `b5247b5ef47b80f2810d8d2af67412a7b7687643` versus
current `dddde3a8b357f2a2141e35f3966795836a6890da`. Direct import/call tracing
shows that only ordinals 47–49 and 54 depend on it. The current helper has no
independent review in the inherited evidence, so those four rows are a small
named missing-input route, not guessed source eligibility or behavior credit.

Runtime also changed `timeline_commit_execution.py` between captured `0c62`
and current Runtime; the current D102 source review is recorded in
`source-heads.tsv`. This does not transfer any exact-tuple PASS or close any
failure.

## Corrected dispositions

- **READY exact-tuple proof:** 13 PASS rows listed above; exact tuple/source
  only.
- **READY source-owner routes:** ordinals 1–33, 35, 37, 39, 41–45, 51, 59.
  These are small, named source routes for the actual unchanged test sources;
  they do not close the recorded FAIL/ERROR outcomes.
- **PEER/LATER/MISSING:** ordinal 46, whose published selected prepared-video
  source binding has no hash; and ordinals 47–49, 54 pending independent
  review of the current helper blob. No source identity is guessed.

Existing ownership is preserved: D98a actual-29 path normalization remains
exclusive to Agent 0539; D101/D100 and restore owners are unchanged. No new
record is requested without concrete essential missing data. The C0 v2
request/reply shape, registered `commitTimeline`/provider path, exact inputs,
opaque values, assertions, refusal/retry/inverse/ABA/no-write guards remain
outside this evidence correction.

# A3 child-placement caller review — FAIL

Reviewed `21c518a5ba176dc81abd988bcfc46b4165e95d25` against current integration
`890b9561666c3619f69335dd747b15e042b3a9a3`; cumulative diff is limited to the
six assigned service/caller/test files.

The changed service and hook plumbing are internally correct: an explicit
`ownerRef` is forwarded verbatim into the registered `occurrence.fork`
`select`, while malformed and ambiguous owners refuse and absent owners retain
the parent-only path. The fork uses the existing A2 outbox/session, and the
targeted fake regression preserves the sibling and emits fork then placement.
The command grammar matches Agent’s closed `occurrence.fork` args and
`shot_id` identity rule.

The integration gate still fails. Actual mounted consumers at
`useGalleryPageState.ts:141-153`, `useImageGenActions.ts:64-76`,
`useShotImageMutations.ts:104-110`, `useAppExternalDrop.ts:58-64`, and the
other `useAddImageToShot` consumers pass only shot/generation/project data.
No production mutation payload supplies the selected canonical `ownerRef`.
The positive assertions are direct tests with the fabricated
`occurrence:selected-occurrence`; the optional fork branch is therefore not
mounted and the real UI still takes parent-only placement. This is the second
FAIL and must escalate to Sol.

Evidence: targeted 5-file Vitest 61/61 PASS; App `tsc`, scoped ESLint,
`git diff --check`, normal Runtime/Agent lock checks, and private exact
Composition `0.0.14`/archive `819acf` graph checks PASS. No shared install was
changed. Browser/body/HTTP/live Runtime/build/full/central suites were not run
per brief, so actual Runtime accepted/merged physical-binding proof remains
unverified.

# Runtime main-history delivery contract

**Decision (2026-10-20 UTC):** keep the approved delivery shape. `merge-base
--is-ancestor(origin/main, tl/integration)` is a delivery-shape classifier, not
an acceptance guard: an ancestor gives a ranged linearized binary patch and an
excluded-base bundle; no ancestor gives the same tree patch and a full bundle.
An unconditional ancestry refusal would reject the intentional unrelated-root
snapshot workflow (explicitly covered by the approved M4 delivery decision).

The approved script is unchanged at SHA
`cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e`. It pins
base and tip before diff/squash/bundle/verification, applies the synthetic
binary patch to a fresh main clone, verifies the bundle, compares both trees,
and rechecks both source refs. Its `ranged` boolean only selects the bundle
fallback and verifier prerequisite; it does not reject unrelated history.

## Evidence and interpretation

The preflight at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-current-main-delivery-preflight.md`
is not reusable as a final ancestry manifest. Its labels “no merge base” for
Agent, Runtime, and Composition contradict its own `0/247`, `0/165`, and
`0/40` left-right counts: those counts mean the recorded `origin/main` was
reachable from the recorded integration tip. The source refs have also moved
since that snapshot (Agent integration `79b33f8a` -> `c73b1ab1`; App main
`86d7def4` -> `bebadd0e`).

Fresh read-only probes of the current source refs report:

| repo | origin/main -> tl/integration | relation | shallow boundary |
|---|---|---|---|
| Agent | `96b283d5` -> `c73b1ab1` | ancestor; `0/249` | none |
| Runtime | `240d5bb2` -> `e2db1e8c` | ancestor; `0/165` | none |
| App | `bebadd0e` -> `0d5009e1` | divergent; merge base `574e97f4`; `6/153` | `3f05489e` |
| Composition | `67b8aa3d` -> `5a4e9b72` | ancestor; `0/40` | none |

App is genuinely shallow (`git rev-parse --is-shallow-repository` is true),
but both refs descend from its recorded boundary `3f05489e`; that is historical
shallow history, not evidence that main is stale. The other three source repos
have no shallow file. Conversely, Git topology alone cannot establish whether
an `origin/main` ref is current with its external remote. Only the required M4
owner refresh can establish that.

## Smallest truthful M4 check

After the owner-controlled refresh, freeze one four-repo manifest containing,
for each repo: authoritative refreshed `origin/main` commit/tree, frozen
`tl/integration` commit/tree, the `ranged`/`full` classification, and any
shallow-boundary marker. Build only from that manifest. Require the existing
script’s ref rechecks and patch/bundle/tree equality; record a moving ref,
missing ranged prerequisite, or tree mismatch as a failure. Do not turn
`is-ancestor` into a blanket hold, and do not infer remote freshness from a
shallow boundary or a missing merge base.

No fetch, ref mutation, script change, delivery dry-run, full suite, or ZIP was
performed for this read-only resolution.

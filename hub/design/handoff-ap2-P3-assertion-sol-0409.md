# P3 assertion correction handoff

## Result and scope

Source correction completed on App base `206d5f30c22b68975d94942430278a581140a0a4`
(tree `36b9938ee4eb7000396d116efd6723f36b83c1c5`).
The only worktree change is `tests/e2e/local/three-products.spec.ts`, limited to
`expectV2History`, its address-comparison helper, and the original Gate-5 calls.

Read PLAN §3 P3, both requested review reports, contract §§1/2/3/4/5/7,
the actual generated App DTOs, and the production Python provider sources
`_commit_patch.py`, `_doc_patch.py`, `_recording.py`, `capture.py`,
`commands.py`, `commit.py`, and `inverse.py` read-only.

This is a source correction for independent review. Actual Gate-5 remains
**UNQUALIFIED**. No central-service request, browser, journey body, full suite,
launcher, schema, generated DTO, pin, dependency installation, or lock change was made.

## Exact review-finding mapping

| Review finding | Correction |
| --- | --- |
| 0404 blocking: native `parent/clip:<id>` cannot match authoritative root-addressed effects | Normalize both operands before comparison. Native clip refs, root `clips/id:<id>`, and mirrored `config/clips/id:<id>` share one logical target. Native track, source, registry, asset, and parent collection addresses keep their actual wire identities. No lookup of a nonexistent `config.clips` is used to reject a native write. |
| 0404 secondary: recorder dependency carriers dropped | Check native selection snapshots, tagged read states, dependency keys/pins, binding-to-dependency links, and physical image revision/digest plus base/landing head, step/command ordinal, phase and effect side. Move image pins come from the actual landing-input document; source pins come from actual registry reads; rate pins come from the observed numeric/rational fps. The step union must cover the corresponding exact field/collection/scope observations. Unknown opaque pins require conservative scope coverage. |
| 0404 secondary: unordered `doc.patch` containment | Require exact ordered equality between submitted step patch and ordered `doc.patch` command changes for patch-only steps. Require exact ordered equality with actual recorder operand bindings, restoring each binding's submitted ref spelling for comparison. Preserve complete authoritative step equality rather than pretending provider effects cannot include normalization or additional effects. |
| 0355: missing declared reads | Preserve exact request-history optional `reads`, including omission versus explicit empty; compare step reads exactly and check declared observations against the authoritative dependency union. |
| 0355: step patch/dependencies only shape-checked | Preserve complete reply/history/recorder step equality, exact normalized reply-command/recorder-command equality, content checks for captures/effects/dependencies, and complete history-entry equality across restart/retry and after undo. These equality checks include the entire actual records, without dropping fields. |
| 0355: digest shape only | Preserve the complete canonical-document sorted compact JSON/SHA-256 recomputation. |

The production-mounted Gate-5 caller invokes the helper for accepted A, its exact
retry after restart, merged B, and mounted undo. It retains the actual A/B/inverse
entries and compares complete entries after later history reads.

All original reset, A/C/B ordering, lost ACK, reopen/restart, exact key/body/receipt
retry, full raw and immutable closure/component readbacks, C/opaque preservation,
history counts, mounted Undo, and zero-legacy assertions remain. The original
`merged` requirement and historical `rebased` compatibility remain unchanged.
Conflict-head, invalid code/path/hint, and preview `would_status` assertions elsewhere
are untouched; this journey claims only its applicable accepted/merged/history/undo subset.

## Decisions and production-shape details

- Binding evaluation is checked at the actual landing input or effect output,
  not by resolving historical observations against the final document.
  Inverse segment bindings refer back to the authenticated target publication/step.
- Native move target selection is an entity-identity query, not a full collection
  read. Its complete snapshot and observed identity are checked accordingly.
- Redundant native clears retain their exact dependency guards; unchanged captures
  do not require invented effect mutations.
- The recorder's aggregate clip-mirror write is compared in full with actual
  before/after arrays. Its native leaf writes still require matching authoritative
  effects. The provider itself treats that mirror as the same authored identity.
- Reply commands are compared exactly with authoritative recorder commands.
  Submitted commands remain checked claims: the provider legitimately completes
  a minimal inverse request with normalized capture fields.
- No TypeScript edit application, semantic executor, hand-authored document,
  expected digest, ignored-field projection, skip, xfail, timeout change, or product
  decision change was introduced.

## Exact checks on final source

Working directory: `/home/user/work/wt/ap2-P3-assertion-sol-0409`.

```bash
scratch_dir=$(cat /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-assertion-sol-0409/tmpdir)
ASTRID_APP_TIMELINE_PORTS_ALLOCATED=1 PLAYWRIGHT_PORT=19409 FAKE_RUNTIME_PORT=19410 PLAYWRIGHT_OUTPUT_DIR="$scratch_dir/playwright-output" npm run test:e2e:three-products -- --grep 'M2 real gate 5 \(M1 real mounted path\): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent$' --list
npm exec tsc -- --noEmit
npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
git diff --check
```

- Exact original Gate-5 listing: **PASS**, exit 0, **1 test in 1 file**.
- Requested TypeScript command: **PASS**, exit 0.
- Exact-file ESLint: **PASS**, exit 0, zero warnings.
- Whitespace check: **PASS**, exit 0.

An earlier exploratory listing used a leading `^` title anchor with the explicit
file argument and collected zero tests (exit 1). Playwright greps the full test
name including its file prefix. The corrected exact-title suffix selector above
collected exactly one test; no behavioral test was executed in either listing.

## Unverified and next steps

No behavioral PASS is claimed. The `doc.patch` source branch is strengthened,
but this original journey exercises native move and inverse posts; it is not
runtime qualification of every command or reply family. The requested root
TypeScript command is reported as run, without claiming a separate test-file
typechecking project.

Prior service 19140 (missing Composition effects export) and 29980 (missing
`TIMELINE_BUNDLE_AGENT_HEAD`) are setup failures, not product behavioral results.
Env0407 owns durable exact archive preparation; App0406 owns the product Vite
export resolver correction. There is no proof-body-ready claim.

Recommended next steps: independent source review of this correction, then the
same original central-service Gate-5 case on the ready, explicitly pinned cohort
after the environment owners' handoff. Nothing blocks completion of this assigned
source-only task. No commits, merges, checkouts, pushes, or branch/ref changes
were performed; the harness owns the commit.


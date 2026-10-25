# D108 App source audit

## Result

Both audit gaps are mapped on current App HEAD `6e21b74ff9`.

### Gap 1 — Runtime history/restore

Verdict: **RESOLVED/MAPPED; D01 remains OPEN.**

The old fresh/frozen predicate at `dataProvider.test.ts:625` (`d11417a59`, `3881e944`) covered:

- project-scoped history: current `dataProvider.test.ts:856–857`; production `dataProvider.ts:212–240`
- successful restore/new head: test `:858–863`; production `:242–262`
- current-head CAS: test `:864–867`; production sends both `expected_head` and `expected_publication_id` at `:250–257`
- accepted closure validation: incomplete closure refuses at test `:861–863`
- no fallback readback: test `:868–870`; accepted Runtime closure is authoritative
- negative guards: missing/unverified head/publication `:880–893`, foreign project/timeline `:895–908`, stale Runtime 409 preservation `:910–930`

Production canonical read/save paths are separately present at:

- read/load: `dataProvider.ts:996–1010`, `:1446–1518`
- guarded save: `dataProvider.ts:1065–1078`, `:1081–1122`, `:1128–1159`

The replacement was introduced by `baacef5d66f` (`fix(runtime): validate accepted timeline closures and restore guards`) and matches the approved contract at `app-contract-review.md:11`. This does not equate ordinary saves with restore/read behavior. D01 `deletion-ledger.app.md:6` remains `OPEN/WAITS` for whole-document saver retirement; it does not authorize refusal of this history/restore behavior.

### Gap 2 — Display labels/signature identity

Verdict: **RESOLVED/MAPPED to the approved display-only label boundary.**

Predicate mapping:

- old display-labelled resolved-config expectation: current `timeline-save-utils.test.ts:214–268` preserves resolved-config identity and signature; direct display-label positives/negatives are covered by `timeline-data.test.ts:575–586`
- old signature-strip predicate: current `timeline-save-utils.test.ts:622–637` and `:681–688` compare full signatures against the unprojected/canonical config
- old legacy pinned-group predicate: current `timeline-save-utils.test.ts:681–688` preserves group order and repaired geometry while using canonical full-config identity

Production boundary:

- derived labels are non-enumerable view data: `timeline-data.ts:498–521`
- `displayName` is view-only and `meta.label` retains only explicit labels: `timeline-data.ts:523–533`
- row reconstruction preserves authored labels and removes legacy derived labels: `timeline-data.ts:325–343`, `:382–390`
- save serialization removes derived labels: `timeline-mutation-engine.ts:141–173`
- actual rebuild callers include `useTimelineCommit.ts:341–363`, `:534–573`, and `timeline-save-utils.ts:31–70`

Negative and intent coverage remains in `timeline-data.test.ts:602–611` (derived name not persisted), `:614–623` (authored label persists), `:625–638` (command edit distinction), `:641–653` (split behavior), and `:655–660` (legacy derived-label healing).

Approvals:

- `app-main574-derived-label-reconciliation.md:24–35,48–62`
- `app-label-reconciliation-final-review-r2.md:7–13,45–74`
- `app-U3b-final-review-0738.md:1–30`

The approved review commits are ancestors of current HEAD (`5404ca470e`, `cd29ff2642`). D69’s source qualification also records zero remaining removed/loosened assertions at `app-U3-D69-home-and-preflight-1704.md:21,31`.

## Verification

- `git diff --check` — passed
- `git status --short` — clean
- No tests, TypeScript, lint, browser, Runtime, provider, or full suites run, as required.
- Source verification used exact Git line/diff comparisons; the audit’s 77 lexical matcher limits are not treated as AST proof.

No product, test, pin, generated, or ledger files were changed. Required `commit-msg` and `DONE` artifacts were created. The external design handoff was not written because worker rules prohibit writing outside the assigned worktree; this final report is the handoff.
# D30 report

Reviewed exact App `9b810408cc` / tree `9a37265f`, pinned Agent `079580ca`, and Runtime `37eb6c`. No source, test, spec, or design files changed.

| Case | Verdict | Correct finding |
|---|---|---|
| Transition None single | FAIL — oracle | Production submits `doc.patch`, `merge: fields`, declared request/step reads, `created: []`, and intent `Clear transitions: <id>`. The helper incorrectly requires atomic/no reads, omits `created`, and expects generic intent. |
| Transition None bulk | FAIL — oracle | Same defect; reads and clear intent cover both selected IDs. |
| registerAsset | FAIL — oracle | Production submits semantic `clip.add-media`, `merge: fields`, created parent asset/clip claims, and submitted `steps[0].patch: []`. The helper incorrectly requires atomic and nonempty patch. |
| Automatic child placement | FAIL — oracle | Reachable embedded drop path submits semantic `occurrence.add-media`, occurrence ownership, created claims, `fields`, and `patch: []`; Runtime enriches authoritative reply effects. Helper expectations are wrong. |
| Popup SWAP | PASS | Helper matches `[occurrence.fork, occurrence.swap-media]`, authenticated old/new selections, `fields`, and empty submitted step patch. |

C0 rule confirmed: `doc.patch` without reads falls back to atomic; declared reads permit `fields`. Semantic commands use `fields` with provider-generated authoritative effects. Idempotency is scoped to the commit POST via `Idempotency-Key`.

Evidence was static/source plus existing mounted/source maps; no browser, HTTP, backend, or duplicate suite was run. Checks:

- `git diff --check` — passed.
- `git status --porcelain` — clean.
- HEAD/tree identity — exact.
- Existing test pair `23809/9310` was not stopped or resubmitted.

Smallest fix owner: App P2 test helpers, with branch-specific assertions for document-patch versus semantic requests. Product routes require no change.

Completion marker and commit message were written.
## Result

SAME-ID run `app-pin-587316e3-d73-p2-current-1747-1024175319-22847` completed:

- Command: `bin/wait-test <ID> 1` (repeated after 124 timeouts)
- Result: exit 1, 402s
- Counts: 8 selected, 4 executed, 1 passed, 3 failed, 5 NOT RUN
- JUnit: `tests=8 failures=3 skipped=5 errors=0`

Failures:

- `three-products.p2-elements-assets.spec.ts:412:46`, 14.506s: expected dialog status `"applied"`; status element absent after 5s. Secondary page-close wait at line 149.
- `three-products.p2-popup.spec.ts:431:61`, 35.080s: actual 422 refusal: `validation_error`, `reason=invalid_records`, verbatim message: `provider created shot owner differs from its authenticated occurrence`. This is provider validation, not classifier safety denial.
- `three-products.p2-tour.spec.ts:631:113`, 115.403s: reload could not find the committed preview revision label within 90s.

The five serial dependents were not run.

Preflight/control evidence:

- Preflight `6282`: PASS, exit 0.
- Missing-runtime-SHA control `10754`: expected source-selection refusal, exit 1; not a safety denial.
- Normal launch/native seed/Agent identity/authoritative history: PASS.
- Readiness: PASS; connected editor and fresh scoped owner observed.
- No additional suite was submitted.

## Identity

Manifest confirms the captured four-repo tuple and clean source snapshots:

- App `587316e37891f1b474c2c3734e19044246b62285`, tree `84886c6b1915ca9748d04bb36c0fe8b6861efca6`
- Agent `f4d6c72ce336da66813fc39828187bccbaf80a5b`, tree `5d328a24dd64fb216ae527b6c05f51d99d7c564e`
- Runtime `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`, tree `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`

Service source was clean, with the App snapshot head `3a56e7a70b2c04d2c1acfbe3ca7f9b62a75ff2f1` and parent App SHA. Versions: Node 20.19.4, npm 10.8.2, `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.

## Safe evidence

Runtime safe-phase-hook JSONL: `UNAVAILABLE`. No qualified Runtime sink/output was present in the run manifest, log, or retained result tree. No Runtime category, code, phase, duration, or ordinal is inferred.

Existing App UIApply projection was validated and retained:

- 6 bounded events, 2,344 bytes, one correlation `apply-1`
- Ordinals `1..6`
- Phases: `apply-click → request-start → test-outcome → retained → teardown-start → page-close`
- Durations: `15375, 16008, 20663, 20698, 20700, 20718` ms
- Response status/code and category: `UNKNOWN`/absent
- Final terminal: `pending`
- Attachment and source content SHA-256: `d751a7d9236eaaeb2b42fac723391f1f4fe4da378feb6e16704bdd4eff0ae824`
- Worker-safe copy: `/tmp/w-ccc6211018/p2-element-apply-diagnostic.json`

## Changes and verification

No App worktree files changed; staged and unstaged `git diff` are clean. Created the required empty `DONE` marker and conventional commit message at the prescribed path.

Recommended next step: hand the exact three failures and Runtime-hook `UNAVAILABLE` result to the owning Runtime/App workers; keep the five serially unverified cases unqualified.
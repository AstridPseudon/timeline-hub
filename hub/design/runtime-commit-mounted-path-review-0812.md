## Report

- Corrected verdict: prior `commitSession.ts` citation **FAIL**; it is dormant D37 code.
- Mounted caller **PASS**, qualified to non-empty element edits:

  `useTimelineSave.ts:776-788` → `timelineLocalSaveHandoff.ts:257-590,598-617` → `localSaveSession.ts:304-311,158-200` → `RuntimeDataProvider.commitTimeline:751-768` → generated HTTP `:202-204`.

- Request shape: one `doc.patch`, `created: []` normally, atomic merge, declared reads, one step with ordinal `[0]`, matching patch, `dry_run:false`, `source:{via:"app"}`, exact revision/publication base, canonical `/commit` route.
- Idempotency key: random UUID allocated durably by `commitOutbox.ts:464-491`, reused on retry, sent as `Idempotency-Key`.
- Passing controls agree: App commits `2056c7c…` / merge `38b29b5…`; assertions at `VideoEditorProvider.runtime-elements.test.tsx:171-188`.
- Preserved facts: Agent validation is initial 3 / CAS retry 2; Runtime authority phases remain distinct. POST outcome, daemon, and server timing remain unknown. D47 remains deferred.

Evidence: [mounted-caller-source-callmap.md](/home/user/work/wt/rt-R-commit-caller-whole-path-0812/evidence/mounted-caller-source-callmap.md)

Checks:

- `git diff --check` — PASS
- Tests — not run; read-only source investigation.
- No product/source/test/pin changes. Commit message and `DONE` marker written.
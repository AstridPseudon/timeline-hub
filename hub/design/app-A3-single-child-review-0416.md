## PASS — A3 provider review

Reviewed commit `561a792a` against PLAN A3, commit-v2 §§1–4, Agent `079580ca`, and Runtime `37eb6c7b`.

Findings:

- Unshared genuine ADD emits registered `occurrence.add-media` through the scoped A2 outbox.
- Exact occurrence/shot/internal revision and dependency-pin guards remain enforced.
- Runtime media selection is queried and identity-checked; no fallback grants authority.
- Agent capture semantics match: new clip is always created; asset claim is created only when absent.
- Shared ADD/SWAP still emits `occurrence.fork` first, preserving existing behavior.
- Unsupported, foreign, stale, duplicate-root, malformed-pin, and mismatched-selection cases refuse before send.
- Production caller verified through `ShotTimelinePreview` → `localDocumentSave` → `useTimelinePersistence`.

Tests:

- Node 20 provider test: **28 passed**
- Exact 12-file acceptance command: **12 files, 341 tests passed**
- Three serialized TypeScript checks: **passed**
- Scoped ESLint `--max-warnings 0`: **passed**
- `git diff --check`: **passed**
- Allowed-file census: **only the two intended files**
- No product or test edits made by this review.

Qualification limits: no browser, backend, live Runtime/Agent integration, full suite, or install was run. The mock provider test does not independently prove live authoritative capture; static Agent/Runtime source inspection supports the emitted envelope.

Commit message and `DONE` marker written.
## D69 report

Implemented the smallest retry classification fix.

- Placement retries only when the outbox reports `kind: conflict` with `details.status: conflict`.
- Definitive refusals, invalid payloads, and transport failures remain durable and are not replayed.
- Existing stale-head retry remains bounded to one retry and preserves merged canonical closure.
- Added focused refusal/invalid/transport controls.
- Scope: `placementService.ts` and focused placement tests only.

Tests:

- OldRED: new controls failed under `fe773` for refusal/invalid replay.
- NewGREEN: focused Vitest, 3 files, **33/33 passed**.
- Serialized TypeScript checks: root, app, node — passed.
- Scoped ESLint — passed.
- `git diff --check` — passed.

Frozen upstream body hashes preserved:

- `fcf8e413...ce8dd0d`
- `80bd6c08...a1183b`

No full/browser/service suites run. No blockers. Commit message written and `DONE` created.
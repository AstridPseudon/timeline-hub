## PASS — A4/D52 transcript retirement review

- Candidate: `8a712d39c74e92ff10886007ae5135d4f316e92e`
- Tree: `27a5e398c14245317ca9fc7f8bb42b037bd84877`
- Parent/P3 pin: `602f8b1f58593302829fb449d0ded62a91462a22`
- Exact delta: only:
  - `transcriptAssociateCapture.ts` — 573 lines
  - `transcriptAssociateCapture.test.ts` — 397 lines
- Deleted test census: 1 `describe`, 5 `it`, 40 `expect`.

Review findings:

- No App production imports, value/type references, dynamic callers, or Agent registry entry for `transcript.associate`.
- Agent registry retains `doc.patch` and native operations.
- Live `useProjectTranscriptHost` → reconciliation/import → `commitData` → `doc.patch` → durable outbox path remains intact.
- Three live negative assertions rejecting `transcript.associate` remain.
- Generic `doc.patch` tests and neighboring helpers are retained.
- Protected tree is identical to `602f` outside the two deletions; deleted blobs are unreachable.
- C0 request/reply fields, P1–P5/H36/D53, clients, waits, and pins are unchanged by the exact delta.

Tests/checks:

- Node `v20.20.0` Vitest: 4 files, 50/50 passed.
- Serialized `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: all passed.
- `git diff --check`: passed.
- Scoped lint: N/A, deletion-only.
- Full/browser/backend/service/HTTP/original journeys: not run per brief.

Existing App ledger row remains current-branch-only `doing`:

`A4-D52-transcript | Remove exclusive dormant capture pair | ... | Author1210 | ... | Base602f`

No blockers. Recommended next step: manager performs the normal merge after the caller-source gate is resolved.
## A4/D52 census report — PASS

Bounded read-only assessment completed against:

- App HEAD: `602f8b1f58593302829fb449d0ded62a91462a22`
- Tree: `a38844975865110cd2c026dc10fd7aa1ea488e71`
- Agent current integration HEAD: `d411f439acce0c6bc2fa50f77a7f92c103773d5d`

No source, test, config, generated, ledger, or protected files were modified or deleted.

### Decisive finding

The only proven exclusive dormant cut is:

- `src/tools/video-editor/commands/transcriptAssociateCapture.ts`
  - Git blob: `bd14f45cbcd10292ca00246072949264d9127a91`
  - SHA-256: `a4db541841f2c068c2984c27225c6fd14a5b557a648b6d9412b5ed5e352020a2`
- `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`
  - Git blob: `5c39a293009df59f796fe476e107a0a9900244d7`
  - SHA-256: `56c1c0bb0393ec2275caf6f76af07b207c23d873e1551f687de9393364b31516`

Current App search found:

- The implementation is not imported by production code.
- Its exported values/types are referenced only by its own test.
- No dynamic import/load path reaches it.
- `transcript.associate` appears elsewhere only in three negative assertions in `project-transcript-host.persistence.test.tsx` at lines 469, 539, and 695.

Current Agent registry inspection found no `transcript.associate` production operation. `commands.py:75-115` registers `doc.patch`, `clip.anchor`, `text-binding.set`, and other native operations; `validate_command` rejects unregistered operations at lines 142-149. The exact production-source search returned no `transcript.associate`.

### Live path retained

The mounted transcript path is separate and must remain:

`useProjectTranscriptHost` → `project-transcript-host.ts:600-674` → `reconcileTranscriptReferences.ts:66-147` → `commitData(..., { save: true, semantic: true })` → `flushPendingSave` → `localSaveSession.ts:158-188` → Runtime `commitTimeline`.

Imports and source selection also remain through `importTranscriptHandoff.ts:312-316` and `project-transcript-host.ts:747-857`.

This live path emits generic v2 `doc.patch`; it does not call the dormant capture module or provide a `transcript.associate` provider counterpart.

### Dormant test coverage inventory

`transcriptAssociateCapture.test.ts` is 397 lines with 40 assertion statements:

- Lines 161-223: nested source planes, operation record, dependencies, bindings, writes, caption/review reconciliation, immutability.
- Lines 225-252: exact prior pin retention and source ordering.
- Lines 254-267: mismatched pin refusal and atomicity.
- Lines 269-368: populated config-clip mirror, reads, expectations, authorship, writes, and atomicity.
- Lines 370-382: two parameterized cases for caption collision and shared review ownership.
- Lines 384-397: malformed pinned source refusal and atomicity.

These are exclusive legacy-operation tests. They are not equivalent coverage for current generic `doc.patch`, transcript-host persistence, recovery, undo, native `clip.anchor`, or Runtime guarantees.

D31/D37 historical retention was therefore preserved conceptually: the old behavior is not represented by a production Agent operation, but its exact operation-record and refusal semantics differ from the live generic path. D52 permits a proven exclusive dormant cut, but this census does not authorize deletion of neighboring helpers or live tests.

### Verification commands

Passed:

```text
git diff --check
git diff --exit-code HEAD --
git diff --cached --exit-code
git status --short --branch
```

All returned clean/zero. No tests were rerun; this was a report-only census per the brief. Existing qualification evidence was reused by exact tree/source identity. Full, browser, live-socket, and source-union suites were not run.

Recommended next step: a separate manager-authorized PR containing only the two named dormant files, followed by independent review. Shared transcript host, reconciliation, generic patch, session, outbox, recovery, undo, and native transcript paths must remain.

Commit metadata was written and `DONE` created.
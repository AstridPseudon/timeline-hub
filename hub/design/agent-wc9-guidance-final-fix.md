# WC9 guidance final fix

Status: complete on worker branch; WC9 remains `IN PROGRESS`/`HELD` pending
manager rereview and merge. The deletion ledger was not marked deleted.

## Exact delta

Base worker HEAD: `610643820bcb474a7e4c9ce6862d88c70fcfda67`.

Only `astrid/packs/rendering/docs/SKILL.md` changed in the worktree. The four
requested guidance regions were repaired (current lines 250-267, 278-283,
673-678, and 721-738):

- Helper-catalog transforms are explicitly read-only/migration preparation.
- Supported publication is captured commands through the native CLI/session and
  existing durable outbox, or a settled proposal queued/flushed by its
  requester.
- Unsupported intent is refused visibly, with the draft retained and the
  missing command reported; no automatic checkout/CAS fallback is suggested.
- Complete composition edits are migration-only/held.
- The checkout example retains checkout/bind/check and readback capability
  explanation but no longer runs the held detached `publish` writer.

No product code, script, template, API, schema, CLI flag, signature, pin, R4
archive, integration worktree, or other WC9 document was changed. Existing
product docs, native examples, 401-word architecture page, and R4 archive are
preserved.

## WC9 census

The WC9 scoped set is six documents: the five prior changed product/reference
docs plus `docs/architecture/timeline.md`. Native command/session/outbox and
settled-proposal requester guidance remains present across that set. Detached
checkout, CAS, cut-sheet, and whole-candidate references are explicitly marked
held, migration/read-only, legacy-draft, or visible-refusal/draft-retention.

There are zero uncaveated detached-publication fallback instructions in the
four repaired SKILL passages and zero runnable checkout-to-`publish` examples
remaining in those passages. The separately held guide/reference migration
sections remain unchanged; they are not presented as the normal writer.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python3 scripts/reshape/check_doc_references.py` — PASS: 0 errors, 0 warnings; 193 docs, 547 capability refs, 263 CLI refs.
- Fenced Python AST probe over `astrid/packs/rendering/docs/SKILL.md` — PASS: 8 blocks parsed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python3 -m astrid timelines edit move --help` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python3 -m astrid timelines edit track-label --help` — PASS.
- Isolated `inspect.signature` probes — PASS for `TimelineSession.open`, `commit`, `commit_many`, `queue_proposal`, `flush`, `undo`, `Checkout.open`, and `RemoteTimelines.open_composition`.
- `git diff --check` — PASS.
- No tests, full suite, browser, live-socket, or large-fixture runs were requested or performed.

The first combined signature probe imported `RemoteTimelines`, `Checkout`, and
`TimelineSession` in an order that exposed an existing circular import between
`astrid.sdk.timeline.checkout` and the legacy re-export. Each public signature
validated independently, so this is not an unresolved documentation blocker;
no source fix was made because the task is docs-only.

## Handoff

Updated shared handoff:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc9-native-docs-cut.md`.

Updated `WC9` in:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.agent.md`.

Recommended next step: manager rereview this one-file docs delta, then merge;
keep WC9 held until the manager confirms the remaining legacy migration
surfaces are either retired or command-backed.

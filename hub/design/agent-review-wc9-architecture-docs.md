# WC9 architecture/docs gate — HOLD

Reviewed candidate commit `61064382` against its base (`tl/agt-m2-wc9-native-docs-cut`), plus the candidate worker report. No repository source changes were made.

## Decision

HOLD. The native examples and architecture landing page are otherwise consistent with the public Agent APIs and settled plan, but the rendering skill retains uncaveated legacy fallback instructions that can teach an agent to publish through the held detached writer. The ledger should remain held until these references are corrected.

## Required documentation fixes

1. `astrid/packs/rendering/docs/SKILL.md:250-263` — the general workflow says to use the detached helper catalog for transforms, then “validate the complete candidate” and save through the compare-and-swap/idempotent publication boundary. Rewrite this as migration/read-only preparation only: use a native command when covered; otherwise retain the draft and report the missing command, with no detached publication fallback.
2. `astrid/packs/rendering/docs/SKILL.md:271-276` — the agent preamble says “otherwise edit a detached same-schema candidate with ordinary code. Validate, diff, and save.” Replace that branch with an explicit visible refusal/retained draft and “do not publish through the held checkout writer.”
3. `astrid/packs/rendering/docs/SKILL.md:664-667` — “Use the detached checkout recipe for that complete composition edit, with Runtime head comparison at publication” contradicts the held-writer policy. State that the complete composition edit is currently migration-only/held and must not be published as a fallback.
4. `astrid/packs/rendering/docs/SKILL.md:710-717` — the “runnable checkout example” still presents checkout → bind-script → check → publish as a complete path, despite the surrounding text saying the broad candidate publication is held. Mark the block explicitly migration-only and say that unsupported normal edits must be retained/reported rather than sent to `publish`, or remove the publication example until native coverage exists.

The changed guide/reference pages already contain the required explicit warnings (for example `docs/timeline-editing-guide.md:292-297`, `astrid/packs/rendering/docs/references/document-checkout.md:3-16`, and `astrid/packs/rendering/docs/references/editing.md:80-102`); preserve those distinctions when fixing the skill.

## Verified as correct

- `TimelineSession.open(project, timeline, *, client, outbox_path=None, base_revision_id=None, base_publication_id=None)` and the documented `move`, `trim`, `commit`, `commit_many`, `queue_proposal`, `flush`, and `undo` calls match the current public Agent signatures.
- Native CLI examples match help: `timelines edit move` accepts `--clip`, `--on`, `--dry-run`, `--idempotency-key`, `--json`; `track-label` accepts `--track`, `--set|--clear` and the same publication controls.
- The examples describe original guard capture, durable exact-flight outbox retry, fresh keys for new intent, and no guard recapture after a lost acknowledgement. Proposal artifacts/dry runs are correctly distinguished from Runtime receipts.
- `docs/architecture/timeline.md` is 401 words, explicitly says M4 is not complete, preserves the R4 archive, names the immutable producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, compatible server `7f6dd89`, and public Composition `0.0.12`, and lists held seams/open gates.
- Distinct Read/See/Edit, producer, view, and held authoring-bundle capability explanations remain present.

## Checks

- `PYTHONPATH="$PWD" python3 scripts/reshape/check_doc_references.py` — PASS (0 errors, 0 warnings; 193 docs, 547 capability refs, 263 CLI refs).
- `git diff --check HEAD^ HEAD` — PASS.
- `PYTHONPATH="$PWD" python3 -m astrid timelines edit --help`, `edit move --help`, `edit track-label --help`, `undo --help`, `redo --help`, `show --help`, `visualize --help` — PASS; documented flags/signatures present.
- Python `inspect.signature` probe for public `TimelineSession`, `Checkout`, and `RemoteTimelines.open_composition` — PASS.
- Python AST compile probe for fenced Python examples in all five changed docs — PASS.

No full or browser/live-socket suite was requested. No code, templates, scripts, fixtures, shared dependencies, integration worktrees, or R4 archive were modified.


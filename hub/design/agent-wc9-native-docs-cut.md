# WC9 native docs cut

Status: worker cut plus final guidance repair applied; WC9 remains HELD pending
manager rereview/merge. Do not mark WC9 deleted from this worker branch.

The active Timeline product docs now present `TimelineSession` and the native
CLI command adapters as the normal write path. Native sessions capture original
read/expect guards once, persist the exact request and retry identity in the
durable outbox, and use Runtime's `/v1` commit route. Settled producer proposals
are queued unchanged and flushed through that same outbox; proposal artifacts,
digests, and dry runs are not receipts. The architecture landing page names the
current compatible Runtime `7f6dd89`, immutable producer `2c4ac180...e99ce26a`,
and integrated public Composition `0.0.12`, without a delivery-completion claim.

Changed docs:

- `docs/timeline-editing-guide.md`
- `docs/timeline-authoring-capabilities.md`
- `astrid/packs/rendering/docs/SKILL.md`
- `astrid/packs/rendering/docs/references/document-checkout.md`
- `astrid/packs/rendering/docs/references/editing.md`
- `docs/architecture/timeline.md` (401 words) plus the guide link

The detached Checkout/cut-sheet/whole-bundle paths are explicitly labeled as
held migration surfaces. Exact remaining legacy instructions are the guide's
detached working-copy `checkout`/`edit`/`publish` section (including narration
and cut-sheet flows), the rendering SKILL's held `publish`/`apply --native`
migration notes, and the checkout reference's migration-only script/helper
catalog. `scripts/timeline_document.py` and templates remain unchanged. WC9
must not be marked deleted until those remaining paths are retired or every
covered operation is command-backed.

Final repair delta (this worker): only
`astrid/packs/rendering/docs/SKILL.md` changed, at the four requested anchors
(current lines 250-267, 278-283, 673-678, and 721-738; line numbers may move).
The helper catalog is now explicitly read-only/migration preparation; unsupported
intent is a visible refusal with the draft retained; complete composition edits
are migration-only/held; and the checkout example no longer runs `publish`.
Normal publication is named only as captured commands through the existing
durable session outbox, or a settled proposal queued/flushed by its requester.
No flag, signature, product code, script, template, API, schema, pin, R4
archive, or other WC9 document changed in this repair.

WC9 scoped-doc census after the repair: six documents (the five changed docs
listed above plus `docs/architecture/timeline.md`) contain native command/
session/outbox or settled-proposal publication guidance; detached checkout,
CAS, cut-sheet, and whole-candidate mentions are all explicitly held,
migration/read-only, or visible-refusal/draft-retention guidance. There are no
uncaveated detached-publication fallback instructions remaining in the four
repaired SKILL passages, and no runnable checkout-to-`publish` example remains
there. The separate guide/reference held migration sections remain intentionally
unchanged and are not normal write instructions.

Validation:

- `python3 scripts/reshape/check_doc_references.py` — 0 errors, 0 warnings;
  193 docs, 547 capability refs, 263 CLI refs.
- `git diff --check` — passed.
- Native `TimelineSession`/proposal snippets — Python compile probe passed.
- `python3 -m astrid timelines edit move --help` and `edit track-label --help`
  — documented flags/signatures present.
- `wc -w docs/architecture/timeline.md` — 401.

Final repair validation on the worker tree:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python3 scripts/reshape/check_doc_references.py` — PASS (0 errors, 0 warnings; 193 docs, 547 capability refs, 263 CLI refs).
- Fenced Python AST probe for `astrid/packs/rendering/docs/SKILL.md` — PASS (8 blocks parsed).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python3 -m astrid timelines edit move --help` and `edit track-label --help` — PASS.
- Isolated `inspect.signature` probes for `TimelineSession`, `Checkout.open`, and `RemoteTimelines.open_composition` — PASS; the first combined import order exposed an existing circular import, so no combined-import pass is claimed.
- `git diff --check` — PASS.

No full suite or browser/live-socket suite was run (docs-only task). No product
writer code, templates, scripts, R4 archive, integration worktree, or shared
dependency was modified.

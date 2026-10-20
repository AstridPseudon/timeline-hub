# WC9 native docs cut

Status: worker cut applied; WC9 remains HELD pending manager review/merge.

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

Validation:

- `python3 scripts/reshape/check_doc_references.py` — 0 errors, 0 warnings;
  193 docs, 547 capability refs, 263 CLI refs.
- `git diff --check` — passed.
- Native `TimelineSession`/proposal snippets — Python compile probe passed.
- `python3 -m astrid timelines edit move --help` and `edit track-label --help`
  — documented flags/signatures present.
- `wc -w docs/architecture/timeline.md` — 401.

No full suite or browser/live-socket suite was run (docs-only task). No product
writer code, templates, scripts, R4 archive, integration worktree, or shared
dependency was modified.

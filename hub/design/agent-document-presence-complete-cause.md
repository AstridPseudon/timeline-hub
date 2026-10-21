# Complete document presence diagnosis

**DO NOT APPROVE** Agent `fa36a85f41aef1ff6270edc3b9e296b5c16c74e7`, tree
`83c3d869e2d82a3ae1bb2c2df07b5bd34ffef4f2`.
`astrid/sdk/timeline/document_diff.py` blob:
`07d456e3d4b1d0fdd3ac5f9e4384dc09be20a630`.

Diagnosis only; no product changes, HTTP, localhost, browser, or full-suite run.
The composed HTTP gate must remain held. Read the orchestrator PLAN and both
independent reviews (`agent-document-diff-presence-track-safety-review.md` and
`agent-document-diff-second-presence-safety-review.md`). Their blocking findings
are reproduced. There is no evidence requiring a settled architectural decision
to change.

## Exact cause

The input is a **complete authored document**, but the adapter validates it partly
as a sparse patch. Presence is lost in three distinct ways:

1. Held-field comparisons use `.get()`: absent and present-null become equal.
2. Collection/container readers supply `{}` or `[]`: absent and present-empty
   become equal before the held checks can observe them.
3. `_require_explicit_rows()` checks only keys still in the candidate row.
   A deletion from a parent config clip mirror is therefore invisible. The
   primary clip paths have `_check_clip_shape()` and native clear/refusal logic;
   the config mirror does not.

The fixes in `aba0346ae` and `fa36a85f4` repaired individual instances of these
patterns, rather than establishing exhaustive ownership of every authored
container and field. The first added a sentinel and fixed selected row/track
paths; the second fixed params/timing and the child internal held-field loop.
Neither applied the same boundary rule to parent/config held maps, registry,
empty containers, and mirror deletions. Their targeted fixtures principally had
populated collections and edited primary rows. Consequently **17 adapter tests
still pass while the counterexamples below fail**. This is an incomplete safety
boundary, not an equality-function, Runtime, or command-schema defect.

Checking only `commands != []` would be insufficient: an ordinary parent move
combined with `parent.presence_probe = null` succeeds with one `clip.move`, but
the opaque edit is still lost. Every requested authored change must either match
native replay, including presence, or refuse the whole candidate with draft kept.

## Reproduction and reachability

Executable probes are in
`ORCH/workers/agt-m2-document-presence-plane-cause-diagnosis-0634/test_presence_diagnosis.py`.
Here `ORCH` means
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.
The probes construct source revision payloads using main-suite `_closure()`,
recompute their immutable content digests, then call `open_authoring_bundle()`.
They do not manufacture a different candidate baseline after checkout.

| Changed authored input | Current adapter outcome | Local preflight evidence |
| --- | --- | --- |
| Parent opaque key absent -> null, and null -> absent | Success, zero commands | Candidate compiles and media plan validates |
| Parent.config opaque key absent -> null, and null -> absent | Success, zero commands | Candidate compiles and media plan validates |
| Child registry absent -> null, with valid parent asset fallback | Success, zero commands | Base and candidate compile; script media planner raises `AttributeError` on candidate |
| Delete `asset` only from parent.config.clips row | Success, zero commands; replay retains asset | Candidate compiles and media plan validates |
| Parent opaque null addition plus ordinary parent move | Success, one `clip.move`; opaque field absent in replay | Candidate compiles and media plan validates |
| Delete empty parent.clips, config.clips, config.tracks, parent.config, or child internal.clips | Success, zero commands | Each candidate compiles and media plan validates |

All diagnostic cases leave both caller candidate and Runtime base unchanged.
The 12 strict expected failures assert the required refusal; rerunning with
`--runxfail` confirms each fails at the explicit unrepresented-edit assertion,
not during fixture construction or compilation. Eleven have zero commands; the
mixed case has one move. These are compact branch representatives, not a frozen
document matrix.

Important distinctions:

- Parent/config opaque nulls are ordinary authored values. Their exact bytes are
  retained by `open_authoring_bundle` (authoring_bundle.py:351-352, 464-467), and
  `compile_authoring_candidate` copies the candidate parent into publication
  (1057-1058). They survive real local planning unchanged and are not read
  decoration or invalid injected roots.
- A missing child registry is a real supported source shape: main's
  `test_live_source_asset_authority_resolves_child_selector_without_local_registry`
  passes here. `_with_source_asset_authority` (554-571) merges fallback assets
  **only into a validation copy**, preserving authored registry absence. The
  probe puts both child selectors in parent authority before opening the bundle.
  Even the live-null candidate compiles through this validation view. However,
  `authoring_media.py:380` chains `.get()` on that null and aborts the script
  before the adapter. Thus the adapter counterexample is real, but **no normal
  script publication of this registry-null case is claimed**. An accidental
  exception is not the intended `DocumentDiffError` held-edit contract.
- Config clips are serialized authored parent content even when a matching
  primary clip collection also exists. The native recorder updates matching
  mirrors (`_recording.py:229-240`); it does not authorize ignoring explicit
  mirror edits. The compiler/media planner do accept the demonstrated one-sided
  field deletion. The command document verifier can additionally reject
  disagreeing populated mirrors (`commit.py:95-98`), but zero-command script
  success bypasses native command execution entirely. Refusal belongs before
  that success branch.
- Revision pins, `source_mapping`, `base_*`, outer shot-envelope metadata, and
  derived parent `occurrences` are not additional authored planes. Tampering
  with them is a pin/schema validation concern, not evidence that arbitrary root
  fields need a writer. Candidate parent `occurrences` is expressly refused by
  compilation. Deleting an id or duplicating a row already refuses in `_rows()`.
- `bundle_from_document()` (commit.py:149-162) opens exact immutable payloads;
  `fetch_bundle()` (store.py:629-645) copies the returned bundle. Neither invents
  missing child registry storage. Legacy `Checkout` flattening/intent migration,
  `_timeline` display fields, and read/render projections must not be used as
  the raw comparison baseline. This document script opens revision payloads
  directly (timeline_document.py:114-137).

## Complete seam inventory on fa36

Line numbers in this table refer to `document_diff.py` unless another file is named.

| Plane / normalization | Current coverage and remaining risk |
| --- | --- |
| JSON equality and `_field` (27-31, 49-51, 86-88) | `equal()` preserves dict membership and bool/number distinctions. The sentinel works when actually used. No global equality change is needed. |
| Pin/scope/placement checks (284-311) | Exact parent base and complete source placements are checked; membership/order and shot membership refuse. Optional `.get(..., [])` defaults can obscure missing empty placement envelopes, but those envelopes are required by compilation and are not an editable plane. Do not repin from a newer head. |
| `_rows()` (34-46) | Stable id, duplicates, and ordered membership checked. List/identity-map spelling is an explicitly admitted view representation; map `.values()` discards outer keys. Do not mistake that view spelling for native stored collection shape or claim malformed map-key tampering is an authored edit. Raw container presence must be checked before defaulting. |
| Parent non-config fields (420-426) | Union of keys is correct; `.get()` still collapses null/absence for **every held top-level field**, including opaque fields and registry. `clips`/`config` are excluded and need their own checks. |
| Parent.config (253-255, 437-446) | Outer absent -> `{}` and missing clips/tracks -> `[]` defaults erase container changes. Union held-field loop also uses `.get()` at each child key. Explicit null/non-map config can instead cause unstructured errors; it must be held visibly. |
| Parent primary clips (427-435, 447-449) | Membership/order and full raw `_changed_keys` shape checks protect row additions/deletions/opaque edits. Scalar emitter handles supported writes. Empty collection removal is hidden by `[]`. |
| Parent.config.clips mirror (444-446) | Membership/order checked, explicit added/null fields compared to native replay. Candidate **deletions** are omitted from row.items(), hence silently accepted. This applies to opaque, params, timing, selector, and other nonidentity row keys, not just `asset`; id deletion already refuses. |
| Parent tracks (258-280, 441-443) | Label edits/clears captured as `track.set`; raw changed unsupported keys refuse. Replay comparison preserves rename support. Missing empty tracks still normalize to `[]`. |
| Child clips (328-335, 370-380) | Identity/order, exact pinned row, and union raw row fields checked. Empty clips presence remains unguarded because clips is excluded from the internal held loop. |
| Params (66-72, 228-249) | Null/absence no longer collapses in initial field check; target null/missing refuses. Internal key set/value/clear uses membership, and opaque keys refuse. Later `{}` scratch values only calculate leaf edits. Absent/null -> empty object emits no params command but **already refuses** in final explicit-row comparison; do not report it as a surviving no-op or introduce an empty-object writer. Nonempty declared edits and key clears use the existing carrier. |
| Timing and hold (196-226) | `at/from/to` compare raw presence; target missing/null refuses. Parent trim `.get()` arguments are only native optional arguments after those checks; final replay must match explicit targets. Child trim remains held. Hold removal uses native clear, including a formerly present-null hold when a surviving source window permits it; setting hold to null refuses. |
| Child tracks and other internal fields (381-383, 413-417) | Tracks use `_field`; other held keys use union plus `_field`, so nested additions/deletions/nulls and opaque deletions refuse. Excluded **clips and registry** remain separate gaps. |
| Child registry (91-113, 384-387) | `_asset_rows()` normalizes absent/null/non-map registry/assets to `{}` for media discovery. The no-media branch then compares `.get('registry')`, hiding absence/null; registry is excluded from the held union. Inner registry/assets/entry changes are otherwise compared as complete dictionaries, retaining nested membership. |
| Media branches (150-160, 336-368, 390-412) | Deferred preflight restores only managed registry binding fields, then compares whole registry/payload; final path compares whole registry/payload to actual native replay. `_replace_registry_media` uses `old.get(key)`: when old lacks a managed field, restoring null can cause a conservative false refusal, not permission to erase raw storage presence. Presence-aware restoration should be audited, but no widening is necessary for this repair. All registry comparisons must preserve the outer tag. |
| Shot payload (116-147, 388-412) | Whole Mapping equality covers nested script/slot nulls, metadata, bindings, opaque fields. Deferred media normalization deep-copies and rewrites only present known string mirror leaves; unsupported differences must still refuse. Whole missing/null payload is malformed under compilation; `.get('payload')` is not evidence of an editable null payload root. |

Upstream/downstream defaults are distinct from authoring authority:

- `authoring_media.py:332-536` works on copies, normalizes local media locators
  into selected immutable media and bounded mirrors, and validates the candidate.
  Its registry/assets defaults are for selection/import discovery, not raw
  equality. Preserve this documented projection and its original input/draft;
  add a small structured refusal for explicit malformed registry/container input
  instead of allowing chained `.get()` exceptions. Do not merge fallback assets
  into authored candidate storage.
- Command state already has tagged `ABSENT`/`present(None)` (`_command_state.py:10,
  25-26, 291-323`), collection shape guards (`_collections.py:35-66`), recorded
  writes, and derived mirror writes. `ctx.object()` deliberately creates a params
  object for an actual native value write; that is a recorded command effect,
  not permission for the view to normalize all missing/null objects globally.
- `capture_move` (capture.py:222-232) creates/updates `app.astrid` timing intent,
  and the recorder updates matching parent mirrors. A blanket whole-row equality
  to the sparse explicit candidate would break these supported native outputs.
- `diff_authoring_candidate()` is useful feedback but **not** an acceptance
  oracle: `_diff_values` tolerates float noise, and `_keyed_rows`/placement logic
  transforms row representations. Its scalar Python equality also differs from
  native JSON equality. Keep exact raw checks with `equal`/presence tags here.

## One bounded correction plan

Repair the existing adapter and its immediate preflight validation, without any
new edit operation, DTO, schema allowance, or whole-document publication path:

1. **Tag containers before reading their members.** Check raw presence/type of
   parent.config, parent.clips, config.clips/tracks, and child internal.clips;
   compare pinned/candidate/replay container states before using empty lookup
   defaults. Keep accepted list/identity-map view spelling, stable ids and order.
   Storage presence changes without an existing native recipe visibly refuse,
   including empty -> absent and its reverse. Child tracks already does this.
   Reuse the existing tagged-state/collection-shape conventions, not a schema
   that declares unknown extension storage illegal.
2. **Use `_field` in all held-map comparisons**, including parent, config, and
   the child registry paths in both deferred/final branches. Compare unknown
   held fields over union keys, recursively through existing `equal`. Preserve
   `_same_alias_changes`, exact Runtime selections, and comparison to native
   media replay; never replace media validation with unconditional registry
   equality or drop registry from coverage again. Guard invalid container input
   in the media planner so it refuses clearly before any import/connection.
3. **Make the existing row result check baseline-aware.** Give it pinned rows;
   retain current explicit-field verification and additionally verify keys
   removed from the pinned row using `_field(candidate, key)` against
   `_field(replay, key)`. Apply at its child, parent, config-mirror, and track
   call sites. Native command-added fields absent from both pinned and candidate
   remain allowed, preserving move-generated timing intent. A requested deletion
   cannot be excused as a derived field. Held mirror-only deletion then refuses;
   supported primary hold/params/label clears still replay and pass.
4. Keep current deep-copy execution and error propagation through script
   preflight **before imports**, then final capture before commit. A supported
   edit combined with any unsupported presence edit must refuse atomically.
   Preserve the editable file and existing outbox retry identities. No generic
   root writer, broader scalar schema, empty-object command, or new receipt is
   required.

This covers the whole authored boundary by partition: placements are held as
complete ordered rows; shot membership is held; shot payload is compared whole
except bounded native media mirrors; child internal fields partition into
clips/tracks/registry/held remainder; parent partitions into clips/config/held
remainder; config partitions into clips/tracks/held remainder. Every partition
then observes both container presence and added/changed/deleted row keys. Native
command replay is the sole authority for allowed writes; unrequested command
outputs retain existing behavior. This closes omission paths even in nonempty
command batches without adding an independent root-diff framework.

## Repair tests and evidence

Move compact refusal representatives into existing main-suite adapter tests:
parent/config null addition and deletion, valid missing-registry fallback to
live null, empty authored-container removal/addition, config-mirror key deletion,
and a supported move combined with a held presence edit. Compare candidate/base
before and after refusal. Exercise registry cases with `defer_media=True` and
final capture; neither may equate absent/null. Include one native media rebind
with an unrelated held change, using existing exact-selection fixture helpers.
Retain original positives: parent move/trim, parent+child present-null hold clear,
declared `hello` value/clear and literal slot/script preservation, track rename,
same-alias selection/reload/undo/retry, opaque preservation, and exact pin checks.
Do not replace positives with refusals. Assert replayed tagged targets, not just
nonzero command counts. No huge Cartesian matrix or stored document snapshots.

Exact commands run from
`/home/user/work/wt/agt-m2-document-presence-plane-cause-diagnosis-0634`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py -k document_view_adapter tests/timeline/test_authoring_bundle.py -k 'document_view_adapter or live_source_asset_authority_resolves_child_selector_without_local_registry'
```

**18 passed, 47 deselected** (17 existing adapter cases plus the real registry
fallback case). No socket/HTTP test selected.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -rx -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-document-presence-plane-cause-diagnosis-0634/test_presence_diagnosis.py
```

**2 passed, 12 xfailed**, one unknown-integration-marker warning from importing
the existing fixture module outside repo test configuration. Strict xfails name
the complete-presence requirement; they are diagnosis artifacts, not gate passes.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q --runxfail --tb=short -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-document-presence-plane-cause-diagnosis-0634/test_presence_diagnosis.py
```

**12 failed, 2 passed**, exit 1, intentionally exposing all 12 unrepresented
edits at the probe assertion. The two passes distinguish already-refused empty
params and the registry-null planner exception. Inline read-only Python probes
also confirmed compilation/planning outcomes in the reachability table.
`git diff --check` passed; assigned worktree is unchanged at fa36. Probe lint:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check --no-cache /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-document-presence-plane-cause-diagnosis-0634/test_presence_diagnosis.py
```

**All checks passed.** Shared dependencies were read-only throughout. There is
no blocker to the diagnosis deliverable; the product remains unapproved.

Next: orchestrator assigns the single bounded repair above; worker runs the
targeted adapter/media/provider neighbors without transport, then independent
review checks the complete partition. Only after approval should the composer
resume its existing HTTP gate. This diagnosis does not certify authenticated
commit/reload, undo/retry, broader provider lanes, HTTP, or a full suite.

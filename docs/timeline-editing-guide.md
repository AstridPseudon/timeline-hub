# Code-driven timeline editing

For cross-product ownership and the canonical path, see [Timeline architecture](architecture/timeline.md).

The default flow is **inspect → capture a command → validate/preview → commit**.
Read the pinned Runtime head, then use a registered native command through a
`TimelineSession` or the matching CLI command. The session captures original
read/expect guards once, persists the exact request and retry identity in its
real outbox, and commits through Runtime's `/v1` door. Rendering,
visualization, and reopening the accepted closure are separate checks; a normal
edit does not require a render.

If the user says **“show me the preview, then save”**, preserve that order:
run the supported read-only visual preview for the pinned head, inspect/deliver
its actual output, then commit the command. A dry-run command validates
semantics but is not a visual preview. If the required preview is unavailable,
report that and do not claim visual proof.

## Accepted undo and unsent draft edits

Accepted history lives in Runtime. Keep the publication ID returned by a native
command commit. Python and CLI undo send a guarded inverse through the same
crash-safe outbox; redo reverses the **undo publication**, using its new ID:

```python
from astrid.sdk.timeline_checkout import Checkout

checkout = Checkout.open(project_id, timeline_ref, client=client)
undone = checkout.undo(publications=[publication_id], client=client)
redone = checkout.redo(publications=[undone["receipt"]["receipt_id"]], client=client)
```

```sh
astrid timelines undo TL --project PROJECT --publication PUBLICATION
astrid timelines redo TL --project PROJECT --publication UNDO_PUBLICATION
```

Both commands accept `--dry-run`, `--idempotency-key`, and `--json`. Repeat
`--publication` oldest first to reverse a group. Runtime checks intervening
writes and retains the original revisions. Reopen the timeline to read the new
head; publication undo leaves detached working copies untouched.

`checkout.undo()` / `redo()` without publication IDs, and the CLI equivalents
without `--publication`, operate on unsent draft edits. Their snapshots stop at
the draft's published base, so an old file is never used to restore accepted
history. New unsent edits on that base remain locally undoable.

The legacy cut sheet still edits a detached draft. `apply_sheet(checkout, text,
client=client)` can recover an older sheet's basis from retained Runtime
revisions; local snapshots and exported copies are used only within the current
base. It does not publish or restore an accepted revision. `apply --native` is
available only for sheet operations already covered by the native adapter. The
remaining sheet three-way merge and detached-draft publication are held for
migration; do not use them as the general timeline writer.

## Shared timeline and shot contracts

`@banodoco/timeline-schema` owns `TimelineConfig` and timeline clip semantics.
Workspace Runtime's `contract/schemas/shot-composition.json` owns the outer
shot publication envelope (revision identity, head/CAS, dependencies, and
occurrences) and references the generated canonical config schema for nested
timelines. The Runtime schema also marks its managed-media registry as a
Runtime-owned extension. Consumers project these contracts into their local
views; they do not define a competing `TimelineConfig`.

Shot audio is optional. Child timeline audio clips and their bindings are the
playback authority; a legacy aggregate `audio` descriptor may be read when
present, but is neither required nor synthesized. Shot payloads remain open to
unknown fields so app-specific data survives a lossless read/edit/publication
round trip. New writes use top-level `name`; readers may fall back through
legacy provenance/metadata names and finally the stable shot identity. Media
kind comes from Runtime's managed-media metadata and stays `unknown` when that
identity is missing or unrecognized; a missing kind never implies `image`.

Visible clip duration is the selected source duration divided once by positive
`speed`: `hold`, transport `duration_ms`, or source trim `to - from` supplies
the source duration. Parent occurrence `duration_ms` caps the resulting visible
interval. Source trims remain in source units, and the renderer owns final frame
rounding against the shared conformance vectors.

The Astrid App editor reads the exact canonical Runtime head. Empty canonical
compositions remain canonical; a failed read shows an error and never routes to
legacy shot groups. Legacy mode is explicit and is selected only when the
canonical adapter is absent. Retry refreshes the pinned Runtime snapshot while
preserving the separate local draft, and publication uses expected-head CAS.

`open_composition` is a read-only inspection projection. Native editing uses a
`TimelineSession` opened for the same project/timeline; it resolves the exact
base head, captures original guards, and persists the in-flight request in the
session's outbox. Whole-bundle mutation remains a held legacy capability while
the remaining edit families migrate.

## Extension data and repeatable passes

The shared schema provides open maps for application data, so a timeline can
carry a small processing ledger without a parallel document or a new schema.
Use the narrowest scope that matches the meaning of the value:

- timeline-wide structure: `candidate["parent"]["config"]["app"]["structure"]`
- one shot/revision: `candidate["shots"][shot_id]["payload"]["metadata"]`
- one occurrence: `candidate["placements"][i]["provenance"]`
- one internal clip or effect: its `app` or `params` map

`config.app.structure` is the schema's intentional timeline extension point. A
direct `config.structure` field is rejected by `TimelineConfig`. Shot payloads
are open so application metadata survives a lossless read/edit/publication
round trip, while the common timeline schema still governs known structure and
timing fields. The editor may not display arbitrary keys until a UI projection
is added. Keep agent-owned values under a namespace such as
`metadata["delivery"]`; if one shot revision is reused by two placements, put
different delivery state under each placement's `provenance`.

### Example: inspect every placement

`timelines show` (or `client.timelines.open_composition`) is the canonical
current-head read. It gives ordered occurrence IDs, names, timing, tracks, and
the pinned head. The read projection is not editable. Keep extension maps in
the projection only until the relevant native command exists; the current
command registry does not make arbitrary metadata writes command-backed.

```python
shown = client.timelines.open_composition(project_id, timeline_ref, detail=True)
assert shown.ok
inspection = shown.data
report = []
for placement in inspection["placements"]:
    shot = inspection["shots"][placement["shot_id"]]
    for clip in shot["internal_timeline"].get("clips", []):
        report.append({
            "occurrence_id": placement["occurrence_id"],
            "clip_id": clip["id"],
            "track": clip.get("track"),
            "at": clip.get("at"),
            "from": clip.get("from"),
            "to": clip.get("to"),
        })
```

For a supported native edit, use the session or its CLI adapter. `move` captures
the original selection/read/expect guards once; the persisted flight keeps the
same request and idempotency key across a lost acknowledgement or restart:

```python
from astrid.sdk.timeline.sync import TimelineSession

session = TimelineSession.open(project_id, timeline_ref, client=client)
result = session.move("parent/clip:opening", 1.5, idempotency_key="edit-42")
publication_id = result["receipt"]["receipt_id"]
```

For a registered command that is already captured, use `session.commit(command)`
or `session.commit_many(commands)`. Supplied claims are verified against the
original base; they are never refreshed from a newer head. A stale or
unsupported command stays in the outbox for inspection rather than becoming a
whole-document fallback.

Producers do not write the timeline directly. After Runtime settles a proposal
and returns its requester/attempt pin, the requesting client queues that exact
proposal and flushes it through the same outbox:

```python
session.queue_proposal(settled_proposal)
result = session.flush(idempotency_key="proposal-42", via="producer")
```

`queue_proposal` preserves the proposal's original target, guards, rationale,
and command identities. It refuses a different project/timeline or pending
local intent. A proposal artifact or dry run is not a publication receipt.

### Renderer and skill boundary

Remotion is a visual proof path, not a timeline authority. Use the pinned
native head with `timelines visualize`; it does not turn an unsupported
candidate mutation into a supported write. Production orchestrators remain in
`video_editing`; canonical timeline authoring, visualization, effects, and
Remotion rendering remain in `timeline_editing`. The source directory and
runtime capability IDs stay `rendering` for compatibility.

## Read the live timeline first

Use the connected Runtime for discovery and readback. `timelines show` is the
native structural/text operation. For declared visual placement, use its
sibling native Runtime operation:

```bash
python3 -m astrid projects current --json
python3 -m astrid timelines show [--project <project>] [<timeline>] --json
python3 -m astrid timelines visualize [<timeline>] [--project <project>] \
  --mode inputs --format md --format png --occurrence <occurrence-id> --json
```

Explicit scope wins. If it is omitted, the Runtime uses the workspace current
project and that project's `metadata.default_timeline_id`; it does not infer a
timeline from names or list order. A missing selection is an actionable error.

Pin the head returned by `show`, then carry the exact `occurrence_id` returned
by the live response into any input view or later focused inspection. Do not replace
it with a shot name, ordinal, fixture alias, seed-map entry, or a nearby
occurrence. The input view describes declared placement and timing; it does
not prove source pixels or a composited render.

`timelines visualize` is the one visual-inspection operation. Its default
`auto` mode reuses a fresh matching render or captures the requested composed
frames from the pinned composition when no render exists. Use `--mode inputs`
for declared inputs without any renderer work. `--mode composed` requests
composed pixels; `--frame N` selects one exact frame, and `--revision-id ID`
keeps historical/current authority explicit. The returned evidence reports
whether frames were reused, freshly captured, or served from cache. Agent conclusions must come from live
Runtime responses and returned artifacts, never from fixture/evaluator JSON,
baseline exports, or prior result files.

For Python callers, open an authenticated client and a `TimelineSession` in the
same connected environment as the shell command. Importing the SDK does not
connect it. Use the supplied connection explicitly; never guess credentials or
inspect private Runtime storage to recover them. The session's default outbox
is durable; pass `outbox_path` only when a separate, explicitly scoped outbox
is required.

```python
from astrid.sdk.timeline.sync import TimelineSession

session = TimelineSession.open(project_id, timeline_ref, client=client)
result = session.trim(
    "parent/clip:opening", out_s=3.0, idempotency_key="trim-opening-42"
)
assert result["receipt"]["command_kind"] == "timeline.commit"
print(result["data"]["show_command"])
```

Important defaults are explicit:

- Clip intervals are half-open `[start, end)` in the containing timeline.
- Use `quantize_interval(start, end, fps, policy=...)` when boundaries are not exactly representable; it reports requested/applied frames and rejects collapsed intervals.
- Absolute placement does not move neighbours. Ripple is never implicit.
- If shifting following visual clips is intended, group a `clip.trim` endpoint
  change with recorded `clip.move` commands for later siblings on that track.
  Leave audio, voice, music, and other tracks unchanged, and state the
  parent-duration extension policy in the command group.
- `duplicate`, broad `replace_media`, reorder, arbitrary metadata, and
  whole-occurrence transforms remain authoring-bundle capabilities, not
  command-backed writes on this base. Keep those changes as a draft and report
  the limitation; do not publish them through a whole-document writer.
- Media import/list/open use the existing Runtime media services. Source viewing
  and composed preview are separate, read-only actions. Unsupported renderer
  capabilities and missing assets must be reported before commit.

## CLI native edits and legacy working-copy checks

Native edits use the command registry and the same guarded session/outbox as
Python. Read the exact selector from `show` first:

```bash
python3 -m astrid timelines show <timeline> --project <project> --json
python3 -m astrid timelines edit move <timeline> --project <project> \
  --clip parent/clip:<id> --on 1.5 --idempotency-key move-42 --json
python3 -m astrid timelines edit track-label <timeline> --project <project> \
  --track parent/track:<id> --set "Dialogue" --idempotency-key label-42 --json
```

`edit move`, `edit track-label`, and native literal trims capture original
guards and use a fresh caller key for a new intent. Repeating the same command
with the same key retries the persisted request; it does not recapture against
a newer head. `--dry-run` validates without accepting a publication.

The remaining detached working-copy surface is retained for capabilities that
have not migrated:

```bash
python3 -m astrid timelines status <timeline> --project <project>
python3 -m astrid timelines checkout <timeline> --project <project>
python3 -m astrid timelines edit <timeline> --project <project> --replace-line vo-1 --take vo/vo-1.wav --words vo/vo-1.words.json
python3 -m astrid timelines edit <timeline> --project <project> --insert-line vo-2 --after vo-1 --take vo/vo-2.wav --words vo/vo-2.words.json
python3 -m astrid timelines edit <timeline> --project <project> --from-script script.json
python3 -m astrid timelines check <timeline> --project <project>
python3 -m astrid timelines publish <timeline> --project <project> --idempotency-key edit-42
```

`status` reads the current published head and, if present, the selected
working copy's base, changed paths, and validation result. It does not create a
working copy or render. There is no passive timeline-scoped latest-render
reader in this CLI, so `status` does not claim render state. A working copy
based on an older head is reported with `head_moved: true` and should be
reconciled before using its legacy publish path.

`checkout --fresh` refreshes the selected working copy from the current head.
If that copy has edits, the CLI refuses to replace it; choose a new name with
`--draft recovered --fresh` to keep the old draft available. `edit` can also
apply `--replace-line`, `--insert-line`, or a JSON `--from-script` using the
existing SDK operations and local take/word-timing files. Repeat
`--gap-after LINE=SECONDS` to declare multiple line gaps.

`publish` remains the legacy detached-draft/whole-candidate writer and is held
pending migration. Its three-way merge, `--force`, and broad Checkout mutation
surface must not be presented as the native command path. Use it only when the
requested edit is explicitly within that legacy capability, and report that
limitation; otherwise refuse visibly and keep the draft. `apply --native` is the
only sheet publication route currently migrated for its covered operations.

```bash
python3 -m astrid timelines check <timeline> --project <project> --sweep
python3 -m astrid timelines edit <timeline> --project <project> --clip <clip> --nudge-frames 1 --sweep
python3 -m astrid timelines log <timeline> --project <project> --verify --json
```

`check --sweep` validates a saved working copy and compares bounded samples across every cut. Sweep status is 0 for expected results, 1 for unexpected picture changes, and 2 when capture was not made; a validation failure returns 1. Without a saved working copy, `check` prints a checkout hint and does not sweep.

A changed edit saves the working copy before sweeping. The sweep runs after a reflow, when more than three cuts changed, or with `--sweep`. `--no-sweep` suppresses it, including when both flags are supplied. An unchanged edit reports no change, returns 3, and does not sweep. These bounded samples do not prove every-frame or audio identity.

`log --verify` checks the journal hash chain. A broken chain returns 1; JSON reports `error.code: validation_error`. A missing journal is reported as “no journal yet” and returns 0. Journal queries accept `--since`, `--actor`, `--op`, `--cut`, `--clip`, and `--outcome`; a query validation error is printed to stderr and returns 2.

## Preview before a native edit

Use the pinned read-only visualizer when a composed preview is requested, then
commit the unchanged native command. A native `--dry-run` is useful for command
validation, but it does not render pixels or create a publication:

```bash
python3 -m astrid timelines visualize <timeline> --project <project> \
  --revision-id <revision> --mode composed --json
python3 -m astrid timelines edit move <timeline> --project <project> \
  --clip parent/clip:<id> --on 1.5 --dry-run --json
python3 -m astrid timelines edit move <timeline> --project <project> \
  --clip parent/clip:<id> --on 1.5 --idempotency-key move-42 --json
```

The detached authoring-bundle preview/render helpers remain available for
inspection and specific render workflows, but their whole-candidate publish
writer is held on this base. Do not use a frozen candidate digest as a native
commit key or claim that it gives the session's original guards. If a required
preview is unavailable, report that limitation before committing.

## Opening sources and returned artifacts

Keep these identities distinct: a clip's `asset`/`asset_id` is a timeline-local
registry alias; a managed media ID identifies a project media record; a
`source_object_id` identifies managed bytes; an artifact handle identifies a
returned view or run output. Resolve the selected clip through its owning
registry or returned source metadata. Never pass a display alias to an API
that asks for a managed ID, or construct an artifact URL from an alias/digest.

For a returned, non-null source object, the connected SDK can retrieve bytes
with `client.media.read_bytes(source_object_id)`. Read/open only the selected
source needed for the task. Media metadata alone does not prove that its bytes
were viewed or played. A missing source object is an explicit access gap.

CLI responses can use `ok/data/error/receipt` envelopes, while bound authoring
helpers return plain candidate/receipt data. Check success and inspect the
documented payload level before selecting nested fields; do not assume every
operation returns the same top-level shape. Use returned verified local paths
with the host's file/image/audio tools when available. An `artifact://` value
is not a filesystem path, and a host's numeric artifact reader may not accept
Astrid's digest-based artifact handle. If no compatible opening action or
materialized path is returned, report that access limitation; do not invent a
URL or claim to have inspected the artifact.

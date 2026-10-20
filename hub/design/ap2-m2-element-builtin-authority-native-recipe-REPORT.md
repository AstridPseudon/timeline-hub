# AP2 M2 built-in owner-pinned overlay native recipe

## Result

**Unsupported on the current native tuple.** No App source was changed and no
owner-pinned consumer was activated. The normal catalog already carries the
right identity tuple and definition schema, but the existing native add/set
carriers do not bind that tuple to the authoritative built-in definition.
Using them as-is would make a false-positive overlay journey.

The correct handoff is a bounded Agent/Viewing/Runtime peer request using the
existing `clip.add`, `clip.set-params`, and `clip.delete` carriers. It requires
no new operation, DTO, store, endpoint, public pin, synthetic catalog, or
`projectDocumentPin` fabrication.

## Exact sources inspected

| Source | Commit / tree or package | Status |
| --- | --- | --- |
| App current integration | `a11dd7a91` | read-only current Main |
| Agent public 0.2.13 floor | `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff` | read-only |
| Runtime public 0.2.13 floor | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18` | read-only |
| Agent private full-carrier floor | `357230816c86da65d5f8cc92b10a3a90d29874e0` / `94692ec85167d5c606626c4ec678fe2a63ee0aa6` | read-only, schema `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3` |
| Agent private project-data floor | `e010e6a3868e963471244491bb6672c3e4a5135e` / `70414cf6875d2c97c45f33e0a5158c80bd7391d9` | read-only, schema `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |

The relevant `ElementRef`, `ClipAddArgs`, `ClipSetParamsArgs`,
`ClipSetElementArgs`, and `DocumentPin` definitions are byte-equivalent across
the public and both private floors for this question. The private floors add
other operations and a capture-version change; they do not add built-in
element authority to these carriers.

## Main normal catalog

The checked-in normal public payload is the generated
`vendor/astrid-build-inputs/public/astrid/packs/rendering/elements/public-catalog.ts`
projection consumed by `src/pages/Home/astrid-public-host.tsx` and then by
`VideoEditorProvider`.

It contains 12 published entries: six `rendering` animations, two `rendering`
effects, two `rendering` transitions, and two `local` effects. The relevant
overlay entries are:

| kind | id | packId | revision |
| --- | --- | --- | --- |
| effect | `audio-reactive-colour` | `rendering` | `sha256:b05ba83a03c60c94acfbde56d04b8b46d76b4e7c6982612c5c9b7a5e9ccd23f1` |
| effect | `end-spanning-layer` | `local` | `sha256:c733005d69971aef4b2c9934c1bede159b4695a9004023a863fcb6bd27a309b8` |
| effect | `frame-overlay` | `local` | `sha256:e22e45f1c65f92721cfc3b9d84ed2a137b50e9b2e3552ae9c176aa385ab9fb18` |

Each entry includes `schema`, `defaults`, `source`, `componentPath`, and
renderability. `buildAstridAgentElementContext` preserves `(kind, id,
packId, revision)` and the host resolver requires the same owner tuple. The
App therefore has legitimate owner-pinned catalog data; stripping `packId`
would discard catalog ownership and is not a valid migration.

Project custom packs remain separate: `admittedCatalogEntries` supplies their
owner-qualified refs, and `refreshAdmittedElementRef` uses the official
provider/admission lookup. This request does not merge custom packs into the
normal catalog or replace that lookup.

## Why the existing carriers are insufficient

The public Agent/Runtime schema says:

- `ElementRef` has optional `packId` plus required `id`, `kind`, and
  `revision`, with no definition/schema payload.
- `clip.add` has only `args.row`; the row requires `id`, `clipType`, `track`,
  `at`, and `hold`, then permits additional JSON. Thus `row.elementRef` can be
  transported, but current Agent `clip_add` treats it as an opaque row field;
  it does not resolve the exact built-in definition, check its revision, or
  validate `params` against that definition.
- `clip.set-params` carries literal `values`/`clear` and optional
  `schema_source: DocumentPin`, but no element reference. For an existing
  owner-pinned ref, Agent routes to `_selected_schema`, which requires scoped
  project-pack inputs and `schema_source`. Without an owner-pinned ref, it
  falls back to `element_schema(clipType)`, which proves only a clip-type
  schema, not the exact `(packId, kind, id, revision)`.
- `clip.set-element` carries `elementRef` and optional `schema_source`, but it
  requires an existing element ref, forbids changing id/kind/selected owner,
  and routes any owner-pinned ref through selected project-pack authority. It
  cannot create the overlay and cannot be used as a built-in catalog proof.

The concrete native implementation matches the schema: `clip_add` records the
literal row and creates it; `clip_set_params` reads the clip identity and
validates either the selected project schema or clip-type schema; and
`clip_set_element` requires an existing ref and selected schema inputs for a
`packId`. Runtime 0.2.13 publishes the same generated shapes. Private 613/392
do not change these facts.

The App currently confirms the same boundary: `ElementsLibraryPanel.tsx`
enters `elementOverlay` only when an effect has no `packId`; a normal built-in
therefore goes through the old `timeline.apply_element` adapter. The native
`buildElementOverlayRow` can preserve a full ref, but no current native
consumer gives that row exact built-in definition authority.

## Exact peer request (no new wire surface)

Use the existing carriers and existing Agent dependency/record machinery. The
requested scope is only a parent-owned visual overlay effect whose row has an
exact owner-qualified `elementRef`:

```json
{
  "elementRef": {
    "packId": "rendering-or-local",
    "kind": "effect",
    "id": "audio-reactive-colour",
    "revision": "sha256:<exact-64-hex-revision>"
  },
  "clipType": "audio-reactive-colour",
  "track": "<active-visual-output-track>",
  "at": 0,
  "hold": 1,
  "params": {}
}
```

The example is illustrative only; the accepted source must come from the
official catalog/provider lookup, never from a fabricated descriptor.

### Agent contract

1. **Before / capture**

   - Resolve the exact built-in `(packId, kind, id, revision)` through the
     official installed catalog/registry and obtain the immutable definition
     schema. Reject missing, stale, wrong-kind, wrong-owner, unpublished, or
     ambiguous refs before any draft mutation.
   - Keep custom project-pack refs on the existing `schema_source` plus scoped
     admission path. Do not treat a custom pack as built-in and do not accept
     an unowned literal as an owner-pinned substitute.
   - For `clip.add`, capture the authored parent source pin, active visual
     output track leaves, parent clip membership/order, target-id absence, and
     the exact definition dependency/binding using existing records. Validate
     known `params` against the resolved definition without coercing or
     normalizing unknown JSON.
   - For `clip.set-params`, capture the stable scoped clip, its original
     `elementRef` including owner and revision, the exact before state for each
     changed/cleared top-level param, and the same exact definition dependency.
   - For `clip.delete`, capture the complete original row and stable parent
     membership/order. The stored original owner-qualified ref is the restore
     authority; deletion must not silently re-resolve to a newer catalog row.

2. **Declared intent**

   Use the existing empty intent `{}`. No ripple, anchor following, occurrence
   ownership, inferred track, or catalog substitution is allowed. `clip.add`
   selects `parent`; set/delete select the stable `parent/clip:<id>`.

3. **Apply**

   - Add exactly one complete row with the owner-qualified `elementRef`,
     `clipType` matching the effect id, literal `at`/`hold`, and supplied
     params. Preserve the existing active-output-track, unsupported-media, and
     unsupported-timing refusals.
   - Set only literal top-level `params` values/clears through existing
     `clip.set-params`; require the original element owner/id/kind/revision to
     remain unchanged. Do not use `clip.set-element` to create or replace a
     different owner.
   - Remove through existing `clip.delete`; do not rewrite the row, strip its
     owner, or clear unrelated fields.

4. **After**

   - Add leaves the exact row as authored, records the created stable identity,
     and preserves all parent/config mirrors as the existing literal add
     recipe does.
   - Set changes only the named params and explicit clears; `elementRef`,
     `clipType`, timing, track, opaque roots, and unknown siblings remain byte
     identical.
   - Remove leaves the target absent and records the full original row for
     guarded inverse/replay. No unrelated clip, track, catalog, or custom-pack
     data changes.

5. **Original pin, owner, opaque data, inverse, retry**

   Preserve the original exact element ref and owner in reads/definitions and
   the existing command record; never strip `packId` or replace it with a
   synthetic literal. Preserve every opaque/unknown row and param value.
   Existing `expect`, `reads`, `selections`, `bindings`, `created`, inverse,
   replay, and Runtime idempotent retry must prove the same command. A changed
   definition revision, owner, target membership/order, original row, or
   changed payload under the same retry identity must refuse before writes.
   A→B→A must remain an inverse refusal where the existing guarded inverse
   machinery requires it.

### Viewing contract

The Composition/App host must resolve the exact tuple `(packId, kind, id,
revision)` from the official catalog for preview/export. It must reject an
owner mismatch and never fall back by bare id. Existing custom-pack admission
remains the only source for custom components; no synthetic normal catalog
entry or owner-stripping compatibility alias is allowed.

### Runtime contract

Runtime should keep the existing public command schema and generated DTOs,
accept the Agent-produced existing-carrier records, and qualify one matching
private pair before any consumer activation. No new endpoint, store, request
field, or public pin is needed. The qualification must prove exact accepted
record/bundle, atomic refusal before writes, changed-payload retry refusal,
lost-ack/idempotent retry, reload/replay, and guarded inverse for add/set/delete.

## Required proof before App activation

Agent direct native tests should add one real normal-catalog built-in row
(using the exact `audio-reactive-colour`, `end-spanning-layer`, or
`frame-overlay` tuple), one wrong-owner/revision/schema refusal, exact params
set/clear, full-row delete/inverse, opaque preservation, and retry/replay
checks. Viewing should add exact tuple resolution and wrong-owner refusal
neighbors. Runtime should run the matching generated-contract/provider tests
on one private Agent/Runtime pair.

Only after that counterpart is reviewed and qualified may App add the real
Elements Library click and mounted Properties Panel delete through the native
overlay/session/outbox. Until then, `D01-app-element-routes` remains open and
the current owner-pinned legacy adapter behavior must remain intact.

## Verification

Targeted App neighbors, unchanged:

```text
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs
NODE_OPTIONS="--require=$RUNNER" TMPDIR=/tmp node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/runtime/element-adapter.test.ts
```

Result: **4 files, 97 tests passed**.

No browser, localhost, live socket, full suite, dependency install, public
pin, artifact generation, or native private-pair run was performed. No App
source diff was created. The report is the requested precise peer handoff, not
a claim that the native recipe is qualified.

# Theme first source: project-authored Document, explicitly selected by the film

> **DEFERRED — owner ruling 2026-10-21 02:04 UTC.** This Runtime proposal is
> historical design evidence, not an M0–M4 requirement. It must not hold
> current save, render, or peer work. M0–M4 uses the ordinary Main path:
> `media.import_file -> project CAS -> inputs.theme -> theme.json -> ONE resolver -> props.theme`. Ordinary proof is green; canonical positive proof
> remains red pending `rt-m3-main-theme-canonical-caller-reconcile`, and this
> does not claim physical parity or current canonical positive green. Preserve
> the constraints and evidence below; do not implement this first-source,
> private, provenance-only contract. See [the ordinary-versus-canonical proof
> distinction](handoff-rt-m3-main-theme-canonical-caller-reconcile.md).

Status: **DEFERRED historical proposal; not implementation authorization**.
2026-10-21.
Supersedes the source/delegation assumptions in
`runtime-theme-private-mode-concrete-proposal.md`; leaves PLAN decisions intact.

## Historical decision request (deferred; no response needed)

Approve one bounded semantic change: a project writer may define the original
Theme through existing project Document CRUD, and a guarded film EditCommand
may select its exact DocumentPin in `parent.config.app.astrid.themeSource`.
Only that accepted selection authorizes Runtime to capture the Theme for a
managed invocation. Use a private **root invocation**, never a delegated child,
of the existing `rendering.render` capability to produce the resolved bytes.

This is the recommended option. It changes explicit source selection from a
portable label to an exact project-authored document dependency. It does not
claim an installed slug, arbitrary CAS object, browser-resolved JSON, transport
receipt, or nonexistent host Theme directory was already authoritative.

## Existing seams and the precise missing semantics

Source reviewed: Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, local Agent
`4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`, local App
`692765846fef511047445fecef3e55ec8bb6a5bf`. Remote manager findings remain the
authority for their newer trees; these local source reads establish carriers,
not a currently qualified cross-repository tuple.

| Actual source/type/path | What it supplies |
| --- | --- |
| Agent `astrid/sdk/documents.py:217` `Documents.create(kind, content, project, ...)`; Runtime `runtime_protocol/server.py:701-722`, `service.py:4439-4522` | Existing project-scoped Document create/read/versioned update, authorized with existing `projects:write`. No Theme-specific endpoint is necessary. |
| Agent `astrid/core/theme/_schema.py:237-264` | Existing full Theme validator and absolute runtime `theme.json` reader. |
| Runtime `timeline_commit_types.py:47`, `timeline_commit_port.py:302-324,515-551`, `timeline_commit_inputs.py:424-465,617-629` | Exact three-field DocumentPin; current or reachable retained `.config` source reads; same-project validation and retained `source` dependency links. |
| Agent reviewed private source `e010e6a3868e963471244491bb6672c3e4a5135e:astrid/sdk/timeline/_project_data_commands.py`, `commands.py`; App `src/tools/video-editor/commands/projectDataMember.ts` | Existing bounded `project-data.write`, replacing exactly `parent.config.app[target][key]` with original guards/inverse/rebase. This is private-source precedent, **not an operation available in the local ordinary Agent union**. |
| Runtime `capture_validation.py:24-99,120-161`, `store.py:_freeze_managed_render_inputs` | Saved/candidate verification against retained closure; candidate document pins must equal those retained by its saved base; exact config/registry freeze. |
| Agent `generic_host.py:6888-6904,7087-7160,8261-8276,9554-9577`; `generic_host_worker.py:157-170`; rendering `pack.yaml:904-907,1030-1035` | Existing named `theme` materialization and private request/result byte carriers, declared `provenance` file output, typed-output validation. These are custody, not first-source authority. |

The current project-pack admission is deliberately **not** used as an invented
Theme catalog: Agent `astrid/core/element/project_packs.py:_definitions` and
`admit_project_pack` accept rendering elements and require at least one;
Runtime `timeline_commit_inputs.py:_project_pack_source` restricts admissions
to effect/animation/transition. A Theme-only source has no existing member
there. A generic `.config` Document already has the appropriate source carrier.

## Original admission and normal user workflow

The admitting principal is a human or agent acting as an authenticated project
writer, through `client.documents.create`, with the existing project scope.
Neither the rendering worker nor catalog read access grants that authority.
The original definition is `content = {id, visual}`, validated with the existing
Agent Theme validator; use kind **`astrid.theme.config`**. This kind's Theme
meaning is proposed here; existing generic `.config` plumbing already carries
it. Its ID is the normal returned `document:<uuid>`, not a reserved filesystem
path, magic Theme root, slug-derived lookup, or new Document envelope.

The writer explicitly authors/imports this original definition. The SDK checks
it before create; selection must validate it again so bypassing the SDK cannot
admit an invalid film dependency. Runtime's canonical Document content, version
and verified digest are the byte authority. Whitespace in an import file is not
retained as identity. A caller-provided hash is only a claim to verify.

**Before:** a user asks the agent to use a Theme label; the film retains
`config.theme`/`theme_overrides`. App's installed TypeScript value can drive its
preview (`compositions/installed-themes.ts:12-105`); Agent's resolver does not
look up that slug and uses its builtin when no runtime input exists. The App
ThemeChip is read-only (`components/ThemeChip.tsx:18-32,134`), not a picker.

**After:** the project writer defines/imports the original Theme using existing
Documents.create; the film remains unchanged. The requesting editor then
commits the returned exact pin to the film through guarded `project-data.write`:

```json
{
  "op": "project-data.write", "version": "1", "select": "parent",
  "args": {
    "target": "astrid", "key": "themeSource", "mode": "replace",
    "value": {"document_id": "document:<returned-id>", "version": 1,
              "content_digest": "sha256:<verified-content-digest>"}
  }
}
```

This shows the semantic member only; the normal command envelope and original
capture guards remain mandatory. The new rule for this one namespace key is
that it is a typed source reference, not opaque decoration. Agent hydrates it
through `port.config_source(pin)`, validates the complete Theme and records an
exact `source` dependency; Runtime revalidates live first use under acceptance
and retains its bytes/pin with the accepted revision. Same-leaf conflicts,
absence/null distinctions, inverse/redo, and old/new pin retention apply.
Malformed values refuse; no fresh pin may enter through inverse/restore or a
generic patch without the same validation. Other namespace keys stay opaque.

This requires a bounded semantic addition to the reviewed project-data member
and its provider hydration, plus its normal eventual union adoption; copying
JSON into the namespace today would not implement this contract. No new
command name, writer, provider or store is proposed. No generation/adoption is
authorized by this document.

Catalog update from V1 to V2 cannot change a film selected at V1. Applying V2
requires another guarded film command. Once present, `themeSource` selects the
base Theme; legacy `config.theme` remains historical label data and cannot
override the pin. Read surfaces show the selected document's ID. Existing
`theme_overrides` remain authored overrides. Unbound explicit historical labels
are not silently migrated or certified: the writer must supply and select the
intended original definition. The implicit public default remains as settled
in PLAN. No browser-resolved/merged value is imported automatically as a base.

## Exact capture and private invocation contract

1. The requesting client, using its existing task submission authority, asks
   for preparation and then final rendering through the existing managed
   invocation. These are two ordinary root task admissions with distinct retry
   keys, not parent/child tasks. The SDK may wrap these calls; the worker never
   admits the second task or receives project-write/task-creation privileges.
   Proposed plain task input `theme_prepare: true` requests preparation only;
   it is untrusted intent, not the trusted dispatch mode or source selector.

2. Runtime first verifies the normal saved revision/publication selector, or
   the real closed `authoring_preview.candidate` plus its retained base, using
   existing capture validation/projector. It extracts `themeSource` from that
   verified frozen config, not from separate requester Theme data. Saved input
   must have that pin in its retained dependency manifest. A candidate must
   keep the base's selected Theme pin and retained document set: selecting a new
   source must be committed first; unsaved ordinary edits/overrides may follow.
   Candidate-less working copies and CAS-only captures remain UNCERTIFIED.

3. Runtime reads that exact retained `.config` content, verifies project/kind,
   pin/digest and bytes, and publishes its canonical UTF-8 JSON through existing
   managed CAS ingestion. Call the raw original object **B**. This is the first
   Theme object, produced from an actual authorized document read, not assumed
   to exist beforehand. Runtime derives the existing named `theme` descriptor
   from B and appends B to its derived ordered inputs; callers cannot insert B
   through the currently media-only ordered-input equality check. Freeze that
   derived descriptor with the normal config/registry, selector/candidate/base,
   capability/source identity, facts/profile and idempotency authority.

4. Proposed trusted mode: Runtime writes
   `_runtime_render_admission.theme_mode = "prepare-v1"` in its existing
   protected admission object. `store.py:create_task` already reserves this
   object; its Theme member is an **addition requiring agreement**. Reject
   attempts to supply the marker through public body/spec/nested inputs. The
   GenericHost derives dispatch exclusively from the claimed admitted spec,
   passes it through its existing serialized `admission` process carrier, and
   adds this case to its private runtime context. No delegated fields or child
   policy are set. `run_id=None` inside the private action and existing worker
   result custody do not remove the outer task/attempt/run/fence association.

5. For exactly this admitted capability/mode, host-private dispatch calls the
   existing `_resolved_theme_for_render(frozen_timeline_path, B_theme_path)`
   once, validates its complete `{id,visual}`, and writes canonical finite JSON
   (sorted keys, compact separators, UTF-8, no extra newline) to the existing
   declared `provenance` file output. No renderer is invoked. Preserve declared
   port, containment, hash, byte-count, source and lease checks. For this mode
   alone, require exactly that result instead of video; all ordinary renders
   still require video and retain ordinary renderer provenance semantics.
   This private branch does not exist today; `_invoke_internal_result` or an
   `ASTRID_INTERNAL_INVOCATION` environment value alone never selects it.

6. Existing `settle_attempt`/managed-output association settles resolved object
   **R** under that preparation task/attempt/project. The client forwards only
   the preparation task ID as proposed plain task data
   `theme_preparation_task_id` on its final normal request. Runtime rechecks the
   completed preparation association and its stored admission: B/pin, exact
   selector or candidate/base, frozen config/registry, facts/profile and source
   identity must all equal the final request's verified authority. Rehash R,
   check complete valid Theme bytes, and derive final named `theme=R` itself.
   A guessed task ID, foreign output, unfinished/stale attempt, changed config
   or arbitrary descriptor is insufficient. A changed frozen tuple needs a
   fresh preparation; an exact retry uses the original frozen admission/result.

7. Runtime marks that final existing admission's Theme member `resolved-v1`.
   GenericHost materializes R as the existing `theme.json` and
   `materialized_objects["theme"]`. Final Root preparation consumes this
   validated resolved document directly through the existing Theme reader;
   it must not merge overrides a second time. This is a bounded consumer wiring
   change, not another resolver. App forwards the same admitted R to preview;
   Viewing consumes it. Catalog CRUD and preparation never edit the film.

The two input hints and the two admission mode values above are proposed
semantics on existing opaque task/admission carriers, not existing behavior or
new public DTOs. They carry no source bytes or authority by themselves. No new
endpoint, schema/client artifact, pack port, delegation scope, capture provider,
storage system or attestation record is needed. Existing output association
and frozen task spec supply the result binding, without an evidence ledger.

## Agreement and evidence boundary

Agent/Runtime should agree specifically to project-writer original admission,
the one typed namespace selection/retention rule, candidate base restriction,
and this nondelegated private root/result contract. App/Viewing should agree
that the pin/R drives display and that unbound explicit labels remain
unqualified. Agreement is a prerequisite to a later implementation brief.

This task performed source reads only. No tests, generated schema/client/pin,
release, renderer/browser/MP4, full suite or old28 repetition ran. No existing
test expectation or product code changed. First-source, preparation settlement
and final forwarding remain unimplemented and unverified. The smallest required
exception is to give this currently opaque namespace pin explicit film-source
meaning; private byte custody alone cannot substitute for that decision.

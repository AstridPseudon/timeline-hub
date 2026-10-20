# Selected PARAM original DocumentPin authority: read-only audit

**Completed audit; production binding remains blocked.** No general existing accessor maps an accepted selected clip to its ORIGINAL `DocumentPin`. Raw selection/ownership and exact retained reads already exist. The missing step is the authority rule associating that selection, at its captured accepted basis, with one particular pack-document version. Do not replace it with latest metadata, a manifest scan that chooses a winner, or another hydrator.

Read PLAN.md and `design/app-selected-param013-production-binding-source.md` first. No settled decision changed. This audit narrows the earlier blocker: **native admission does return a full document binding triple**, and host object spreads can preserve it in browser metadata. It is the current resolution's binding, without timeline/clip provenance, and is not proof of an original accepted-basis pin.

## Frozen sources and scope

- App: `/home/user/work/wt/app-m2-selected-param-original-pin-authority-audit`, HEAD `64d7e19b3c0e9db217381c955b8e50944879d49f`; generated normal Runtime0.2.13. All tracked files unchanged.
- Native S2: Agent `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`, read-only snapshot `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/agent-s2`. Raw command-schema SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`, matching published013's S2. Probe checks six relevant snapshot files against `git show` of that exact commit; hashes in `notes/trace_pin.json`.
- Moving Agent integration was observed at `cf7448ed6c1298b172d004914cfe2bb8c99048e7`, whose raw command-schema SHA256 is `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224`. It is **not** relabeled as S2. Executable conclusions below use S2.
- No product/test/package edit, build, install, project tsc, full suite, central-service request, browser, socket, external message, Git mutation, dependency/cache/venv write, or integration-worktree write. All probes and outputs are worker-private scratch. No KEEP.

App paths below are relative to the assigned App root; Agent paths are relative to the frozen S2 snapshot. Line references identify the inspected source.

## Existing App mapping, through the last authoritative field

| Step | Exact existing source | Data and limit |
| --- | --- | --- |
| Accepted basis | `src/integrations/runtime/dataProvider.ts:778–819`, `:1694–1701` | `loadTimelineCommandBasis()` reads history head, exact parent image, exact shot/internal images and manifest; returns `head`, `canonicalDocument`, `history`, `graph`. Documents are checked/deduplicated by the complete triple, so different versions of one document are allowed. No document content or selected-clip association is added. |
| Local accepted snapshot | `src/tools/video-editor/commands/authoringBundle.ts:108–156`, `:212–222`; `commands/commitSession.ts:74–78` | Opener clones the closure and preserves it in `source_mapping._runtime_document`. Session keeps `acceptedBasis`/`acceptedBundle`. This is the existing access point for **accepted manifest pins**, not a new canonical loader. |
| Display clip -> raw clip | `src/tools/video-editor/commands/commitSession.ts:439–483`; `commands/clipMovePrimitives.ts:124–148` | Capture checks display project/timeline/head, exactly one displayed ID, no migration-only pinned group, and explicit parent or occurrence identity. Occurrence also checks `ownerRef`, `occurrenceId`, `rawClipId`, source shot/internal revisions and stable output identity. It then reads `new AuthoredState(bundle).entity(select)`. Parent clips use nonempty `parent.clips`, otherwise `parent.config.clips`; occurrence clips use the resolved occurrence-owned internal timeline. No display-ID suffix guessing. |
| Raw element selection | `src/tools/video-editor/commands/commitSession.ts:474–481` | Nonempty raw `elementRef` wins, otherwise `element_ref`; selected pack owner must exist. The captured bundle/select/local generation and `acceptedBasisAvailable` stay frozen. The raw selection carries `{packId,id,kind,revision}`, not a document version/pin. |
| Exact document/object read | `src/integrations/runtime/retainedParamInputs.ts:28–88`; `commands/commitSession.ts:486–508` | Caller must already provide the original closed `DocumentPin`. Helper reads `VerifiedDocument`, matches exact pin/project/kind/pack/realm-relative manifest, exactly one matching admission, then that admission's `snapshot_object` through the same exact pin. It returns existing `{verified,objects}`. It does not determine where the pin came from or discover one by selection. |
| Captured use | `src/tools/video-editor/commands/commitSession.ts:494–519`; `commands/clipParamsCapture.ts:6–30` | Once provided, pin and basis cannot refresh across awaits; raw values/clear/source go to `clip.set-params`. Semantic validation is native. `acceptedBasisAvailable` is never promoted by this audit. |
| Production seam | `src/tools/video-editor/hooks/useTimelineSave.ts:99–102`; `components/PropertiesPanel/PropertiesPanel.tsx:522–559`; `components/PropertiesPanel/ClipPanelBody.tsx:48–52` | Save does not pass `paramReadClient`; PropertiesPanel does not pass staged `retainedDocumentPin`, `timelineOps`, `commandState`. Existing optional props are consumers, not authority sources. |

`TimelineCommandBasis.history.items` can expose previously accepted record associations, but it is a paginated history response, not an original-pin accessor. Session `latestOwn` at `commitSession.ts:99–100` selects the current author's undo candidate, not a selected-element schema source. Bootstrap/legacy clips can lack any PARAM or element-change record. A new history traversal and a rule choosing first/last/author would be a new policy, not an existing mapping.

## Admission/catalog: full triple exists, but does not name the accepted clip's original source

1. `src/tools/video-editor/contexts/VideoEditorProvider.tsx:259–271` requests pack preview admission from resolved clip element refs. The request contains project + element refs, **no timeline accepted head, clip select or original DocumentPin**.
2. `config/vite/vite.config.ts:97–109` uses the existing authenticated native Runtime client for `getDocument(project,id)` and invokes the configured native `project-pack resolve` command with realm/project/pack/element/kind/revision. This is distinct from the command session's exact-read capability.
3. `config/vite/projectElementSelection.ts:40–77` reads the current default/named project-pack document and finds the exact declaration in its admissions. Native S2 `astrid/core/element/project_packs.py:704–731` likewise calls `_read_document`, finds one admission, and returns the record plus:

```ts
binding: { projectId, documentId, documentVersion, contentDigest }
```

The triple maps structurally to `{document_id: binding.documentId, version: binding.documentVersion, content_digest: binding.contentDigest}`. This is an exact **current resolver** source, not a selected-clip accepted-basis association. Resolving an unchanged old element after another admission can return a newer document version. `projectElementSelection.ts:75–76` checks it against the concurrently read current document on a cache miss. Its local digest comparison is a consistency check; App must not recompute one to manufacture an original pin.
4. Do not assume the full triple is discarded: `verifyElementAdmissions()` at `config/vite/astridElementAdmissions.ts:108,129` spreads the native record; `generateElementAdmissionModule():135–140` strips only snapshot/import paths and can retain extra `binding` metadata. However, `AdmittedElement`/`ProjectElementAuthoring` in `runtime/admitted-elements.ts:10–24` do not expose this binding as a typed pin capability. `admittedCatalogEntries():129–136` projects descriptor/authoring and drops it. `AstridElementDescriptor` (`runtime/astrid-element-host.ts:17–25`) has no DocumentPin. Reading a hidden extra property by cast would not establish original authority.
5. There is also no guaranteed “fresh current binding” at that hidden extra property: selection's `resolvedCache` key (`config/vite/projectElementSelection.ts:69–85`) includes the selected snapshot digest but not document version/full content digest. A cache hit bypasses the current-document binding check and can reuse a prior native record after an unrelated admission. This is a source-inspected observation, not a browser repro or a requested cache fix.
6. `AstridElementParams.tsx:19–32` retains a descriptor for display hints after an explicit pin arrives. `astrid-element-param-descriptor.ts:35–53` matches the four element identity fields. Neither establishes document authority.

`selectionDigest` is a host build-selection digest; element `revision` is an immutable element/source identity; admission `snapshot_digest` is a resource closure digest; `snapshot_object.digest` identifies portable bytes; parent/shot/internal `content_digest` identifies timeline images. None is the project-pack **document content** digest in a DocumentPin. `project.documentId/documentVersion` is only the default project pack's current authoring metadata and omits the required digest.

## Native S2 semantics and exact recorded relationship

- `_scalar_commands.py:98–128` requires caller `args.schema_source`, resolves the matching retained verified input, validates the exact declaration/portable snapshot, records `params.schema` (pin) and `params.snapshot` (`source`, exact `element`, `object`), binds `params.element` to the raw clip ref, and retains the verified document in `source_mapping.pinned_documents`. It does not write a DocumentPin into the authored clip.
- `commit.py:350–392` hydrates exact manifest pins plus the command's `schema_source`; `:395–438` resolves the selected raw element at the real command stage using the existing ports. This is the one native resolver; no App equivalent is proposed.
- `commit.py:279–285,304` unions retained pins into canonical `dependency_manifest.documents`. The manifest is global, sorted/deduplicated by full triple, and preserves multiple consumed versions.
- S2 `clip.set-element` (`_clip_scalar_commands.py:111–140`) similarly uses `_selected_schema` and writes only `elementRef` (clearing the alias), leaving its source association in recorded history rather than in the raw clip.
- An authenticated accepted history record **does** provide the exact historical mapping:

```text
HistoryEntry.records.commands[i]
  .command.select = parent/clip:clip-a
  .command.args.schema_source = P
  .bindings[key=params.element].ref = parent/clip:clip-a
  .dependencies[key=params.schema].pin = P
  .dependencies[key=params.snapshot].pin = {source:P, element:E, object:O}
```

These existing `HistoryEntry`/`Recorder` fields are generated at `timeline-commit-types.ts:86–87` and produced by native handlers. They prove what that recorded edit consumed. They do not decide which record is the required source for a new edit at an arbitrary accepted head, especially a bootstrap/add/legacy clip with no such record or a clip later retargeted/restored. No receipt/history inference was implemented.

## Executable counterexample using actual native handlers and real App read code

Artifacts: `workers/app-m2-selected-param-original-pin-authority-audit/notes/trace_pin.py`, `trace_pin.json`, `trace_app.mjs`, `trace_app.json`.

These are **diagnostic probes, not new repository behavior tests or authenticated Runtime fixtures**. Native probe reuses the previously retained portable-input corpus in `workers/app-m2-selected-param-server-authority-stage/notes/native-provider-result.json` and S2's existing `DetachedRealm`/`DetachedPort` test helpers. The build receipt and authority ports are synthetic; no admission/build was run. Native validator/provider/record/compiler code is real. V2 is explicitly formed with native admission's append semantics (retaining the old admission and appending the new one), not a claimed live-service capture.

Exact raw selected clip, accepted by S2 provider from its original canonical closure:

```json
{
  "id": "clip-a",
  "track": "picture",
  "asset": "picture",
  "clipType": "reveal",
  "at": 1,
  "hold": 2,
  "app": {
    "org.example": {
      "literal": "clip-a",
      "clear": null
    }
  },
  "elementRef": {
    "id": "reveal",
    "kind": "effect",
    "packId": "project_a5f654b128acc2020fb7",
    "revision": "sha256:0e00fcd197e2757e382ceddf4ef5fbf0c0b7b73ab281cf5d99d9105a11ac3bcf"
  },
  "params": {
    "seed": 4,
    "opaque": [
      null,
      false,
      {}
    ]
  }
}
```

Its original full canonical dependency manifest is:

```json
{
  "shots": [
    {
      "shot_id": "chapter-shot",
      "revision_id": "shot-1",
      "internal_timeline_revision_id": "internal-1",
      "content_digest": "sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775"
    }
  ],
  "internal_timelines": [
    {
      "timeline_id": "chapter-1",
      "revision_id": "internal-1",
      "content_digest": "sha256:40c17ebc38241cfc57e7104070b70d2d858c7cf3c731fbbe410459c99bf5aaa0"
    }
  ],
  "media": [
    {
      "media_id": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
      "content_digest": "sha256:1111111111111111111111111111111111111111111111111111111111111111"
    }
  ],
  "documents": []
}
```

There is no original DocumentPin to retrieve from that clip/closure. This is supported raw input; it is not rejected merely because a selected clip has no consumed document pin.

The native probe makes two sequences from that same base:

```text
A: clip.set-params seed8/source=P1 -> seed9/source=P2
B: clip.set-params seed8/source=P2 -> seed9/source=P1
```

Both pins admit the same original exact element revision/portable descriptor. All four native commits accept. Both final **entire canonical documents are equal as JSON values**, including revision, raw elementRef, params and full manifest, while their last accepted records select different source pins. Final manifest's shot/internal/media sections equal the original above; its exact `documents` array is:

```json
[
  {
    "document_id": "document:d70cf67a-a5f9-577c-915d-2458074abdfe",
    "version": 1,
    "content_digest": "sha256:ce3c29054ac73f2c93b4ac99e34b7646ba150f677695d387c09aa4dea02bbb40"
  },
  {
    "document_id": "document:d70cf67a-a5f9-577c-915d-2458074abdfe",
    "version": 2,
    "content_digest": "sha256:542cd0de114fc707474da7f786c1e3dd33fc72068e50c06ff10aafb699fac0a6"
  }
]
```

Thus canonical data alone cannot recover either the first-used or last-used original source. This is not a native authority bypass: each requested exact pin is independently resolved. It proves that source identity was an input to the edit, not an invertible property of `elementRef` or the manifest.

The second probe executes the **unchanged real App** `authoringBundleFromDocument` and `readRetainedParamInputs` using Node22 type erasure (no bundler, package install, Vite/cache). It confirms the initial empty closure remains empty, both final pins survive without a clip association, missing source refuses before reads, and either explicit source passes the exact read helper for the same selected element. Exactly two document + two object reads use their supplied pins. Synthetic read responses do not establish authenticated host binding.

## Smallest Agent-owned contract question and next bounded result

**Question for the Agent edit-contract owner:** For accepted project `project-1` / timeline `film`, raw `parent/clip:clip-a` and exact element E above, which existing accepted field/record is authoritative for the ORIGINAL `clip.set-params.args.schema_source` when `dependency_manifest.documents=[]`? When it contains both P1 and P2, what existing binding selects one? Is “original” defined as a particular accepted admission/edit record, or as the exact authenticated native admission binding captured when this new edit begins? The latter would require an explicit authority rule; it cannot be inferred from current `resolve_admitted_element(...).binding`, which has no timeline/head/select input.

**Requested bounded answer:** Point to one existing accepted association (for both parent and occurrence clips, including initially unpinned clips), using the existing `DocumentPin`, `VerifiedDocument`, `HistoryEntry.records` or native record `binding` fields above. If none is authoritative, say so and identify which existing Agent-owned admission/edit producer must preserve the association. Decide the empty/two-pin case before App implementation. No invented DTO, endpoint, browser schema validator or second hydrator is needed for this question. A unique candidate found by scanning retained documents proves uniqueness of matching content, not historical originality; do not silently adopt that policy.

After that answer, App's next bounded unit is **existing accessor wiring** at the captured session basis: raw selected identity + explicitly authoritative pin, forwarding only `getProjectVerifiedDocument` and `getProjectVerifiedDocumentObject` through existing authenticated session/project scope, then existing helper + existing PARAM props/ops. Pin/head/generation must stay original across awaits. `RuntimeDataProvider.documents.get` (`dataProvider.ts:376–380`) is a current document read, not an exact retained read. The generated exact methods exist (`generated.ts:182–183`), but facade `client` (`client.ts:287`) / `withSession` (`:506`) and provider client/project (`dataProvider.ts:330–331`) are private. No new client or private-member cast is justified.

Missing/ambiguous original authority stays a **visible, draft-preserving refusal**. Current structural pin gate says `selected pack requires an original exact DocumentPin`; current session without the authenticated read capability says `Selected clip parameter input reads are unavailable; draft preserved`. This audit does not activate the staged UI or change fallback behavior. The existing lack of production refusal wiring itself remains part of the separately assigned binding work.

## Commands, results, and unverified gates

From the assigned App worktree; `$O` below is the absolute orchestrator path given in the task, and `$W=$O/workers/app-m2-selected-param-original-pin-authority-audit`.

```bash
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/notes/trace_pin.py"
node --experimental-strip-types "$W/notes/trace_app.mjs"
git diff --check
git diff --exit-code
git status --porcelain
```

- Native diagnostic: **exit0**, six pinned source-blob comparisons and five reported assertion groups pass; four actual S2 provider acceptances through existing in-memory test ports. JSON contains exact original/final closures, verified rows, distinct records and source hashes.
- App diagnostic: **exit0**, four reported assertion groups pass; real opener/helper, missing-pin refusal with zero reads, two exact pin/document/object chains. Node `v22.22.0`.
- Whitespace/source cleanliness checks: **exit0**, empty diff/status. No tracked App file change.
- Repository test suites were **not run** for this read-only audit; these assertions are diagnostic evidence only and do not replace main's suites. No full/build/tsc/browser/socket/install/package or live authenticated request. Actual custody/storage, real admission build, native Runtime service acceptance/restart/retry/inverse and actual PropertiesPanel binding/browser zero-legacy gate remain **unverified here**. Prior report test totals were read, not rerun or claimed as this audit's passes.

Audit is DONE; the original-pin production seam needs the bounded Agent contract answer above. Wrote design report, worker report and commit-msg; no KEEP or product change.

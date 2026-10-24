## P2 assessment

Base verified: `66354161950d1e747965c095ea97b881d2592708`, tree `9a37265f0286128df7e6240a9df9877d959474af`. Worktree is clean; no source or test files changed.

### Oracle classifications

| Branch | Classification | Source-backed expected shape |
|---|---|---|
| Parent move | ORACLE FAIL; production builder PASS | `merge: fields`; exact declared parent reads; `created: []`; intent `Move f2-app-clip on V1`; one `doc.patch` `set` of `parent/clips/id:f2-app-clip/at` from `0` to `5`. |
| Catalog apply | ORACLE FAIL; product cause UNKNOWN | `merge: atomic`; exact collection/selected-row/tracks reads; `created: ["parent/clip:<new-id>"]`; intent `timeline.apply_element`; submitted `list.insert` patch. |
| Element params | ORACLE FAIL; execution NOT REACHED/UNKNOWN | `merge: atomic`; exact post-apply clip collection plus selected `id`, `elementRef`, `params` reads; `created: []`; intent `timeline.update_element`; one `set` of the new clip’s `params` from absent to `{bob: 12}`. |
| Inverse | ORACLE FAIL; production builder PASS | `merge: fields`; no request/step reads; inverse command targets exactly the prior publication; submitted step `patch: []`, label/intent `Undo timeline`. |

The current helpers incorrectly require atomic/no reads for these document patches and reject the inverse’s full v2 metadata shape.

### Exact branch details

Parent move source is `timelineLocalSaveHandoff.ts:517-559`, with request construction in `localSaveSession.ts:168-185`.

For the seeded fixture, the exact read set is:

- selected `f2-app-clip`: `id`, `track`, `at`, `clipType`, `hold`, `from`, `to`, `speed`, `asset`;
- `config.output.fps`;
- `config.registry.assets.f2-app`;
- `config.tracks/id:V1/kind`;
- `config.pinnedShotGroups`;
- `config.clips` collection membership/order;
- sibling `f2-transition-clip`: `track`, then the same timing fields and `config.registry.assets.f2-video`.

No theme fallback reads apply because the fixture has `output.fps`. Request and step reads must equal this exact producer set, with no extras.

Catalog apply uses `ElementsLibraryPanel.tsx:70-101` and `timelineLocalSaveHandoff.ts:337-380`. The overlay operation creates the appended clip (`element-am-burst-0` for the fixture), and the submitted logical patch is:

```text
list.insert
ref: parent
path: ["clips"]
id: <new-id>
before: absent
value: complete new clip row
order_before: ["f2-app-clip", "f2-transition-clip"]
after_id: "f2-transition-clip"
```

Its exact reads are the `config.clips` collection plus selected `f2-app-clip` fields `id`, `clipType`, `hold`, `from`, `to`, `speed`, `track`, `at`, and the complete `config.tracks` field. The catalog itself is local input, not a document read.

Params uses the post-apply collection/order and reads only the selected new clip’s `id`, `elementRef`, and absent `params`. The submitted patch is:

```text
set
ref: parent
path: ["clips", "id:<new-id>", "params"]
before: absent
value: { bob: 12 }
```

The operation intent is exactly `timeline.update_element`.

Inverse is produced by `timelineLocalSaveHandoff.ts:179-195` and serialized by `localSaveSession.ts:176-185`:

```text
commands: [timeline.inverse(publications: [targetPublication])]
label: "Undo timeline"
steps: [{ id, label: "Undo timeline", intent: "Undo timeline",
          tags: [], command_ordinals: [0], patch: [] }]
merge: "fields"
dry_run: false
source: { via: "app" }
```

No request or step `reads` field is present.

All accepted/merged/rebased replies must retain the full canonical closure, digest, id map, provider/compiler/publisher metadata, authoritative steps and receipt. History must record the commit, authoritative reads/writes/bindings/created claims, and undo metadata. Reload must preserve canonical state and complete history; inverse history must contain `undo_of: [target]`, preserve earlier entries, and restore the exact prior document. Legacy routes remain forbidden.

### Original-page readiness

`three-products.p2-elements-assets.spec.ts:163-169` only waits for connection, project selection, and track visibility. It does not wait for the production save owner.

The existing genuine boundary is `three-products.spec.ts:1264-1276`: after the same connection/project/timeline guards, it captures prior owner IDs and waits up to the existing 90-second ceiling for a new owner with `!pending && intents.length === 0`. Production ownership is established through `useTimelineSave.ts:302-392`; element saves then explicitly await `localOwner.ready` at `useTimelineSave.ts:776-788`.

Therefore the minimal meaningful original-case setup is the existing fresh-settled-owner predicate before the gesture, retaining the existing 5,000 ms `applied` assertion and 90,000 ms request ceiling. D28’s separate preflight page/seed is not same-case proof. The retained element failure at line 390 proves only that `applied` was absent while `Applying…` remained; it does not prove the pending await caused it. Causal attribution remains UNKNOWN without same-case retained owner/outbox phase evidence.

### Verification

- `git diff --check` — passed.
- `git status --porcelain=v1` — clean.
- Relevant source hashes recorded; no unexpected changes.
- `node --version` — `v22.22.0`.
- No targeted tests rerun: no source/test changes were made, and the task explicitly disallowed repeated source-cohort/type/lint runs. Retained evidence remains the prior 23809 run: exit 1, 3 failures, 5 not run.

Commit message written with P2 in the subject; `DONE` marker created.
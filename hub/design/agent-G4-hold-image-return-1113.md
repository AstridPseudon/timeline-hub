# G4 held-image first return

## Result

**HOLD: no Runtime acceptance credit.** The Agent source/recipe change remains
valid, but current Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181` refuses
an authenticated current-provider genesis before accepting the held-image
command. No Runtime, contract, pin, provider, App, fixture, or Agent source
change was made in this return.

## Bounded current-provider probe

The probe used normal public service creation (`RuntimeService.create_project`,
`create_timeline`, and real `import_media`), the current Agent provider, and
Agent capture functions. It did not call `publish_parent_composition`, create
a prepared/fake acceptance, write the journal, or use a closure cache.

The exact captured request was:

```json
{
  "api_version": 1,
  "project_id": "bcaff4677fd940b1b77d384fe18c24b7",
  "timeline_id": "film",
  "base_revision_id": "bootstrap-4fc98bfa65594d2884fd4dfc865e3322",
  "base_publication_id": "txn-0bf90065227b4300bdc4ca000814f4cd",
  "source": {"via": "python"},
  "commands": [
    {"op": "track.create", "select": "parent", "args": {"row": {"id": "picture", "kind": "visual"}}},
    {"op": "track.create", "select": "parent", "args": {"row": {"id": "overlay", "kind": "visual"}}},
    {"op": "clip.add-media", "select": "parent", "args": {"row": {"id": "parent-clip", "clipType": "image", "asset": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "track": "overlay", "at": 0, "hold": 3, "opaque": [null, false]}, "media": {"asset": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "generation_id": "generation-task-bffe44ef6b83411c9c686a002451fbca", "variant_id": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "object_id": "sha256:1b2bbf246184130848230202b2aad630691442c709f7ff015eb25b8639a5e5e1", "catalog_digest": "sha256:81fde1f3ceaf203f4ade9dc3b98582a7cc791ec7dbd17194be49a5feb5f418fa"}}},
    {"op": "occurrence.create", "select": "parent", "args": {"occurrence_id": "occ-a", "shot_id": "shot-a", "name": "A", "track": "picture", "on": 0, "duration": 5}},
    {"op": "track.create", "select": "occurrence:occ-a", "args": {"row": {"id": "picture", "kind": "visual"}}},
    {"op": "occurrence.add-media", "select": "occurrence:occ-a", "args": {"row": {"id": "clip-a", "clipType": "hold", "asset": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "track": "picture", "at": 2, "hold": 2, "opaque": [null, false]}, "media": {"asset": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "generation_id": "generation-task-bffe44ef6b83411c9c686a002451fbca", "variant_id": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b", "object_id": "sha256:1b2bbf246184130848230202b2aad630691442c709f7ff015eb25b8639a5e5e1", "catalog_digest": "sha256:81fde1f3ceaf203f4ade9dc3b98582a7cc791ec7dbd17194be49a5feb5f418fa"}}}
  ]
}
```

The exact Runtime-verified selection/input was:

```json
{
  "asset": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b",
  "generation_id": "generation-task-bffe44ef6b83411c9c686a002451fbca",
  "variant_id": "initial-0d7c3ec6a05f88184bc498a50cf47723fb41acea7afb8ff5f006975193e9937b",
  "object_id": "sha256:1b2bbf246184130848230202b2aad630691442c709f7ff015eb25b8639a5e5e1",
  "catalog_digest": "sha256:81fde1f3ceaf203f4ade9dc3b98582a7cc791ec7dbd17194be49a5feb5f418fa"
}
```

Runtime returned `422 invalid_records`:

```json
{
  "reason": "invalid_records",
  "message": "provider occurrence alias is outside its boundary",
  "failing_ref": "occurrence:occ-a/source",
  "failing_path": ["output", "fps"],
  "validation_boundary_keys": ["parent"],
  "validation_parent_occurrences": []
}
```

The prepared Agent candidate did contain the authored occurrence, shot and
internal closure. Its canonical identities were:

- parent revision digest `sha256:f7192ae725b3810a0c8a0fd0949937e320671f73781bf8229c427db06196f0f1`;
- shot `shot-a`, revision `authoring-shot-revision-e832a0407b37e34527dd6501bd96d7358992b970ee73b57b31628582b91f93a0`, digest `sha256:3a55db5db8bd1d0fa267781ba61e1e90233c2788dbf97bd3f7d30c58453b434f`;
- internal `film`, revision `authoring-timeline-revision-039f7c63da7a88ee9f50379104a10fde9e5e5fd46f3f0a8c0b3218a5f8032ce8`, digest `sha256:c4a51d1d648d41dca8d42b154d0791383269c406e33815e32454df517bfcab8a`;
- retained media object `sha256:1b2bbf246184130848230202b2aad630691442c709f7ff015eb25b8639a5e5e1`.

The candidate preserved `clipType: "hold"` and `hold: 2` in the occurrence
clip. Its command origins/bindings were captured as follows: `track.create`
bound `parent/track:picture`; `clip.add-media` bound `parent` and
`parent/track:overlay` with exact `media.new`; `occurrence.create` bound
`parent/track:picture`; child `track.create` bound `occurrence:occ-a`; and
`occurrence.add-media` bound `occurrence:occ-a`, its clip/track collections,
and `occurrence:occ-a/track:picture` with the same exact `media.new` pin.
Every command's `commit.input` origin pointed to the authenticated bootstrap
head and its prepared canonical candidate; no guessed pin or alias was added.

History before and after was unchanged: only the normal `bootstrap:film`
record remained, with head revision
`bootstrap-4fc98bfa65594d2884fd4dfc865e3322` and publication
`txn-0bf90065227b4300bdc4ca000814f4cd`. Runtime therefore performed no write.

## Classification and handback

This is a Runtime boundary seam. Runtime validation builds the failing step's
boundary from `parent` only, while the Agent candidate's authenticated
bindings and canonical document contain the created occurrence's source. The
Agent-owned recipe file cannot safely repair that boundary: waiving the read,
retargeting it to `parent`, or adding a guessed pin would violate the request's
authenticity and custody requirements. Hand back to the Runtime owner to make
created-child occurrence/source boundaries available to `timeline_commit_auth`
while retaining the current exact Agent claims.

The old acceptance fixture's `publish_parent_composition` setup remains a
separate retired-route failure and was not reintroduced. No actual held-image
ADD/SWAP acceptance or video-hold refusal is credited from this run.

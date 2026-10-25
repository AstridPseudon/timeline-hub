# D92 bounded genuine setup

Source origins:

- Agent source: `/home/user/work/wt/agt-F-D92-genuine-unused-0242`, HEAD `f6d0ae5997f634ef9743e9edce77a7f995cf715d` before the source edit.
- Runtime source: `/home/user/work/runtime`, integration HEAD `6634a17f3ffd885567ba3c91b6c7a560df7375a4`.
- Runtime API path: `RuntimeService.create_project` → `create_timeline` → `import_media` → `commit_timeline` with the registered current Agent provider.
- No SQL, synthetic history, fabricated pins, custody writes, or shared-worktree writes.

The one bounded command used an isolated `/tmp/d92-genuine-*` realm, imported real audio bytes, created ordinary current bootstrap commits, then submitted Commit A (`doc.patch` consumer plus `media.admit`) and Commit B (normal emitted `doc.patch` consumer removal).

Observed transcript:

```json
{
  "project_id": "00a98d692b2046209afe8758d8535f0c",
  "timeline_id": "film",
  "media_id": "sha256:0ba8d8660e99dc076d5573ad9f13743a6d6e191481d3f92c5131ff7da3813b7b",
  "commit_a_pair": {
    "revision_id": "authoring-parent-revision-468d4ae6a93782158fefb440436df49f2b7168726b6ab785a9284184bfc53c8e",
    "publication_id": "txn-3d77b55b36264d919f3dff34f1aadf29"
  },
  "commit_b_pair": {
    "revision_id": "authoring-parent-revision-f8e6440c45236aed33a528dcaa25c6b575cae5cc12e047a099c3dd6cc717eecb",
    "publication_id": "txn-4f9905dfeef64c9892d9e3b387a2510f"
  },
  "commands_a": ["doc.patch", "media.admit"],
  "commands_b": ["doc.patch"],
  "b_payload_contains_pin": false,
  "b_manifest_media": [
    {
      "media_id": "sha256:0ba8d8660e99dc076d5573ad9f13743a6d6e191481d3f92c5131ff7da3813b7b",
      "content_digest": "sha256:0ba8d8660e99dc076d5573ad9f13743a6d6e191481d3f92c5131ff7da3813b7b"
    }
  ],
  "history_head": {
    "revision_id": "authoring-parent-revision-f8e6440c45236aed33a528dcaa25c6b575cae5cc12e047a099c3dd6cc717eecb",
    "publication_id": "txn-4f9905dfeef64c9892d9e3b387a2510f"
  }
}
```

The migrated compound helper was not executed as part of this source task, per the brief; the transcript above is the independent bounded current-API setup proof.

## Result

Produced [a4-image-current-0043-output.json](/home/user/work/wt/app-A4-image-current-producer-0059/a4-image-current-0043-output.json).

- Base: `22efcda3da4005f8663c078439ff0edbfade69be`
- Input: 8,957 bytes; SHA-256 `09f4afbb93d7f6c74f37f661565b86d2015f3d33f0c3f5e1a6664a346a2f24c4`
- Output: 1,371 bytes; SHA-256 `b9f9b3c5be3fe54e3d29cc604b5bc888ddf4492652129aef2a5e970e4368bc7a`
- Handoff source blob: `551f2fa739a5932360a7e1a9e59abae45ea97e4d`
- Producer source blob: `8f686e3e3be448995eae1c43a9e86d1dee217aeb`

Producer invocation succeeded once via external Vitest `createVitest` with normal aliases and private cache. Input remained byte-identical. Request shape passed validation: one `clip.add-media`, `select: "parent"`, `intent: {}`, exact five-field media selection, `merge: "fields"`, one empty-patch step. Raw `visual.opaque` remained at its original location/value; no rehome or flattening.

Runtime acceptance: **NOT RUN**.

```json
{"request":{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-038ec4093d414e55d51ef6d29eead099b6fc0fed1821c46d9c354ad321db8cff","base_publication_id":"txn-ffc7992ec173410d8810b90278d6a1e3","commands":[{"schema_version":1,"op":"clip.add-media","version":"1","select":"parent","args":{"row":{"id":"clip-0","at":2,"track":"visual","asset":"variant-01ef09ccfe29c2615c9c28960f79fd4eab1320851267594c507f2e72cad4a0ea","clipType":"hold","hold":5,"opacity":1},"media":{"asset":"variant-01ef09ccfe29c2615c9c28960f79fd4eab1320851267594c507f2e72cad4a0ea","generation_id":"generation-d4536a96a172c8a3abca172fb359d5c9fe1f521e5006408b39fcecafb17a962c","variant_id":"variant-01ef09ccfe29c2615c9c28960f79fd4eab1320851267594c507f2e72cad4a0ea","object_id":"sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437","catalog_digest":"sha256:ec3fc782f68358b0bcd2cb8cd3f983d60a99cbec58806cf5fc9d1a021fe75975"}},"intent":{}}],"source":{"via":"app"},"label":"Add media","dry_run":false,"steps":[{"id":"99826979-46a2-4716-bf87-5b65847976a6","label":"Add media","intent":"Add media","tags":[],"command_ordinals":[0],"patch":[]}],"merge":"fields"},"idempotency_key":"d3961806-1c89-4f19-9bb0-535391a0de4d","request_body_sha256":"sha256:9f405ef5f71872c42e9ae25c15abb0a41764774836b66321d250817ea0e70141"}
```